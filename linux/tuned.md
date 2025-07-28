# TuneD

Soruce:

- <https://documentation.ubuntu.com/server/explanation/performance/perf-tune-tuned/>
- <https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/performance_tuning_guide/chap-red_hat_enterprise_linux-performance_tuning_guide-tuned>

TuneD\*1 is a service used to tune your system and optimise the performance under certain workloads. At the core of TuneD are profiles, which tune your system for different use cases. TuneD is distributed with a number of predefined profiles for use cases such as:

- High throughput
- Low latency
- Saving power

It is possible to modify the rules defined for each profile and customise how to tune a particular device. When you switch to another profile or deactivate TuneD, all changes made to the system settings by the previous profile revert back to their original state.
