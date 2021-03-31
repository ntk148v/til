# Amazon ECS

## What is ECS?

ECS is the AWS Docker cotnainer service that handles the orchestration and provisioning of Docker containers.

![](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/images/overview-fargate.png)

## ECS Terms

ECS terminology:
* `Task definition`: This is a blueprint that describes how a docker container should launch. It contains settings like exposed port, docker image, cpu shares, memory requirement, command to run and environmental variables.
* `Task`: This is a running container with the settings defined in the Task Definition. It can be thought of as an "instance" of a Task Definition. Multiple Tasks can be created by one Task Definitions, as demand requires.

![](https://cdn-media-1.freecodecamp.org/images/eL718lUcFCktxO96DKpdAIu1uBguoNqOKHRF)

* `Service`: Defines long running tasks of the same Task Definition. This can be 1 running container of multiple running containers all using the same Task Definition.
* `Cluster`: A logic group of EC2 instances. When an instance launches the ecs-agent software on the server registers the instance to an ECS cluster. This is easily configurable by setting the ECS\_CLUSTER variable in /etc/ecs/ecs.config.
* `Container instance`: This is just an EC2 instance that is part of an ECS cluster and has docker and the ecs-agent running on it.

![](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/images/overview-service-fargate.png)

* `Container agent`: It runs on each infrastructure resource within an ECS cluster. It sends information about the resource's current running tasks and resource utilization to ECS, and starts and stops tasks whenever it receives a request from ECS.

![](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/images/overview-containeragent-fargate.png)

## Resources

1. FreeCodeCamp: https://www.freecodecamp.org/news/amazon-ecs-terms-and-architecture-807d8c4960fd/

2. Medium: https://medium.com/boltops/gentle-introduction-to-how-aws-ecs-works-with-example-tutorial-cea3d27ce63d

3. Official Doc: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
