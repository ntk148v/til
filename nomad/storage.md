# Storage Plugins

- Nomad's storage plugin support extends this to allow scheduling tasks with externally created storage volumes. Storage plugins are third-party plugins that conform to the [Container Storage Interface (CSI)](https://github.com/container-storage-interface/spec) specification.
- A list of available CSI plugins can be found in the [Kubernetes CSI documentation](https://kubernetes-csi.github.io/docs/drivers.html).
- Choices:
  - [ceph](https://github.com/ceph/ceph-csi):
    - https://croit.io/blog/use-ceph-as-persistent-storage-for-nomad
    - https://itnext.io/provision-volumes-from-external-ceph-storage-on-kubernetes-and-nomad-using-ceph-csi-7ad9b15e9809
  - [openstack](https://github.com/kubernetes/cloud-provider-openstack/tree/master/pkg/csi): cinder and manila
  - [vsphere](https://github.com/kubernetes-sigs/vsphere-csi-driver)
