# OpenStack Magnum

## What is Magnum?

* Magnum is an OpenStack service developed by the OpenStack Containers Team making Container orchestration engine (COE) such as Kubernetes, Docker Swarm & Apache Mesos available as the 1st class resources in OpenStack.
* Use Heat to orchestrate an OS image which contains Docker and COE and runs that image in either virtual machines or bare metal in a cluster configuration.

## Main concepts.

### ClusterTemplate (BayModel)

* A collection of parameters to describe how a cluster can be constructed. Some parameters are relevant to the insfrastructure of the cluster, while others are for the particular COE.

### Cluster (Bay)

* An instance of the ClusterTemplate of a COE. Magnum deploys a cluster by referring to the attributes defined in the particular ClusterTemplate as well as a few additional parameters for the cluster.

## COE

### Kubernetes

```
# Must upload coreos/fedora-atomic images before (os_distro)

openstack coe cluster template create k8s-cluster-template \
                        --image coreos \
                        --keypair controller21 \
                        --external-network mgnt-net \
                        --flavor m1.mini2 \
                        --docker-volume-size 5 \
                        --network-driver flannel \
                        --coe kubernetes

openstack coe cluster create k8s-cluster-template \
            --cluster-template k8s-cluster-template \
            --master-count 3 \
            --node-count 8
```
