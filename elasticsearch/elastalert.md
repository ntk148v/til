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

## Rule Types

### Frequency

The rule matches when there are at least a certain number of events of a given time frame.

* `num_events`: the number of events which will trigger an alert, inclusive.
* `timeframe`: the time that `num_events` must occur within.
* `use_count_query`: if true, ElastAlert will poll Elasticsearch using the count api and not download all of the matching documents.
* `doc_type`: specify the `_type` of document to search for. This must be present if `use_count_query` or `use_terms_query` is set.
* `use_terms_query`: if true, ElastAlert will make an aggregation query against Elasticsearch to get counts of documents matching each unique value of `query_key`.
* `term_size`: when used with `use_terms_query`, this is the maximum number of terms returned per query.
* `query_key`: counts of documents will be stored independently for each value of `query_key`.

### Spike

The rule matches when the volume of events during a given time period is `spike_height` times larger or smaller than durring the previous time period.

* `spike_height`: the ratio of number of events in the last `timeframe` to the previous `timeframe` that when hit will trigger an alert.
* `spike_type`: up, down or both.

```
# Up
num_of_events_cur_timeframe >= spike_height * number_of_events_ref_timeframe
# Down
num_of_events_cur_timeframe < spike_height * number_of_events_ref_timeframe
```

* `timeframe`: average out the rate of events over this time period.
* `field_value`: when set, uses the value of the field in the documnet and not the number of matching documents.
* `threshold_ref`: the minimum number of events that must exist in the reference window for an alert to trigger.
* `threshold_cur`: the minimum number of events that must exist in the current window for an alert to trigger.

```
threshold_ref: 10
spike_height: 3
-> _ref >= 10 <-> _cur >= _ref * spike_height
threshold_cur: 30
spike_height: 3
-> the same...
```
