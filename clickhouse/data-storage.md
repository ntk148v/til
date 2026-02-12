# Data storage

> [!note]
> use [Amazon Customer Reviewer](https://clickhouse.com/docs/getting-started/example-datasets/amazon-reviews) dataset.

Loading the dataset:

```sql
SELECT *
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_2015.snappy.parquet')
LIMIT 3;

CREATE DATABASE amazon;

CREATE TABLE amazon.amazon_reviews
(
    `review_date` Date,
    `marketplace` LowCardinality(String),
    `customer_id` UInt64,
    `review_id` String,
    `product_id` String,
    `product_parent` UInt64,
    `product_title` String,
    `product_category` LowCardinality(String),
    `star_rating` UInt8,
    `helpful_votes` UInt32,
    `total_votes` UInt32,
    `vine` Bool,
    `verified_purchase` Bool,
    `review_headline` String,
    `review_body` String,
    PROJECTION helpful_votes
    (
        SELECT *
        ORDER BY helpful_votes
    )
)
ENGINE = MergeTree
ORDER BY (review_date, product_category);

INSERT INTO amazon.amazon_reviews SELECT * FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/amazon_reviews/amazon_reviews_*.snappy.parquet');

DESCRIBE TABLE amazon.amazon_reviews;
```
