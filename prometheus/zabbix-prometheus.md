# Zabbix & Prometheus Comprasion

1. Zabbix.

- Has core written in C and  webUI based on PHP.
- Classic-monitoring.
- Use agents. Zabbix by default uses "pull" model when a server connects to
  agents on each monitoring machine, agents periodically gather the info and
  send it to a server. Alternative is "active checks" mode when agents
  establish connection with a server and send data to it when it need.
- Stores data in RDBMS.
- Uses its own WebUI.
- Has supported alerting in its core.
- Simple to set up.
- Decent performance for up to 10000 nodes. Refer [this article](http://offlinewallet.net/zabbix-vs-prometheus/),
  but I couldn't find any other refers about it.

2. Prometheus.

- Written in Go.
- Prometheus prefers "pull" model when a server gather info from client
  machines. But Prometheus Push Gateway may be used in cases when "push" model
  is needed.
- Requires an application to be instrumented with Prometheus client library
  for preparing metrics. But for monitoring software or system that can't be
  instrusmented, there is an official [blackbox\_exporter](https://github.com/prometheus/blackbox_exporter)
  that allows probing endpoints over a range of protocols; additionally, a
  wide spraed of [3rd party exporters](https://prometheus.io/docs/instrumenting/exporters/)
  and tools are available to help expose metrics for Prometheus.
- Uses its own database embedded into backend process with new format of
  query. [Prometheus time series database comprasion with others](https://prometheus.io/docs/introduction/comparison/).
- Prometheus offers basic tool for exploring gathered data and visualizing it
  in simple graphs on its native server and also offers a minimal dashboard
  builder PromDash. It is also designed to be supported by modern visualizing
  tools like Grafana.
- Alerting - Alertmanager application.
- Takes more time to set up due to requiring manual file editing and
  integration with other tools.
- Faster and more stable even on a large network.
- Recommended for Cloud, Saas and OpenStack monitoring.
