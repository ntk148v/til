# OpenStack Vitrage

**Root Cause Analysis service** for:
* Organizing OpenStack alarms & events.
* Analyzing them.
* Expanding the knowledge based on alarm & events.

## High Level Architecture

![high-level-architecture](https://docs.openstack.org/vitrage/latest/_images/vitrage_graph_architecture.png)

* **Data Sources**: import information from different sources, regarding the state of the system.
* **Graph**: Holds the information collected by the Data Sources, as well as their their inter-relations.
* **Evaluator**: cooradiantes the analysis of changes to the Graph and processes the results of this analysis.
* **Notifiers**: notify external systems of Vitrage alarms and states.

## Templates Format & Usage

* YAML

### General template structure

```yaml
# Contains general information about the template
metadata:
  version: <template version>
  name: <unique template identifier>
  type: <one of: standard, definition, equivalence>
  description: <what this template does>
# Contains the atomic definitions referenced later on, for entities and relationships
# **mandatory** unless an include section is specified.
definitions:
  # describe the resources and alarms which are relevant to the template scenario
  entities:
    - entity: ...
    - entity: ...
  # the relationships between the entities.
  relationships:
    - relationship: ...
    - relationship: ...
# Containts a list of names of definition templates
# **optional**
includes:
  - name: <name as stated in the metadata of a definition template>
  - name: ...
# A list of if-then scenarios to consider
scenarios:
  - scenario:
    # the condition to be met
    condition: <if statement true do the action>
    # a list of actions to execute when the condition is met
    actions:
      - action: ...
```

### Definition template structure

* There are separate files, which containts only definitions and can be included under the includes section in regular section.
* YAML.
* Same format as a regular template, except it **does not** contain a scenarios or an include section.

### [Usage](https://docs.openstack.org/vitrage/latest/contributor/vitrage-template-format.html#usage)

### Common parameters and acceptable values - for writing templates

Here is the update & more complete version of Common parameters section in [Usage](https://docs.openstack.org/vitrage/latest/contributor/vitrage-template-format.html#usage)

| block             | key         | supported values                                                                                                                                                                                                      | comments                                                                                                                                                    |
| ----------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| entity            | category    | ALARM/RESOURCE(choose one)                                                                                                                                                                                            | no comment                                                                                                                                                  |
| entity (ALARM)    | type        | any string                                                                                                                                                                                                            | no comment                                                                                                                                                  |
| entity (RESOURCE) | type        | aodh, ceilometer, openstack.cluster, collectd, doctor, heat.stack, kubernetes, nagios, neutron.port, prometheus, static, static_physical, neutron.network, nova.zone, nova.host, nova.instance, cinder.volume, zabbix | These are for the datasources that come with vitrage by default. Adding datasources will add more supported types, as defined in the datasource transformer |
| action            | action_type | raise_alarm, set_state, add_causal_relationship, mark_down, execute_mistral                                                                                                                                           | no comment                                                                                                                                                  |
More details

* Action:
    * `set_state`: Set (deduced) state.
    * `raise_alarm`: Raise a Vitrage (deduced) alarm.
    * `mark_down`: Mark a host as down.
    * `execute_mistral`: Execute a Mistral workflow.
    * `add_causal_relationship`: Connect two alarms in the graph to indicate one cause other (RCA).

* Relationship type:
    * `on`
    * `contains`
    * `causes`
    * `attached`
    * `attached_public`
    * `attached_private`
    * `connect`
    * `managed_by`
    * `comprised`
