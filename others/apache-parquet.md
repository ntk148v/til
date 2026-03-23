# Aapache Parquet

Source:

- <https://parquet.apache.org/>
- <https://www.ibm.com/think/topics/parquet>

## 1. What is Apache Parquet?

Columnar storage format that addresses big data processing challenges. Unlike traditional row-based storage, it organizes data into columns. This structure allows you to read only the necessary columns, making data queries faster and reducing resource consumption.

Features:

- Columnar storage:
  - Parquet files are split into row groups, which hold a batch of rows. Each row group is broken into column chunks, each containing data for one column. These chunks are further divided into smaller pieces called pages, which are compressed to save space.
    - Row groups: A row group contains multiple rows but stores data column-wise for efficient reading.
    - Column chunks:
      - Within each row group, data is separated by columns.
      - This design allows columnar pruning, where we can read only the relevant columns instead of scanning the entire file.
    - Pages:
      - Each column chunk is further split into pages to optimize memory usage.
      - Pages are typically compressed, reducing storage costs.
  - Parquet files store extra information in the footer, called metadata, which locates and reads only the data we need.
    - Footer (metadata)
      - The footer at the end of a Parquet file stores index information:
      - Schema: Defines data types and column names.
      - Row group offsets: Helps locate specific data quickly.
      - Statistics: Min/max values to enable predicate pushdown (filtering at the storage level).

  ![](https://media.datacamp.com/cms/ad_4nxcuuincavq5rqwc42rsxrqtf_hrepxa5zaohmvbkyjdivivu2p79s8pkbiov5ws85byacezrthjzpkg_uk-b1gybmog8fszuf_edkdle1j36eixnmhqb7unprq4emw4phm__zrp.png)

- Compression and encoding: Parquet compresses data column by column using compression methods like Snappy and Gzip. It also uses two encoding techniques:
  - Run-length encoding to store repeated values compactly.
  - Dictionary encoding to replace duplicates with dictionary references.

- Schema evolution means modifying the structure of datasets, such as adding or altering columns. It may sound simple, but depending on how your data is stored, modifying the schema can be slow and resource-intensive.
  - With Parquet, you can add, remove, or update fields without breaking your existing files.
  - Parquet stores schema information inside the file footer (metadata), allowing for evolving schemas without modifying existing files.
    - When you add a new column, existing Parquet files remain unchanged.
    - New files will include the additional column, while old files still follow the previous schema.
    - Removing a column doesn’t require reprocessing previous data; queries will ignore the missing column.
    - If a column doesn’t exist in an older file, Parquet engines (like Apache Spark, Hive, or BigQuery) return NULL instead of breaking the query.
    - Older Parquet files can be read even after schema modifications.
    - Newer Parquet files with additional columns can still be read by systems expecting an older schema.

## 2. How Apache Parquet works?

Apache Parquet systematically transforms raw data into an optimized columnar format, significantly improving both storage efficiency and query performance.

Here's how Parquet processes data:

1. Data organization: When writing data to a Parquet file, the format first divides the data into row groups. Each row group represents an independent unit of the dataset, enabling parallel processing and efficient memory management for large-scale operations. This partitioning strategy forms the foundation for Parquet's high-performance data access.
2. Column chunking: Within each row group, Parquet's assembly algorithm reorganizes data by column rather than row. Similar data types are grouped into column chunks, enabling specialized encoding based on the data's characteristics. For example, a column of dates can be optimized differently than a column of numerical values.
3. Compression and encoding: Parquet applies a two-stage optimization process. First, it uses encoding schemes such as run-length encoding (RLE) to efficiently represent repeated values—particularly valuable for columns with many duplicate entries. Then, it applies compression algorithms such as Snappy or Gzip to further reduce storage requirements.
4. Metadata generation: The format creates comprehensive metadata—including file schema and data types, statistics for each column, row group locations and structure. This metadata helps enable efficient query planning and optimization.
5. Query execution: When reading Parquet data, query engines first consult metadata to identify relevant columns. Only necessary column chunks are read from storage, and data is decompressed and decoded as needed.
