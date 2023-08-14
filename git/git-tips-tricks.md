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
