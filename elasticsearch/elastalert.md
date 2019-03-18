# ElastAlert

## Overview

* A simple framework for alerting on anomalies, spikes, or other patterns of interest from data in Elasticsearch.
* ElastAlert has three main components that may be imported as a module or customized: rule types, alerts and enhancements.

* Rule types is responsible for processing the data returned from Elasticsearch.
  * “Match where there are X events in Y time” (`frequency` type)
  * “Match when the rate of events increases or decreases” (`spike` type)
  * “Match when there are less than X events in Y time” (`flatline` type)
  * aer“Match when a certain field matches a blacklist/whitelist” (`blacklist`and `whitelist` type)
  * “Match on any event matching a given filter” (`any` type)
  * “Match when a field has two different values within some time” (`change`type)
* Alerts are responsible for taking action based on a match (a dictionary containing values from a document in Elasticsearch, but may contain arbitrary data added by the rule type).
* Enhancements are a way of intercepting an alert and modifying or enhancing it in some way. 

## Running ElastAlert

[Follow this](<https://elastalert.readthedocs.io/en/latest/running_elastalert.html>)

ElastAlert saves information and metadata about its queries and its alerts back to Elasticsearch. This is useful for auditing, debugging, and it allows ElastAlert to restart and resume exactly where it left off. This is not required for ElastAlert to run, but highly recommended. we need to create an index for ElastAlert to write to by running `elastalert-create-index` and following the instructions