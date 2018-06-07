# Autoscaling with OpenStack Heat

## Ref articles:

* [IBM Bluebox support - Using Heat for autoscaling](https://ibm-blue-box-help.github.io/help-documentation/heat/autoscaling-with-heat/)
* [Cloudify - Autoscaling your Apps with OpenStack Heat](https://cloudify.co/2015/05/20/openstack-summit-vancouver-cloud-network-orchestration-automation-heat-scaling.html)
* [RedHat OpenStack - Auto Scaling for Instances](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/11/pdf/auto_scaling_for_instances/Red_Hat_OpenStack_Platform-11-Auto_Scaling_for_Instances-en-US.pdf)
* [Keith Tenzer - Auto Scaling Instances with OpenStack](https://keithtenzer.com/2015/09/02/auto-scaling-instances-with-openstack)
* [Rackspace - OpenStack Orchestration In Depth, Part IV: Scaling](https://developer.rackspace.com/blog/openstack-orchestration-in-depth-part-4-scaling/)

## Resource types:

### OS::Heat::AutoScalingGroup

An autoscaling group that can scale arbitrary resources.

An autoscaling group allows the creation of a desired count of similar resources, which are defined with the resource property in HOT format. If there is a need to create many of the same resources (e.g one hundred sets of Server, WaitCondition and WaitConditionHandle or even Neutron Nets), AutoScalingGroup is a convenient and easy way to do that.

An AutoScalingGroup is a resource type that is used to encapsulate the resource that we wish to scale, and some properties related to the scale process.

```
# Required Properties
max_size:
    # Maximum number of resources in the group
    # Integer value expected
    # Can be updated without replacement
    # The value must be at least 0
min_size:
    # Minimum number of resources in the group
    # Integer value expected
    # Can be updated without replacement
    # The value must be at least 0
resource:
    # Resource definition for the resources in the group.
```

### OS::Heat::ScalingPolicy

A ScalingPolicy is a resource type that is used to define the effect a scale process will have on the scaled resource.

A resource to manage scaling of OS::Heat::AutoScalingGroup, i.e. define which metric should be scaled and scaling adjustment, set cooldown.

```
# Required Properties

adjustment_type:
    # Type of adjustment
    # String value expected
    # Can be updated without replacement
    # Allowed values: change_in_capacity, exact_capacity, percent_change_in_capacity.
auto_scaling_group_id:
    # AutoScalingGroup ID to apply policy to.
    # String value expected
    # Updated cause replacement
scaling_adjustment
    # Size of adjustment
    # Number value expected
    # Can be updated without replacement
```
### OS::Aodh::GnocchiAggregationByMetricsAlarm

A resource that implements alarm with specified metrics, allows to use specified by user metrics in metrics list.

```
# Required Properties
metrics:
    # A list of metric ids
    # List value expected
    # Can be updated without replacement
threshold:
    # Threshold to evaluate against
    # Number value expected
    # Can be updated without replacement
```


