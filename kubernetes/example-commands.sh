#
# Working with pods example
#

# Check nginx-centos-pod
cat templates/nginx-centos-pod.yaml
# Lauch nginx-centos-pod
kubectl create -f templates/nginx-centos-pod.yaml
# Check pods status
kubectl get pods
kubectl get po # it also supports shorthand format as "po"
# Describe pod
kubectl describe pods nginx-centos-pod
# Check logs
kubectl logs nginx-centos-pod -c centos-1 --tail=30
# Check docker containers
docker ps
# 3 containers - CentOS, nginx & pause - are running instead of 2. Because
# each pod we need to keep belongs to a particular Linux namespace, if both
# the CentOS and nginx containers die, the namespace will be destroyed.
#
# https://stackoverflow.com/questions/33472741/what-work-does-the-process-in-container-gcr-io-google-containers-pause0-8-0-d
#
# In Kubernetes, each pod has an IP and within a pod there exists a so called
# infrastructure container, which is the first container that the Kubelet
# instantiates and it acquires the pod’s IP and sets up the network namespace.
# All the other containers in the pod then join the infra container’s network
# and IPC namespace. The infra container has network bridge mode enabled and all
# the other containers in the pod share its namespace via container mode. The
# initial process that runs in the infra container does effectively nothing
# since its sole purpose is to act as the home for the namespaces.


#
# Working with Deployment and ReplicaSet
#

kubectl create -f templates/nginx-deployment.yaml
kubectl get po
kubectl get deployment
