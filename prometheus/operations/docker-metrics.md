# Collect Docker metrics with Prometheus

## Option 1: cAdvisor

- [Monitoring cAdvisor with Prometheus](https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md)

## Option 2: Docker daemon itself

- While people generally know (and agree) that cAdvisor is the guy in the room to keep track of container metrics, there's a sort of hidden feature of the docker daemon that people don't take into account: the daemon by itself can be monitored too - see [Collect Docker metrics with Prometheus](https://docs.docker.com/config/thirdparty/prometheus/).
- [Ops.tips article](https://ops.tips/gists/how-to-collect-docker-daemon-metrics/)
