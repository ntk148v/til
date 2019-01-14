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
  type: <one of: standard, definition, equivalence> # Don't know what is difference between these type.
  description: <what this template does>
# Contains the atomic definitions referenced later on, for entities and relationships
# **mandatory** unless an include section is specified.
# Condition building-blocks
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
# Action defined based on the building blocks
scenarios:
  - scenario:
    # the condition to be met
    # condition can be relationship or template_id!
    condition: <if statement true do the action>
    # a list of actions to execute when the condition is met
    actions:
      - action: ...
```

* Example:

```yaml
metadata:
  version: 2
  type: standard
  name: raise_alarm_for_host_errors
  description: host in error raises alarm
definitions:
  entities:
    - entity:
        category: RESOURCE
        type: nova.host
        state: ERROR
        template_id: host_in_error
scenarios:
  scenario:
    condition: host_in_error  # uses template_id
    actions:
      - action:
          type: raise_alarm
          target:
            target: host_in_error # uses template_ids
            properties:
              alarm_type: host_malfunctioning   # any string
              severity: critical
```

### Definition template structure

* There are separate files, which containts only definitions and can be included under the includes section in regular section.
* YAML.
* Same format as a regular template, except it **does not** contain a scenarios or an include section.

### [Usage](https://docs.openstack.org/vitrage/latest/contributor/vitrage-template-format.html#usage)

### Common parameters and acceptable values - for writing templates

Here is the update & more complete version of Common parameters section in [Usage](https://docs.openstack.org/vitrage/latest/contributor/vitrage-template-format.html#usage)

| block             | key                 | supported values                                                                                                                                                                                                      | comments                                                                                                                                                    |
| ----------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| entity            | category            | ALARM/RESOURCE(choose one)                                                                                                                                                                                            | no comment                                                                                                                                                  |
| entity (ALARM)    | type                | any string                                                                                                                                                                                                            | no comment                                                                                                                                                  |
| entity (RESOURCE) | type                | aodh, ceilometer, openstack.cluster, collectd, doctor, heat.stack, kubernetes, nagios, neutron.port, prometheus, static, static_physical, neutron.network, nova.zone, nova.host, nova.instance, cinder.volume, zabbix | These are for the datasources that come with vitrage by default. Adding datasources will add more supported types, as defined in the datasource transformer |
| action            | action_type         | raise_alarm, set_state, add_causal_relationship, mark_down, execute_mistral                                                                                                                                           | no comment                                                                                                                                                  |
| relationship      | relationship_type   | comprised,on,contains,attached,attached_public,attached_private,connected                                                                                                                                             | no comment                                                                                                                                                  |
| metadata          | type                | standard,equivalence,definition                                                                                                                                                                                       | no comment                                                                                                                                                  |
| action            | properties/state    | N/A,OK,TRANSIENT,SUBOPTIMAL,ERROR,DELETED                                                                                                                                                                             | no comment                                                                                                                                                  |
| action            | properties/severity | CRITICAL,SEVERE,WARNING,N/A,OK                                                                                                                                                                                        | no comment                                                                                                                                                  |

* Action:
    * `set_state`: Set state of specified entity. This will directly affect the state as seen in Vitrage, but will not impact the state at the relevant datasource of this entity.

    ```yaml
    actions:
      - action:
          action_type: set_state
          action_target:
            target: nova_host # A template id of resource nova.host
          properties:
            state: SUBOPTIMAL
    ```

    * `raise_alarm`: Raise a Vitrage (deduced) alarm on a target entity.

    ```yaml
    actions:
      - action:
          action_type: raise_alarm
          action_target:
            target: nova_host # A template id of resource nova.host
          properties:
            alarm_name: HostNayBiLoiNe
            severity: critical
    ```

    * `mark_down`: Set an entity marked_down field. This can be used along with nova notifier to call force_down for a  host.

    ```yaml
    action:
     action_type : mark_down
         action_target:
             target: host # mandatory. entity (from the definitions section, only host) to be marked as down
    ```

    * `execute_mistral`: Execute a Mistral workflow. If the Mistral notifier is used, the specified workflow will be executed with its parameters.

    ```yaml
    actions:
      - action:
          action_type: execute_mistral
          properties:
            workflow: demo_wf # The name or id of created Mistral workflow
            input:
              host_name: host-name-ne
    ```

    * `add_causal_relationship`: Add a causual relationship between alarms. Connect two alarms in the graph to indicate one cause other (RCA).

    ```yaml
    actions:
      - action:
          action_type: add_causal_relationship
          action_target:
            source: alarm1
            source: alarm2
    ```

* Relationship type:
    * `on`: common case - alarm *on* resource.

    ```yaml
    relationships:
      - relationship:
          source: alarm1
          target: host
          relationship_type: on
          template_id: alarm_on_host
    ```

    * `contains`: common case - resource A that contains other resources, for example, nova.host resource will contain nova.instance resource.

    ```yaml
    relationships:
      - relationship:
          source: host
          target: instance
          relationship_type: contains
          template_id: host_contains_instance
    ```

    * `causes`: no example, no clue (update later after dive into code)
    * `attached`: common case - volume is attached to an instance. static switch that is attached to a router. The Switch is attached a Host that contains a Vm.

    ```yaml
    relationships:
      - relationship:
         source: volume1
         relationship_type: attached
         target: instance1
         template_id : volume_attached_instance1
    ```

    * `attached_public`: same as `caused`.
    * `attached_private`: same as `caused`.
    * `connect`: common case - Check if there is any edges between two resources.
    * `managed_by`: same as `caused`.
    * `comprised`: common case - Heat stack comprises an instance, K8s cluster comprises host. (comprised != contains? -> not know yet).

    ```yaml
     relationships:
      - relationship:
         source: heat_stack
         relationship_type: comprised
         target: instance
         template_id : heat_comprised_instance
      - relationship:
         source: k8s_cluster
         relationship_type: comprised
         target: host
         template_id : k8s_cluster_comprised_host
    ```

### Useful information you should know

* `get_attr`: This function retrieves the value of an attribute of an entity that is defined in the template. It is supported only for `execute_mistral` action.

```yaml
scenario:
  condition: alarm_on_host_1
  actions:
    action:
      action_type: execute_mistral
      properties:
        workflow: demo_workflow
        input:
          host_name: get_attr(host_1,name)
          retries: 5
```

* Condition Format: The condition which needs to be met will be phrased using the entities and relationships previously defined. An expression is either a single entity, or some logical combination of relationships. Expression can be combined using the following logical operators:
    * “and” - indicates both expressions must be satisfied in order for the condition to be met.
    * “or” - indicates at least one expression must be satisfied in order for the condition to be met (non-exclusive or).
    * “not” - indicates that the expression must not be satisfied in order for the condition to be met.
    * parentheses “()” - clause indicating the scope of an expression.
