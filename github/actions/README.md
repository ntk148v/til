# Github Actions

## 1. What is Github Actions?

Github Actions is a task automation system fully integrated with Github.

## 2. Core concepts

Check [this](https://docs.github.com/en/actions/getting-started-with-github-actions/core-concepts-for-github-actions) for details.

To automate a set of **tasks**, you need to create **workflows** in your Github repository. Github looks for `YAML` files inside of the `.github/workflows` directory. **Events** like commits, the opening or closing of Pull requests, or updates to the project's wiki, trigger the start of a workflow.

**Workflows are composed of jobs**, which run concurrently by default. Each job should represent a separate part of your workflow.

**Jobs contain a list of steps**, which Github executes in sequence. A step can be a set of shell commands or an **action**, which is a pre-built, reusable step implementd either in the TypeScript or inside a container. Some actions are provided by the Github team, while the open-source community maintains many more.

## 3. Tutorial

Follow: https://lab.github.com/githubtraining/github-actions:-hello-worl
