# OpenStack Heat Tips

Some tips to write a flexible HOT template

## 1. Hot Template spec

- [Check this link](https://docs.openstack.org/heat/queens/template_guide/hot_spec.html#hot-spec)

## 2. Hot Template example

- [Check this](https://github.com/openstack/heat-templates/tree/master/hot)

## 3. Write a complex HOT Template with user_data

- Use `user_data`:
  - `user_data` completely in RAW format and `str\_replace`, for [example](https://github.com/openstack/heat-templates/blob/master/hot/autoscaling.yaml#L81)
  - `user_data` + `get_file`, write all execuable commands to file and just get it.
  - `user_data` + RAW format + `OS::Heat::MultipartMime`: We can split scripts to multiple file scripts. For example

```
complex-server:
  type: OS::Nova::Server
  properties:
    image: ...
    ...
    user_data_format: RAW
    user_data: { get_resource: complex_collection_software_configs }

complex_collection_software_configs:
  type: OS::Heat::MultipartMime
  properties:
    parts:
      - config: { get_resource: install_docker }
      - config: { get_resource: disable_selinux }

install_docker:
  type: OS::Heat::SoftwareConfig
  properties:
    group: ungrouped
    config: { get_file: /path/to/install_docker.sh }

disable_selinux:
  type: OS::Heat::SoftwareConfig
  properties:
    group: ungrouped
    config: { get_file: /path/to/disable_selinux.sh }
```
