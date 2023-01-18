# OpenStack Kolla

## Problems of OpenStack

- OpenStack in Theory: Discrete services, when combined providing private cloud capabiltites.

![The Beautify of OpenStack](https://allthingsopendotcom.files.wordpress.com/2014/10/screen-shot-2014-10-22-at-8-39-48-am.png)

- OpenStack in Reality: Not so discrete services, with interdependencies, which complicates the deployment with lifecycle of OpenStack environments. [Image]

![The Reality of OpenStack](https://allthingsopendotcom.files.wordpress.com/2014/10/screen-shot-2014-10-22-at-8-42-30-am.png)

- Separatopm of OpenStack components which share common libraries in different versions.

- Upgradability of OpenStack.

- "It worked on my devstack", "It work on my test env"

- Possible differences in deployments due to i.e packages installation in different time.

- Some questions start to arise:

  - How do I add more nodes/systems to my cluster.

  - If I `apt-get update` or `yum update` one of my nodes, what happens to state of that system?

  - How do I synchronize common configuration changes across my OpenStack environments.

  - How do I upgrade just one piece/service of my OpenStack environment to fix a bug?

  - How do I test that bugfix in isolation?

  - How do I roll back if that bugfix causes more issues.

  - How do I update OpenStack release A (Kilo for example) to release B (Mitaka for example)? Without downtime?

  - And on and on.

--> **The questions start having answers when deploy OpenStack following the tenents of [immutable infrastructure](https://sdake.io/2015/11/11/the-tldr-on-immutable-infrastructure/)**

--> **Dockerizing OpenStack.**

## Dockerizing OpenStack

1. Why Docker?

   - Pros:

     - Immutable.

     - Portable.

     - Fast.

     - App focused experience.

     - Massive community.

     - Branding.

     - Growth.

   - Cons:

     - Green - Kolla is even greener.

     - Additional complexity.

     - Difficult to audit.

2. What does it mean?

   Create Docker images for all OpenStack components.

   - OpenStack has **many** services: Keystone, Nova, Swift, Cinder,...

   - Each service can have one or more components. For ex Nova: api, scheduler, condutor,...

   - Docker best practices calls one function/proccess per container. All of this boils down to having to create a significant number of docker images (around 45 for the base services).

   - This now presents with a new problem, managing a large amount of Docker containers over many hosts.

3. What does it buy you?

   - Simplify deployments and ongoing operations. Breaking up the OpenStack services up into the micro services (Docker containers) each micro service becomes an atomic unit of management such as deployment, upgrading, scaling,...

   - Repeatable, reliale and fast. As long as the Docker container are idemponent:

     - Patching, upgrading the docker containers are atomic.

     - The patches are applied upstream to docker image. Tags are then used for rolling forward and backward.

## Introduction

1. What exactly is it?

   - Openstack Kolla is a recent project to come under the Openstack Big Tent and aims to provide production-ready, ansible-based, declarative deployment of Openstack entirely in Docker containers.

   - OpenSource project is hosted on StackForge.

   - Goal: Scalable, fast, reliable and upgradable OpenStack clouds using community best practices.

   - Kolla provides Docker containers and Ansible playbooks to meet Kolla’s mission. Kolla’s mission is to provide production-ready containers and deployment tools for operating OpenStack clouds.

   - Kolla is highly opinionated out of the box, but allows for complete customization. This permits operators with minimal experience to deploy OpenStack quickly and as experience grows modify the OpenStack configuration to suit the operator’s exact requirements.

   - Docker images: View the available images on [Docker Hub](https://hub.docker.com/u/kolla/)

2. What does it do?

   - Provide all the Dockerfiles to build the OpenStack services Docker container images.

     - A simple Python script to build all the images using the Dockerfiles and optionally push them to a private registry.

     - Can build from both source (pull from github) or binary (RPMs/Debs - for example RDO). Source builds allow the build to pick up patches/releases that have not yet made it into the distros yet.

   - Provide start/config scripts that live inside the images to start/config the specific OpenStack service.

3. Current Status.

   - Core Services Containers completed.

   - Kolla is tested on CentOS, Oracle Linux, RHEL and Ubuntu as both container OS platforms and bare metal deployment targets.

   - Single Node & MultiNode installation with Ansible completed.

   - Configuration management for core services with Ansible is done.

   - Templating Dockerfiles is done too.

4. Contribution Summary.

   - Contribution by companies.

   ![Contribution by companies](https://github.com/ntk148v/research_about_kolla/blob/master/images/contribution_by_companies.png?raw=true)

   - Contribution by contributors.

   ![Contribution by contributors](https://github.com/ntk148v/research_about_kolla/blob/master/images/contribution_by_contributors.png?raw=true)

## Architecture

![Kolla's Architecture](http://image.slidesharecdn.com/tuckeropenstacksummitvancouverpossibilities-150525221145-lva1-app6891/95/openstack-in-an-ever-expanding-world-of-possibilities-vancouver-2015-summit-27-638.jpg?cb=1432592195)

## Deployment Philosophy

### Overview

- Kolla has an objective to replace the inflexible, painful, resource-intensive deployment process of OpenStack with a flexible, painless, inexpensive deployment process.

- Simplify the deployment process while enabling flexible deployment models.

- Allow deploy with the simple configuration of 3 key/value pairs. And Kolla offers full capabilty to override every OpenStack service configuration option in the deployment.

### ~~Template customization.~~

### Custom configuration sections

- During deployment of an OpenStack service, a basic set of default configuration options are merged with and overridden by custom ini configuration sections.

- How to config and how it actually works? Note, see [kolla-ansible](http://github.com/openstack/kolla-ansible). In Ocata release, `ansible` dir is removed from kolla repo, and move to kolla-ansible repo. See Source Directories section.

  - At the beginning, you should define `node_custom_config` var in /etc/kolla/globals.yml. Default it's e/etc/kolla/config.
  - Then, Kolla will look for a file in /etc/kolla/config/<< service name >>/<< config file >>. This can be done per-project, per-service or per-service-on-specified-host. For example to override scheduler_max_attempts in nova scheduler, the operator needs to create /etc/kolla/config/nova/nova-scheduler.conf with content:

    ```
    [DEFAULT]
    scheduler_max_attempts = 100
    ```

  - Access to ansible/roles dir, role - service. For example. look at [roles/nova/tasks/config.yml](https://github.com/openstack/kolla-ansible/blob/master/ansible/roles/nova/tasks/config.yml). Kolla-ansible will execute [merge-configs)](https://github.com/openstack/kolla-ansible/blob/master/ansible/action_plugins/merge_configs.py) action. It will be read files in {{ node_custom_config }}/nova/ dir (if present, of course), then merge all of them together into nova.conf file.

  - Now, cd to /etc/kolla/<< nova-component >> (like nova-compute for e.x), you will see nova.conf file.

- Custom configuration sections is a flexible way to config. Absolutely, you have to fill a correct-config in your custom config file. If you put something like `virt_type = wrong_type` in nova-compute.conf, it doesn't work. So, do it carefully.

## Components of Kolla

## Source Directories

Note: Ocata - `ansible` directory is split to [openstack kolla-ansible](http://github.com/openstack/kolla-ansible)

- `contrib` - Contains demos scenarios for Heat and Murano and a development environment for Vagrant
- `doc` - Contains documentation.
- `docker` - Contains jinja2 templates for the docker build system.
- `etc` - Contains a reference etc directory structure which requires configuration of a small number of configuration variables to achieve working All-in-One (AIO) deployment.
- `tests` - Contains functional testing tools.
- `tools` - Contains tools for interacting with Kolla.
- `specs` - Contains the Kolla communities key arguments about architectural shifts in the code base.

## Problems

1. Install Kolla in VM (in my case, this is OpenStack instance).

- Problem with MTU value:

  OpenStack network seems to use lower MTU values (<1500) and Docker does not infer the MTU settings from the host's network card [since 1.10](https://github.com/docker/docker/issues/22028). So the solution is running docker daemon with custom MTU settings. To do it, open this file:

  > $ sudo vim /lib/systemd/system/docker.service

  Then edit a line to look like this:

  > ExecStart=/usr/bin/dockerd -H fd:// --mtu=1454

  MTU=1454 is the value that seems to be common with OpenStack. After that, you can look it up in your host using ifconfig or ip a.

  Finally restart Docker:

  > $ sudo systemctl daemon-reload
  > $ sudo service docker restart

But why? Let me explain. Because HTTPS servers set the DF or Do Not Fragment IP flag on packets and regular HTTP servers do not. This matters because HTTP and HTTPS usually transfer a lot of data. That means that the packets are usually quite large and are often the maximum allowed size. So if a server sends out a very big HTTP packet and it goes through a route on the network that does not allow packets that size, then the router in question simply breaks the packet up. But if a server sends out a big HTTPS packet and it hits a route that doesn’t allow packets that size, the routers on that route can’t break the packet up. So they drop the packet and send back an ICMP message telling the machine that sent the big packet to adjust it’s MTU (maximum transfer unit) size and resend the packet. This is called [Path MTU Discovery](https://en.wikipedia.org/wiki/Path_MTU_Discovery). [More details here](http://markmaunder.com/2009/10/20/routers-treat-https-and-http-traffic-differently/)

These links make my day:

- [HTTPS connection failing for Docker >= 1.10](https://bugs.launchpad.net/neutron/+bug/1595762)
- [Docker container not connecting to https endpoints](http://stackoverflow.com/questions/35300497/docker-container-not-connecting-to-https-endpoints)

## References

1. [Kolla's Documentation](http://docs.openstack.org/developer/kolla/)

2. [IaaS Part 2 - Openstack Kolla All-In-One](http://mntdevops.com/2016/08/08/iaas-2/)

3. [OpenStack Contained Slide](http://events.linuxfoundation.org/sites/events/files/slides/CloudOpen2015.pdf)
