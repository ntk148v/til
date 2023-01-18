# Git two-dot vs three-dot

Source: <https://stackoverflow.com/questions/462974/what-are-the-differences-between-double-dot-and-triple-dot-in-git-com>

## Concepts

From [man gitrevisions](https://git-scm.com/docs/gitrevisions#_dotted_range_notations):

- **The .. (two-dot) range notation**: The `^r1 r2` set operation appears so often that there is a shorthand for it. When you have two commits `r1` and `r2` (named according to the syntax explained in SPECIFYING REVISIONS above), you can ask for commits that are reachable from r2 excluding those that are reachable from r1 by `^r1 r2` and it can be written as `r1..r2`.

- **The ... (three-dot) range notation**: A similar `r1..r2` is called synmmetric difference of `r1` and `r2` and is defined as `r1 r2 --not $(git merge-base --all r1 r2)`. It is the set of commits that are reachable from either one of `r1` (left side) and `r2` (right side) but not from both.

## Git log

- Show all of the commits that B has that A doesn't have.

```bash
git log A..B
```

![](https://i.stack.imgur.com/beLTVm.png)

- Show you both the commits that A has and that B doesn't have, and the commits B has that A doesn't have, or in other words, it will filter out all of the commits that both A and B share, thus only showing the commits that they don't both share.

```bash
git log A...B
```

![](https://i.stack.imgur.com/4SprXm.png)

![](https://i.stack.imgur.com/Fyff5.png)

```bash
git log A...B = git log A..B + git log B..A
```

## Git diff

- Show the difference the tips of the two branches `A` and `B`.

```bash
git diff A..B
git diff A B # the same thing as above
```

- Show the difference between the "merge base" (usually the last commit in common between those branches) of the two branches and the tip of `B`.

```bash
git diff A...B
git diff $(git merge-base A B) B # same thing as above
```

![](https://i.stack.imgur.com/uWWDV.png)

```bash
git diff A..B = git diff A...B + git diff B...A
```
