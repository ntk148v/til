# We also have to unset other variables that might impact LC_ALL
# taking effect.
unset LANG
unset LANGUAGE
LC_ALL=en_US.utf8
export LC_ALL

# Make sure umask is sane
umask 022

# Save trace setting
XTRACE=$(set +o | grep xtrace)
set -o xtrace

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

#
# Working with Service
#
# check the status of the service kube-proxy
systemctl status kube-proxy.service / docker ps
# Creating a service for a pod
kubectl run nginx-pod --image=nginx --port=80 --port=80 \
    --restart="Never" --labels="app=nginx"
kubectl expose pod nginx-pod --port=8000 --target-port=80 \
    --name="service-pod"
kubectl get svc service-pod
# Creating a service for the replication controller and adding an external IP
# kubectl run nginx-rc --image=nginx --port=80 --replicas=2
kubectl expose deployment nginx-deployment --name="service-deployment" \
    --external-ip="<USER_SPECIFIED_IP>"
kubectl get svc service-deployment
kubectl describe svc service-deployment
# Creating a no-selector service for an endpoint
# create an nginx server on another instance with IP address
docker run -d -p 80:80 nginx
docker ps
cat templates/nginx-ep.json
kubectl create -f templates/nginx-ep.json
kubectl get ep service-foreign-ep
cat templates/service-ep.json
kubectl create -f templates/service-ep.json
kubectl describe svc service-foreign-ep

#
# Working with label & selector
#
kubectl create -f templates/staging-nginx.yaml
kubectl describe pod nginx
kubectl run nginx-prod --image=nginx --replicas=2 --port=80 \
    --labels="environment=production,project=pilot,tier=frontend"
kubectl get pods
kubectl get pods -l "project=pilot,environment=production"

# Linking service with a replication controller/deployment by using label selectors


# Restore xtrace
$XTRACE
