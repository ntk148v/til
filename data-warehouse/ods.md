# Operational Data Store

Source: <https://www.techtarget.com/searchoracle/definition/operational-data-store>

## 1. What is Operational Data Store (ODS)?

- An ODS is a type of database that's often used as an interim logical area of a data warehouse.
- ODS is designed to integrate data from multiple sources for lightweight data processing activities such as operational reporting and real-time analysis.
- ODS is commonly used in Online Transaction Processing application, which invovle processing transactional data.

## 2. How does ODS work?

![](https://cdn.ttgtmedia.com/rms/onlineimages/how_ods_works-f.png)

- They way ODS work is comparable to the extract, transfrom and load (ETL) process. ODS systems import raw data from production systems and store it in its original form.
- In the ETL process, data is extracted from target sources, transformed and loaded to its destination. In the ODS process, data is not transformed, but rather it's presented as is to business intelligence (BI) applications for analysis and operational decision-making.
- As ODS ingests data, new incoming data overwrites existing data.

## 3. How are operational data stores used?

- An ODS pulls data from multple transactional systems for operational reporting and business reporting.
- ODS is also useful for troubleshooting integration issues with data when they occur. They can compare recent versions of data to copies on other systems to determine if there is a continuity error.
- ODS lends themselves to easy systems integration. Administrator can program rules into an ODS that synchronize data across multiple systems. When it changes on one system, it can trigger change on another system.
- ODS can also facilitate a real-time data stream from data sources into data pipeline.
