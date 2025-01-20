# Git tips & tricks

## 1. List only untracked files

```bash
git ls-files --others --exclude-standard
# Add untracked files
git add $(git ls-files -o --exclude-standard)
```

## 2. Use --diff-filter

- What is diff-filter?

```
--diff-filter=[(A|C|D|M|R|T|U|X|B)...[*]]
    Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type (i.e. regular file, symlink, submodule, ...) changed (T), are Unmerged (U),
    are Unknown (X), or have had their pairing Broken (B). Any combination of the filter characters (including none) can be used. When * (All-or-none) is added to the combination, all
    paths are selected if there is any file that matches other criteria in the comparison; if there is no file that matches other criteria, nothing is selected.

    Also, these upper-case letters can be downcased to exclude. E.g.  --diff-filter=ad excludes added and deleted paths.

    Note that not all diffs can feature all types. For instance, diffs from the index to the working tree can never have Added entries (because the set of paths included in the diff is
    limited by what is in the index). Similarly, copied and renamed entries cannot appear if detection for those types is disabled.
```

```bash
# List only unmerged files
git diff --name-only --diff-filter=U
# Add only unmerged files
git add $(git diff --name-only --diff-filter=U | xargs)
```

## 3. git-gc

- `git-gc` - Cleanup unnecessary files and optimize the local repository.

```man
Runs a number of housekeeping tasks within the current repository, such as compressing file revisions (to reduce disk space and increase performance), removing unreachable objects which may have been created from prior invocations of git add, packing refs, pruning reflog, rerere metadata or stale working trees. May also update ancillary indexes such as the commit-graph.

When common porcelain operations that create objects are run, they will check whether the repository has grown substantially since the last maintenance, and if so run git gc automatically. See gc.auto below for how to disable this behavior.

Running git gc manually should only be needed when adding objects to a repository without regularly running such porcelain commands, to do a one-off repository optimization, or e.g. to clean up a suboptimal mass-import. See the "PACKFILE OPTIMIZATION" section in git-fast-import[1] for more details on the import case.
```

## 4. Oh shit, git?

Source: <https://ohshitgit.com/>

### 4.1. Oh shit, I did something terribly wrong, please tell me git has a magic time machine?

```shell
git reflog
# you will see a list of every thing you've
# done in git, across all branches!
# each one has an index HEAD@{index}
# find the one before you broke everything
git reset HEAD@{index}
# magic time machine
```

### 4.2. Oh shit, I accidentally committed something to master that should have been on a brand new branch!

```shell
# create a new branch from the current state of master
git branch some-new-branch-name
# remove the last commit from the master branch
git reset HEAD~ --hard
git checkout some-new-branch-name
# your commit lives in this branch now :)
```

### 4.3. Oh shit, I accidentally committed to the wrong branch!

```shell
# undo the last commit, but leave the changes available
git reset HEAD~ --soft
git stash
# move to the correct branch
git checkout name-of-the-correct-branch
git stash pop
git add . # or add individual files
git commit -m "your message here";
# now your changes are on the correct branch
```

```shell
# undo the last commit, but leave the changes available
git reset HEAD~ --soft
git stash
# move to the correct branch
git checkout name-of-the-correct-branch
git stash pop
git add . # or add individual files
git commit -m "your message here";
# now your changes are on the correct branch
```

### 4.4. Oh shit, I need to undo my changes to a file!

```shell
# find a hash for a commit before the file was changed
git log
# use the arrow keys to scroll up and down in history
# once you've found your commit, save the hash
git checkout [saved hash] -- path/to/file
# the old version of the file will be in your index
git commit -m "Wow, you don't have to copy-paste to undo"
```

## 5. help.autoCorrect

If git detects typos and can identify exactly one valid command similar to the error, git will try to suggest the correct command or even run the suggestion automatically. Possible config values are:

0 (default): show the suggested command.

- positive number: run the suggested command after specified deciseconds (0.1 sec).
- "immediate": run the suggested command immediately.
- "prompt": show the suggestion and prompt for confirmation to run the command.
- "never": don’t run or show any suggested command.
