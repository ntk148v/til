# Query execution

Source:

- <https://clickhouse.com/docs/guides/developer/understanding-query-execution-with-the-analyzer>
- <https://youtu.be/hP6G2Nlz_cA>

```sql
CREATE TABLE session_events(
   clientId UUID,
   sessionId UUID,
   pageId UUID,
   timestamp DateTime,
   type String
) ORDER BY (timestamp);

INSERT INTO session_events SELECT * FROM generateRandom('clientId UUID,
   sessionId UUID,
   pageId UUID,
   timestamp DateTime,
   type Enum(\'type1\', \'type2\')', 1, 10, 2) LIMIT 1000;
```

The execution of a query is decomposed into many steps. Each step of the query execution can be analyzed and troubleshooted using the corresponding `EXPLAIN` query.

![](https://clickhouse.com/docs/assets/ideal-img/analyzer1.fa6c1ee.1024.png)

## 1. Parser

The goal of a parser is to transform the query text into an Abstract Syntax Tree (AST).

```sql
EXPLAIN AST
SELECT
    min(timestamp),
    max(timestamp)
FROM session_events

Query id: eb074673-8b32-4d7d-ad4a-3c9cff9c4230

    ┌─explain─────────────────────────────────────┐
 1. │ SelectWithUnionQuery (children 1)           │
 2. │  ExpressionList (children 1)                │
 3. │   SelectQuery (children 2)                  │
 4. │    ExpressionList (children 2)              │
 5. │     Function min (children 1)               │
 6. │      ExpressionList (children 1)            │
 7. │       Identifier timestamp                  │
 8. │     Function max (children 1)               │
 9. │      ExpressionList (children 1)            │
10. │       Identifier timestamp                  │
11. │    TablesInSelectQuery (children 1)         │
12. │     TablesInSelectQueryElement (children 1) │
13. │      TableExpression (children 1)           │
14. │       TableIdentifier session_events        │
    └─────────────────────────────────────────────┘

14 rows in set. Elapsed: 0.001 sec.
```

![](https://clickhouse.com/docs/assets/ideal-img/analyzer2.b8e73e5.1024.png)

## 2. Analyzer

ClickHouse currently has two architectures for the Analyzer, but we just describe only the new architecture. The analyzer takes an AST and trasnform it into a query tree. The main benefit of a query tree over an AST is that a lot of the components will be resolved, like the storage for instance. We also know from which table to read, aliases are also resolved, and the tree knows the different data types used. With all these benefits, the analyzer can apply optimizations. The way these optimizations work is via "passes". Every pass is going to look for different optimizations.

```text
0 – QueryAnalysisPass
1 – GroupingFunctionsResolvePass
2 – RemoveUnusedProjectionColumnsPass
3 – FunctionToSubcolumnsPass
4 – ConvertLogicalExpressionToCNFPass
5 – RewriteSumFunctionWithSumAndCountPass
6 – CountDistinctPass
7 – UniqToCountPass
8 – RewriteAggregateFunctionWithIfPass
9 – SumIfToCountIfPass
10 – RewriteArrayExistsToHasPass
11 – NormalizeCountVariantsPass
12 – AggregateFunctionsArithmericOperationsPass
13 – UniqInjectiveFunctionsEliminationPass
14 – OptimizeGroupByFunctionKeysPass
15 – OptimizeGroupByInjectiveFunctionsPass
16 – MultiIfToIfPass
17 – IfConstantConditionPass
18 – IfChainToMultiIfPass
19 – ComparisonTupleEliminationPass
20 – OptimizeRedundantFunctionsInOrderByPass
21 – OrderByTupleEliminationPass
22 – OrderByLimitByDuplicateEliminationPass
23 – FuseFunctionsPass
24 – IfTransformStringsToEnumPass
25 – ConvertOrLikeChainPass
26 – LogicalExpressionOptimizerPass
27 – AutoFinalOnQueryPass
28 – CrossToInnerJoinPass
29 – ShardNumColumnToFunctionPass
30 – OptimizeDateOrDateTimeConverterWithPreimagePass
```

```sql
EXPLAIN QUERY TREE passes = 0
SELECT
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date
FROM session_events
SETTINGS allow_experimental_analyzer = 1

Query id: 3aa07359-d9fe-40bd-af8f-27dc2608d0e7

    ┌─explain────────────────────────────────────────────────────────────────────────────────┐
 1. │ QUERY id: 0                                                                            │
 2. │   PROJECTION                                                                           │
 3. │     LIST id: 1, nodes: 2                                                               │
 4. │       FUNCTION id: 2, alias: minimum_date, function_name: min, function_type: ordinary │
 5. │         ARGUMENTS                                                                      │
 6. │           LIST id: 3, nodes: 1                                                         │
 7. │             IDENTIFIER id: 4, identifier: timestamp                                    │
 8. │       FUNCTION id: 5, alias: maximum_date, function_name: max, function_type: ordinary │
 9. │         ARGUMENTS                                                                      │
10. │           LIST id: 6, nodes: 1                                                         │
11. │             IDENTIFIER id: 7, identifier: timestamp                                    │
12. │   JOIN TREE                                                                            │
13. │     IDENTIFIER id: 8, identifier: session_events                                       │
14. │   SETTINGS allow_experimental_analyzer=1                                               │
    └────────────────────────────────────────────────────────────────────────────────────────┘

14 rows in set. Elapsed: 0.001 sec.
```

## 3. Planner

The planner takes a query tree and builds a query plan out of it. The query tree tells us what we want to do with a specific query, and the query plan tells us how we will do it. Additional optimizations are going to be done as part of the query plan.

```sql
EXPLAIN
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type

Query id: 29732ca7-04e2-493a-b56b-05a0e9b21084

   ┌─explain────────────────────────────────────────────────────────────────────────┐
1. │ Expression ((Project names + Projection))                                      │
2. │   Aggregating                                                                  │
3. │     Expression ((Before GROUP BY + Change column names to column identifiers)) │
4. │       ReadFromMergeTree (default.session_events)                               │
   └────────────────────────────────────────────────────────────────────────────────┘

4 rows in set. Elapsed: 0.006 sec.

-- Add header to the query to know the column's name
EXPLAIN header = 1
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type

Query id: ceefa2cd-21ad-4206-86a2-52103467ce55

    ┌─explain────────────────────────────────────────────────────────────────────────┐
 1. │ Expression ((Project names + Projection))                                      │
 2. │ Header: type String                                                            │
 3. │         minimum_date DateTime                                                  │
 4. │         maximum_date DateTime                                                  │
 5. │         percentage Nullable(Float64)                                           │
 6. │   Aggregating                                                                  │
 7. │   Header: __table1.type String                                                 │
 8. │           min(__table1.timestamp) DateTime                                     │
 9. │           max(__table1.timestamp) DateTime                                     │
10. │           count() UInt64                                                       │
11. │     Expression ((Before GROUP BY + Change column names to column identifiers)) │
12. │     Header: __table1.type String                                               │
13. │             __table1.timestamp DateTime                                        │
14. │       ReadFromMergeTree (default.session_events)                               │
15. │       Header: type String                                                      │
16. │               timestamp DateTime                                               │
    └────────────────────────────────────────────────────────────────────────────────┘

16 rows in set. Elapsed: 0.006 sec.

-- all the actions that need to be executed
EXPLAIN actions = 1
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type

Query id: ca9f2a29-b70e-4441-8d78-498784e48868

    ┌─explain──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 1. │ Expression ((Project names + Projection))                                                                                                                                                                                                        │
 2. │ Actions: INPUT : 0 -> min(__table1.timestamp) DateTime : 0                                                                                                                                                                                       │
 3. │          INPUT : 1 -> max(__table1.timestamp) DateTime : 1                                                                                                                                                                                       │
 4. │          INPUT : 2 -> count() UInt64 : 2                                                                                                                                                                                                         │
 5. │          INPUT : 3 -> __table1.type String : 3                                                                                                                                                                                                   │
 6. │          COLUMN Const(Nullable(UInt64)) -> _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String) Nullable(UInt64) : 4                                                                                                                          │
 7. │          COLUMN Const(UInt8) -> 100_UInt8 UInt8 : 5                                                                                                                                                                                              │
 8. │          ALIAS min(__table1.timestamp) :: 0 -> minimum_date DateTime : 6                                                                                                                                                                         │
 9. │          ALIAS max(__table1.timestamp) :: 1 -> maximum_date DateTime : 0                                                                                                                                                                         │
10. │          ALIAS __table1.type :: 3 -> type String : 1                                                                                                                                                                                             │
11. │          FUNCTION divide(count() :: 2, _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String) :: 4) -> divide(count(), _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String)) Nullable(Float64) : 3                                           │
12. │          FUNCTION multiply(divide(count(), _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String)) :: 3, 100_UInt8 :: 5) -> multiply(divide(count(), _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String)), 100_UInt8) Nullable(Float64) : 4 │
13. │          ALIAS multiply(divide(count(), _CAST(1000_Nullable(UInt64), 'Nullable(UInt64)'_String)), 100_UInt8) :: 4 -> percentage Nullable(Float64) : 5                                                                                            │
14. │ Positions: 1 6 0 5                                                                                                                                                                                                                               │
15. │   Aggregating                                                                                                                                                                                                                                    │
16. │   Keys: __table1.type                                                                                                                                                                                                                            │
17. │   Aggregates:                                                                                                                                                                                                                                    │
18. │       min(__table1.timestamp)                                                                                                                                                                                                                    │
19. │         Function: min(DateTime) → DateTime                                                                                                                                                                                                       │
20. │         Arguments: __table1.timestamp                                                                                                                                                                                                            │
21. │       max(__table1.timestamp)                                                                                                                                                                                                                    │
22. │         Function: max(DateTime) → DateTime                                                                                                                                                                                                       │
23. │         Arguments: __table1.timestamp                                                                                                                                                                                                            │
24. │       count()                                                                                                                                                                                                                                    │
25. │         Function: count() → UInt64                                                                                                                                                                                                               │
26. │         Arguments: none                                                                                                                                                                                                                          │
27. │   Skip merging: 0                                                                                                                                                                                                                                │
28. │     Expression ((Before GROUP BY + Change column names to column identifiers))                                                                                                                                                                   │
29. │     Actions: INPUT : 0 -> type String : 0                                                                                                                                                                                                        │
30. │              INPUT : 1 -> timestamp DateTime : 1                                                                                                                                                                                                 │
31. │              ALIAS type :: 0 -> __table1.type String : 2                                                                                                                                                                                         │
32. │              ALIAS timestamp :: 1 -> __table1.timestamp DateTime : 0                                                                                                                                                                             │
33. │     Positions: 2 0                                                                                                                                                                                                                               │
34. │       ReadFromMergeTree (default.session_events)                                                                                                                                                                                                 │
35. │       ReadType: Default                                                                                                                                                                                                                          │
36. │       Parts: 1                                                                                                                                                                                                                                   │
37. │       Granules: 1                                                                                                                                                                                                                                │
    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

37 rows in set. Elapsed: 0.002 sec.
```

## 4. Query pipeline

A query pipeline is generated from the query plan. The query pipeline is very similar to the query plan, with the difference that it's not a tree but a graph. It highlights how ClickHouse is going to execute a query and what resources are going to be used. Analyzing the query pipeline is very useful to see where the bottleneck is in terms of inputs/outputs.

```sql
EXPLAIN PIPELINE
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type

Query id: 06a53e10-fefd-459b-89b9-531b0f2b5da5

   ┌─explain──────────────────────────────────────────────────────────────────┐
1. │ (Expression)                                                             │
2. │ ExpressionTransform × 16                                                 │
3. │   (Aggregating)                                                          │
4. │   Resize 1 → 16                                                          │
5. │     AggregatingTransform                                                 │
6. │       (Expression)                                                       │
7. │       ExpressionTransform                                                │
8. │         (ReadFromMergeTree)                                              │
9. │         MergeTreeSelect(pool: ReadPoolInOrder, algorithm: InOrder) 0 → 1 │
   └──────────────────────────────────────────────────────────────────────────┘

9 rows in set. Elapsed: 0.003 sec.

-- TSV graph
EXPLAIN PIPELINE graph = 1
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type
FORMAT TSV

Query id: f61c3cbb-d547-4536-88c8-191063826453

digraph
{
  rankdir="LR";
  { node [shape = rect]
    subgraph cluster_0 {
      label ="Expression";
      style=filled;
      color=lightgrey;
      node [style=filled,color=white];
      { rank = same;
        n5 [label="ExpressionTransform × 16"];
      }
    }
    subgraph cluster_1 {
      label ="Expression";
      style=filled;
      color=lightgrey;
      node [style=filled,color=white];
      { rank = same;
        n2 [label="ExpressionTransform"];
      }
    }
    subgraph cluster_2 {
      label ="ReadFromMergeTree";
      style=filled;
      color=lightgrey;
      node [style=filled,color=white];
      { rank = same;
        n1 [label="MergeTreeSelect(pool: ReadPoolInOrder, algorithm: InOrder)"];
      }
    }
    subgraph cluster_3 {
      label ="Aggregating";
      style=filled;
      color=lightgrey;
      node [style=filled,color=white];
      { rank = same;
        n3 [label="AggregatingTransform"];
        n4 [label="Resize"];
      }
    }
  }
  n2 -> n3 [label=""];
  n1 -> n2 [label=""];
  n3 -> n4 [label=""];
  n4 -> n5 [label="× 16"];
}

47 rows in set. Elapsed: 0.006 sec.

-- Disable the compact
EXPLAIN PIPELINE graph = 1, compact = 0
WITH (
        SELECT count(*)
        FROM session_events
    ) AS total_rows
SELECT
    type,
    min(timestamp) AS minimum_date,
    max(timestamp) AS maximum_date,
    (count(*) / total_rows) * 100 AS percentage
FROM session_events
GROUP BY type
FORMAT TSV

Query id: 3af4ea21-5766-4cee-9b17-6b133c6b3acb

digraph
{
  rankdir="LR";
  { node [shape = rect]
    n0[label="MergeTreeSelect(pool: ReadPoolInOrder, algorithm: InOrder)_8"];
    n1[label="ExpressionTransform_9"];
    n2[label="AggregatingTransform_10"];
    n3[label="Resize_11"];
    n4[label="ExpressionTransform_12"];
    n5[label="ExpressionTransform_13"];
    n6[label="ExpressionTransform_14"];
    n7[label="ExpressionTransform_15"];
    n8[label="ExpressionTransform_16"];
    n9[label="ExpressionTransform_17"];
    n10[label="ExpressionTransform_18"];
    n11[label="ExpressionTransform_19"];
    n12[label="ExpressionTransform_20"];
    n13[label="ExpressionTransform_21"];
    n14[label="ExpressionTransform_22"];
    n15[label="ExpressionTransform_23"];
    n16[label="ExpressionTransform_24"];
    n17[label="ExpressionTransform_25"];
    n18[label="ExpressionTransform_26"];
    n19[label="ExpressionTransform_27"];
  }
  n0 -> n1;
  n1 -> n2;
  n2 -> n3;
  n3 -> n4;
  n3 -> n5;
  n3 -> n6;
  n3 -> n7;
  n3 -> n8;
  n3 -> n9;
  n3 -> n10;
  n3 -> n11;
  n3 -> n12;
  n3 -> n13;
  n3 -> n14;
  n3 -> n15;
  n3 -> n16;
  n3 -> n17;
  n3 -> n18;
  n3 -> n19;
}

45 rows in set. Elapsed: 0.003 sec.
```

Why does ClickHouse not read from the table using multiple threads? Let's try to add more data to our table:

```sql
INSERT INTO session_events SELECT * FROM generateRandom('clientId UUID,
   sessionId UUID,
   pageId UUID,
   timestamp DateTime,
   type Enum(\'type1\', \'type2\')', 1, 10, 2) LIMIT 1000000;
```

Run the explain again:

```sql
digraph
{
  rankdir="LR";
  { node [shape = rect]
    n0[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_8"];
    n1[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_9"];
    n2[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_10"];
    n3[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_11"];
    n4[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_12"];
    n5[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_13"];
    n6[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_14"];
    n7[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_15"];
    n8[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_16"];
    n9[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_17"];
    n10[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_18"];
    n11[label="MergeTreeSelect(pool: ReadPool, algorithm: Thread)_19"];
    n12[label="ExpressionTransform_20"];
    n13[label="ExpressionTransform_21"];
    n14[label="ExpressionTransform_22"];
    n15[label="ExpressionTransform_23"];
    n16[label="ExpressionTransform_24"];
    n17[label="ExpressionTransform_25"];
    n18[label="ExpressionTransform_26"];
    n19[label="ExpressionTransform_27"];
    n20[label="ExpressionTransform_28"];
    n21[label="ExpressionTransform_29"];
    n22[label="ExpressionTransform_30"];
    n23[label="ExpressionTransform_31"];
    n24[label="AggregatingTransform_32"];
    n25[label="AggregatingTransform_33"];
    n26[label="AggregatingTransform_34"];
    n27[label="AggregatingTransform_35"];
    n28[label="AggregatingTransform_36"];
    n29[label="AggregatingTransform_37"];
    n30[label="AggregatingTransform_38"];
    n31[label="AggregatingTransform_39"];
    n32[label="AggregatingTransform_40"];
    n33[label="AggregatingTransform_41"];
    n34[label="AggregatingTransform_42"];
    n35[label="AggregatingTransform_43"];
    n36[label="Resize_44"];
    n37[label="ExpressionTransform_45"];
    n38[label="ExpressionTransform_46"];
    n39[label="ExpressionTransform_47"];
    n40[label="ExpressionTransform_48"];
    n41[label="ExpressionTransform_49"];
    n42[label="ExpressionTransform_50"];
    n43[label="ExpressionTransform_51"];
    n44[label="ExpressionTransform_52"];
    n45[label="ExpressionTransform_53"];
    n46[label="ExpressionTransform_54"];
    n47[label="ExpressionTransform_55"];
    n48[label="ExpressionTransform_56"];
    n49[label="ExpressionTransform_57"];
    n50[label="ExpressionTransform_58"];
    n51[label="ExpressionTransform_59"];
    n52[label="ExpressionTransform_60"];
  }
  n0 -> n12;
  n1 -> n13;
  n2 -> n14;
  n3 -> n15;
  n4 -> n16;
  n5 -> n17;
  n6 -> n18;
  n7 -> n19;
  n8 -> n20;
  n9 -> n21;
  n10 -> n22;
  n11 -> n23;
  n12 -> n24;
  n13 -> n25;
  n14 -> n26;
  n15 -> n27;
  n16 -> n28;
  n17 -> n29;
  n18 -> n30;
  n19 -> n31;
  n20 -> n32;
  n21 -> n33;
  n22 -> n34;
  n23 -> n35;
  n24 -> n36;
  n25 -> n36;
  n26 -> n36;
  n27 -> n36;
  n28 -> n36;
  n29 -> n36;
  n30 -> n36;
  n31 -> n36;
  n32 -> n36;
  n33 -> n36;
  n34 -> n36;
  n35 -> n36;
  n36 -> n37;
  n36 -> n38;
  n36 -> n39;
  n36 -> n40;
  n36 -> n41;
  n36 -> n42;
  n36 -> n43;
  n36 -> n44;
  n36 -> n45;
  n36 -> n46;
  n36 -> n47;
  n36 -> n48;
  n36 -> n49;
  n36 -> n50;
  n36 -> n51;
  n36 -> n52;
}
```

So the executor decided not to parallelize operations because the volume of data wasn't high enough. By adding more rows, the executor then decided to use multiple threads as shown in the graph.

## 5. Executor

Finally the last step of the query execution is done by the executor. It will take the query pipeline and execute it. There are different types of executors, depending if you're doing a `SELECT`, an `INSERT`, or an `INSERT SELECT`.
