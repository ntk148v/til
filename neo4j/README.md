# Neo4j

Source:

- <https://neo4j.com/docs/getting-started>

## 1. Overview

- Graph Database: a database used to model the data in form of graph.
  - A graph is a pictorial representation of a set of objects where some pairs of objects are connected by links. It is composed of two elements - nodes (vertices) and relationships (edges).

| RDBMS            | Graph Database            |
| ---------------- | ------------------------- |
| Tables           | Graphs                    |
| Rows             | Nodes                     |
| Columns and Data | Properties and its values |
| Constraints      | Relationships             |
| Joins            | Traversal                 |

- Neo4j uses a _property graph_ database.
  - The model represents data in Nodes, Relationships and Properties
  - Properties are key-value pairs
  - Nodes are represented using circle and Relationships are represented using arrow keys
  - Relationships have directions: Unidirectional and Bidirectional
  - Each Relationship contains "Start Node" or "From Node" and "To Node" or "End Node"
  - Both Nodes and Relationships contain properties
  - Relationships connects nodes

![](https://www.tutorialspoint.com/neo4j/images/property_graph.jpg)

- Neo4j uses Native GPE (Graph Processing Engine) to work with its Native graph storage format.
- Concepts:

  - **Node**: represents entity (discrete object) of a domain. Node can have labels (Labels shape the domain by grouping (classifying) nodes into sets where all nodes with a certain label belong to the same set).

  ![](https://neo4j.com/docs/getting-started/current/_images/graph_single_node.svg)

  - **Relationship**:
    - Connects a source code and a target node.
    - Has a direction.
    - Must have a type.
    - It is possible for a node to have a relationship to itself.
    - Can have properties (key-value pairs).

  ![](https://neo4j.com/docs/getting-started/current/_images/graph_example_relationship.svg)

  - **Properties**: key-value pairs that are used for storing data on nodes and relationships.
  - **Traversals and paths**: a traversal is how you query a graph in order to find answers to question.
  - **Schema**: refer to indexes and constrains (optional).

- Naming convention.

| Graph entity      | Recommended style                                       | Example       |
| ----------------- | ------------------------------------------------------- | ------------- |
| Node label        | Camel case, beginning with an upper-case character      | :VehicleOwner |
| Relationship type | Upper case, using underscore to separate words          | :OWNS_VEHICLE |
| Property          | Lower camel case, beginning with a lower-case character | firstName     |

## 2. Setup

Checkout [Neo4j documentation](https://neo4j.com/docs/operations-manual/current/installation/).

```yaml
version: "3"
services:
  neo4j:
    image: neo4j:4.4
    container_name: neo4j
    ports:
      - "7474:7474"
      - "7473:7473"
      - "7687:7687"
    volumes:
      - "neo4j_data:/data"
      - "neo4j_logs:/logs"
volumes:
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local
  neo4j_conf:
    driver: local
```

## 3. CQL
