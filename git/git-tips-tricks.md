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
