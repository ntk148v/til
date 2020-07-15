# Remove sensitive data from a repository

Source: https://docs.github.com/en/github/authenticating-to-github/removing-sensitive-data-from-a-repository

## 1. Intro

To entirely remove unwanted files from a repository's history you can use [git filter-branch](https://git-scm.com/docs/git-filter-branch) command. It rewrites your repository's history, which changes the SHAs for existing commits that you alter and any dependent commits. _Changed commit SHAs may affect open PR in your repository_.

## 2. Step-by-step

- Get a local copy of repository with sensitive data in history.

```bash
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
$ cd YOUR-REPOSITORY
```

- Run the following command, replacing `PATH-TO-YOUR-FILE-WITH-SENSITIVE-DATA` with the **path to the file you want to remove, not just its filename**.

```bash
$ git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch PATH-TO-YOUR-FILE-WITH-SENSITIVE-DATA" \
  --prune-empty --tag-name-filter cat -- --all
```

    - `--all` rewrite all branches and tags.
    - `--prune-empty` Some filters will generate empty commits that leave the tree untouched. This options instructs git-filter-branch to remove such commits.
