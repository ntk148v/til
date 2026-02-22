# Testing Ansible with Molecule

Source:

- <https://molecule.readthedocs.io/en/latest/getting-started/>
- <https://www.jeffgeerling.com/blog/2018/testing-your-ansible-roles-molecule>

Table of contents:

- [Testing Ansible with Molecule](#testing-ansible-with-molecule)
  - [0. Problem](#0-problem)
  - [1. Introduction](#1-introduction)
  - [2. Play with Molecule](#2-play-with-molecule)
    - [2.1. Getting started](#21-getting-started)
    - [2.2. Custom Docker image](#22-custom-docker-image)
    - [2.3. Test an existing role](#23-test-an-existing-role)
    - [2.4. Test Cluster](#24-test-cluster)

## 0. Problem

You wrote an Ansible playbook, good job, congratulations! Now you have to (should) check if the playbook works correctly. You may have multiple choices:

- Test in production :innocent: Just do it, just run it! If something wrongs, fix and run it again.

<div style="width:480px"><iframe allow="fullscreen" frameBorder="0" height="270" src="https://giphy.com/embed/AbOZR8G922HtmsfNlv/video" width="480"></iframe></div>

- Create a testing environment, check playbook in it.

Unless you're a brave hero or a careless person, you should go to option 2 - testing environment. Let's talk about it, the testing environment should be clean, so the procedure is:

```dunno
- Spin up a VM.
- Run your playbook.
- Destroy the VM.
- If something went wrong, repeat from the first step
```

:roll_eyes: This is pretty inefficient. Another option is you might keep the same VM and clean up manually every time you finish your tests, which is also annoying. That's why we need [Molecule](https://molecule.readthedocs.io/en/latest/) to make life easier.

## 1. Introduction

So the question is: "What is Molecule?"

- Molecule is a testing framework that is designed to aid in development and testing of Ansible roles (and playbooks too).
- Molecule provides support for testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios.
- Molecule encourages an approach that results in consistently developed roles that are well-written, easily understood and maintained.
- Molecule supports only the latest _two major versions of Ansible (N/N-1)_, meaning that if the latest version is 2.9.x, we will also test our code with 2.8.x.

## 2. Play with Molecule

> Source can be found [here](https://github.com/ntk148v/testing/tree/master/ansible/molecule/example).

### 2.1. Getting started

- You can install Molucule from pip/source, there are [many options](https://molecule.readthedocs.io/en/latest/installation), just choose one.

```shell
$ pip install molecule
```

- Molecule requires an external Python dependency for the Docker driver.

```shell
$ pip install 'molecule[docker]'
$ molecule --version
molecule 4.0.4 using python 3.10
    ansible:2.14.3
    delegated:4.0.4 from molecule
    docker:2.1.0 from molecule_docker requiring collections: community.docker>=3.0.2 ansible.posix>=1.4.0

$ molecule drivers
╶──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╴
  delegated
  docker
```

- Before start integrating Molecule into an _existing role_, let's use Molecule itself to create a new role with the standard structure.

```shell
# Molecule uses ansible-galaxy under the hood to generate conventional role layouts
$ molecule init role kiennt26.example -d docker

INFO     Initializing new role example...
Using /etc/ansible/ansible.cfg as config file
- Role example was created successfully
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: error in 'jsonfile' cache plugin while trying to create cache dir
/etc/ansible/facts.d : b"[Errno 13] Permission denied: '/etc/ansible/facts.d'"
localhost | CHANGED => {"backup": "","changed": true,"msg": "line added"}
INFO     Initialized role in /path/to/example successfully

$ tree example

example
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── molecule # <---  here we go
│   └── default
│       ├── converge.yml
│       ├── molecule.yml
│       └── verify.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```

- Inside `example/molecule`, there is a single `root_scenario` called `default`. Scenarios are the starting point for a lot of powerful functionality that Molecule offers.

```shell
├── molecule # <---  here we go
│   └── default # Scenario
│       ├── converge.yml # Playbook file that contains the call for your role
│       ├── molecule.yml  # The central configuration entrypoint for Molecule
│       └── verify.yml # Ansible file used for testing as Anisble the default verifier.
```

- Check `molecule.yml`:

```shell
$ cat example/molecule/default/molecule.yml
---
dependency: # Molecule uses galaxy development guide by default to resolve your role dependencies: <https://docs.ansible.com/ansible/latest/galaxy/dev_guide.html>
  name: galaxy
driver: # Molecule use the driver to delegate the task of creating instances
  name: docker
platforms: # To know which instances to create, name and to which group each instance belongs -> test role against multiple distros
  - name: instance
    image: quay.io/centos/centos:stream8
    pre_build_image: true
provisioner: # To control the scenario sequence order
  name: ansible
verifier: # Specific state checking tests
  name: ansible
```

- Molecule create an isntance:

```shell
$ molecule create
# ...
PLAY [Create] ******************************************************************

TASK [Set async_dir for HOME env] **********************************************
ok: [localhost]

TASK [Log into a Docker registry] **********************************************
skipping: [localhost] => (item=None)
skipping: [localhost]

TASK [Check presence of custom Dockerfiles] ************************************
ok: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True})

TASK [Create Dockerfiles from image names] *************************************
skipping: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True})
skipping: [localhost]

TASK [Synchronization the context] *********************************************
skipping: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True})
skipping: [localhost]

TASK [Discover local Docker images] ********************************************
ok: [localhost] => (item={'changed': False, 'skipped': True, 'skip_reason': 'Conditional result was False', 'item': {'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True}, 'ansible_loop_var': 'item', 'i': 0, 'ansible_index_var': 'i'})

TASK [Build an Ansible compatible image (new)] *********************************
skipping: [localhost] => (item=molecule_local/quay.io/centos/centos:stream8)
skipping: [localhost]

TASK [Create docker network(s)] ************************************************
skipping: [localhost]

TASK [Determine the CMD directives] ********************************************
ok: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True})

TASK [Create molecule instance(s)] *********************************************
changed: [localhost] => (item=instance)

TASK [Wait for instance(s) creation to complete] *******************************
FAILED - RETRYING: [localhost]: Wait for instance(s) creation to complete (300 retries left).
changed: [localhost] => (item={'failed': 0, 'started': 1, 'finished': 0, 'ansible_job_id': '942472572382.94929', 'results_file': '/home/user/.ansible_async/942472572382.94929', 'changed': True, 'item': {'image': 'quay.io/centos/centos:stream8', 'name': 'instance', 'pre_build_image': True}, 'ansible_loop_var': 'item'})

PLAY RECAP *********************************************************************
localhost                  : ok=6    changed=2    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0

INFO     Running default > prepare

# Check Docker list
$ docker ps
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS          PORTS     NAMES
744e3b709b0c   quay.io/centos/centos:stream8   "bash -c 'while true…"   32 seconds ago   Up 31 seconds             instance

# Verify that Molecule has created the instance
$ molecule list

INFO     Running default > list
                ╷             ╷                  ╷               ╷         ╷
  Instance Name │ Driver Name │ Provisioner Name │ Scenario Name │ Created │ Converged
╶───────────────┼─────────────┼──────────────────┼───────────────┼─────────┼───────────╴
  instance      │ docker      │ ansible          │ default       │ true    │ false
```

- Add to `tasks/main.yml`:

```shell
- name: Molecule Hello World!
  ansible.builtin.debug:
    msg: Hello, World!
```

- Test our role against our instance:

```shell
$ molecule converge
# ...
PLAY [Converge] ****************************************************************

TASK [Gathering Facts] *********************************************************
ok: [instance]

TASK [Include kiennt26.example] ************************************************

TASK [kiennt26.example : Molecule Hello World!] ********************************
ok: [instance] => {
    "msg": "Hello, World!"
}

PLAY RECAP *********************************************************************
instance                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- Clean up:

```shell
$ molecule destroy

$ molecule list
INFO     Running default > list
                ╷             ╷                  ╷               ╷         ╷
  Instance Name │ Driver Name │ Provisioner Name │ Scenario Name │ Created │ Converged
╶───────────────┼─────────────┼──────────────────┼───────────────┼─────────┼───────────╴
  instance      │ docker      │ ansible          │ default       │ false   │ false
                ╵             ╵                  ╵               ╵         ╵
```

- To run a full test sequence:

```shell
$ molecule test
# ...
PLAY [Converge] ****************************************************************

TASK [Gathering Facts] *********************************************************
ok: [instance]

TASK [Include kiennt26.example] ************************************************

TASK [kiennt26.example : Molecule Hello World!] ********************************
ok: [instance] => {
    "msg": "Hello, World!"
}

PLAY RECAP *********************************************************************
instance                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Running default > idempotence

PLAY [Converge] ****************************************************************

TASK [Gathering Facts] *********************************************************
ok: [instance]

TASK [Include kiennt26.example] ************************************************

TASK [kiennt26.example : Molecule Hello World!] ********************************
ok: [instance] => {
    "msg": "Hello, World!"
}

PLAY RECAP *********************************************************************
instance                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Idempotence completed successfully.
INFO     Running default > side_effect
WARNING  Skipping, side effect playbook not configured.
INFO     Running default > verify
INFO     Running Ansible Verifier

PLAY [Verify] ******************************************************************

TASK [Example assertion] *******************************************************
ok: [instance] => {
    "changed": false,
    "msg": "All assertions passed"
}

PLAY RECAP *********************************************************************
instance                   : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

INFO     Verifier completed successfully.
INFO     Running default > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running default > destroy

PLAY [Destroy] *****************************************************************

TASK [Set async_dir for HOME env] **********************************************
ok: [localhost]

TASK [Destroy molecule instance(s)] ********************************************
changed: [localhost] => (item=instance)

TASK [Wait for instance(s) deletion to complete] *******************************
changed: [localhost] => (item=instance)

TASK [Delete docker networks(s)] ***********************************************
skipping: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=2    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

INFO     Pruning extra files from scenario ephemeral directory
```

- With Molecule, any time you want to bring up a local environment and start running your role, you just run `molecule converge`. And since you can use Molecule with Docker, Virtualbox,... you can have your roles run inside any type of virtual environment you need (Sometimes it can be hard to test certain types of applications or automation inside of Docker container).

### 2.2. Custom Docker image

- The Docker driver supports using pre-built images and `docker build`-ing local customizations for each scenario's platform.
- The Docker image use by a scenario is governed by the following configuration items:
  - `platforms[*].image`: Docker image name:tag to use as base image.
  - `platforms[*].pre_build_image`: Whether to customize base image or use as-is:
    - `true`: use the specified `platforms[*].image` as-is.
    - `false`: exec Docker build to customize base image using either:
      - Dockerfile specified by `platforms[*].dockerfile` or
      - Dockerfile rendered from `Dockerfile.j2` template (in scenario dir).

- Create the scenario with custom Docker image:

```shell
$ molecule init scenario -d docker custom-image

INFO     Initializing new scenario custom-image...
INFO     Initialized scenario in /path/to/example/molecule/custom-image successfully.
```

- Change to `platforms[*].pre_build_image` to `false`:

```yml
platforms:
  - name: instance
    image: quay.io/centos/centos:stream8
    pre_build_image: false
```

- Create the custom Dockerfile.j2:

```Dockerfile
# Molecule managed

{% if item.registry is defined %}
FROM {{ item.registry.url }}/{{ item.image }}
{% else %}
FROM {{ item.image }}
{% endif %}

RUN if [ $(command -v apt-get) ]; then                                                        apt-get update && apt-get install -y python sudo bash ca-certificates iproute2 init && apt-get clean; \
    elif [ $(command -v zypper) ]; then                                                       zypper refresh && zypper install -y python sudo bash python-xml iproute2 systemd-sysvinit && zypper clean -a; \
    elif [ $(command -v apk) ]; then                                                          apk update && apk add --no-cache python sudo bash ca-certificates; \
    elif [ $(command -v xbps-install) ]; then                                                 xbps-install -Syu && xbps-install -y python sudo bash ca-certificates iproute2 && xbps-remove -O; \
    elif [ $(command -v swupd) ]; then                                                        swupd bundle-add python3-basic sudo iproute2; \
    elif [ $(command -v dnf) ] && cat /etc/os-release | grep -q '^NAME=Fedora' && \
           cat /etc/os-release | grep -q '^VERSION_ID=30'; then                               dnf makecache && dnf --assumeyes install python sudo python-devel python3-dnf bash iproute && dnf clean all; \
    elif [ $(command -v dnf) ] && cat /etc/os-release | grep -q '^NAME=Fedora'; then          dnf makecache && dnf --assumeyes install python sudo python-devel python*-dnf bash iproute && dnf clean all; \
    elif [ $(command -v dnf) ] && cat /etc/os-release | grep -q '^NAME="CentOS Linux"' ; then dnf makecache && dnf --assumeyes install python36 sudo platform-python-devel python*-dnf bash iproute && dnf clean all && ln -s /usr/bin/python3 /usr/bin/python; \
    elif [ $(command -v yum) ]; then                                                          yum makecache fast && yum install -y python sudo yum-plugin-ovl bash iproute && sed -i 's/plugins=0/plugins=1/g' /etc/yum.conf && yum clean all; \
    fi

# Centos:8 + ansible 2.7 failed with error: "The module failed to execute correctly, you probably need to set the interpreter"
# Solution: ln -s /usr/bin/python3 /usr/bin/python

# Fedora:30 deprecated python2-dnf
# Solution: explicitly use python3-dnf instead
# https://github.com/ansible/ansible/issues/54855
# https://github.com/ansible/ansible/issues/59248
```

- Customize `example/custom-image/molecule.yml`:

```yml
platforms:
  - name: instance-${MOLECULE_DISTRO:-'quay.io/centos/centos:stream8'}
    image: ${MOLECULE_DISTRO:-'quay.io/centos/centos:stream8'}
    pre_build_image: false
```

- Start the instances:

```shell
$ molecule create -s custom-image -d docker
# ...
PLAY [Create] ******************************************************************

TASK [Set async_dir for HOME env] **********************************************
ok: [localhost]

TASK [Log into a Docker registry] **********************************************
skipping: [localhost] => (item=None)
skipping: [localhost]

TASK [Check presence of custom Dockerfiles] ************************************
ok: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance-quay.io/centos/centos:stream8', 'pre_build_image': False})

TASK [Create Dockerfiles from image names] *************************************
ok: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance-quay.io/centos/centos:stream8', 'pre_build_image': False})

TASK [Synchronization the context] *********************************************
changed: [localhost] => (item={'image': 'quay.io/centos/centos:stream8', 'name': 'instance-quay.io/centos/centos:stream8', 'pre_build_image': False})

TASK [Discover local Docker images] ********************************************
ok: [localhost] => (item=None)
ok: [localhost]

TASK [Build an Ansible compatible image (new)] *********************************

# ...

# You want to change to another base image
$ MOLECULE_DISTRO=ubuntu:22.04 molecule create -s custom-image -d docker
# ...
PLAY [Create] ******************************************************************

TASK [Set async_dir for HOME env] **********************************************
ok: [localhost]

TASK [Log into a Docker registry] **********************************************
skipping: [localhost] => (item=None)
skipping: [localhost]

TASK [Check presence of custom Dockerfiles] ************************************
ok: [localhost] => (item={'image': 'ubuntu:22.04', 'name': 'instance-ubuntu:22.04', 'pre_build_image': False})

TASK [Create Dockerfiles from image names] *************************************
changed: [localhost] => (item={'image': 'ubuntu:22.04', 'name': 'instance-ubuntu:22.04', 'pre_build_image': False})

TASK [Synchronization the context] *********************************************
changed: [localhost] => (item={'image': 'ubuntu:22.04', 'name': 'instance-ubuntu:22.04', 'pre_build_image': False})

TASK [Discover local Docker images] ********************************************
ok: [localhost] => (item=None)
ok: [localhost]

TASK [Build an Ansible compatible image (new)] *********************************
# ...
```

### 2.3. Test an existing role

If you want to initialize Molecule within an existing role, you would use the `molecule init scenario -r my_role_name my_scenario` command from within the role's directory.

### 2.4. Test Cluster

- Create new scenario:

```shell
$ molecule init scenario -d docker cluster
```

- Modify `example/molecule/cluster/molecule.yml` to create 3 hosts:

```yml
platforms:
  - name: instance-0
    image: quay.io/centos/centos:stream8
    pre_build_image: true
  - name: instance-1
    image: quay.io/centos/centos:stream8
    pre_build_image: true
  - name: instance-2
    image: quay.io/centos/centos:stream8
    pre_build_image: true
```

- You can also take advantage of yaml [anchor and merge key features](https://learnxinyminutes.com/docs/yaml/) to make it shorter (if your instance definition is complicated, and you don't to waste your time repeat it):
  - Note: anchors and merge keys can only be used in the same yaml file. So this will not work between different scenario.

```yml
platforms:
  - &default-instance
    name: instance-0
    image: quay.io/centos/centos:stream8
    pre_build_image: true
    groups:
      - test
    # command: /sbin/init
    # volumes:
    #   - /sys/fs/cgroup:/sys/fs/cgroup:ro
    # networks:
    #   - name: net1
  - <<: *default-instance
    name: instance-1
  - <<: *default-instance
    name: instance-2
```

- Start instances:

```shell
$ molecule create -s cluster

$ molecule list -s cluster

  Instance Name │ Driver Name │ Provisioner Name │ Scenario Name │ Created │ Converged
╶───────────────┼─────────────┼──────────────────┼───────────────┼─────────┼───────────╴
  instance-0    │ docker      │ ansible          │ cluster       │ true    │ false
  instance-1    │ docker      │ ansible          │ cluster       │ true    │ false
  instance-2    │ docker      │ ansible          │ cluster       │ true    │ false
                ╵             ╵                  ╵               ╵         ╵

$ docker ps
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS          PORTS     NAMES
8fe77dd8e250   quay.io/centos/centos:stream8   "bash -c 'while true…"   34 seconds ago   Up 33 seconds             instance-2
0dee3cd04c07   quay.io/centos/centos:stream8   "bash -c 'while true…"   35 seconds ago   Up 34 seconds             instance-1
9004da1f541d   quay.io/centos/centos:stream8   "bash -c 'while true…"   36 seconds ago   Up 35 seconds             instance-0
```

- Molecule doesn't have an inventory file, so you must define host group in `example/molecule/cluster/molecule.yml` file.

```yaml
platforms:
  - &default-instance
    name: instance-0
    image: quay.io/centos/centos:stream8
    pre_build_image: true
    groups:
      - test # <-- your group
```
