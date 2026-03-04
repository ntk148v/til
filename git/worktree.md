# Git Worktree

Source: <https://www.gitkraken.com/learn/git/git-worktree>

The Git worktree command allows you to checkout and work in multiple Git branches simultaneously. Now, what situations might you utilize this action?

**Scenario:**

- you’re in the middle of making numerous changes on a project with multiple new dependencies introduced with various WIP changes
- what would happen if you suddenly have to work on a hotfix in another branch?
- for many people, the normal workflow: git stash -> checkout the hotfix branch -> conclude that work -> re-checkout the branch you were originally on and pop your stash.
- With Git worktree, tell Git to checkout the feature branch in a different directory, outside the present working directory and change to that directory; from here, you can do your work and change back to the original directory to find all your work in progress awaiting you.

In Git, a branch is a pointer to one specific commit, while a commit is a snapshot of your repository at a specific point in time. Your branch pointer moves along with each new commit you make.

By default, Git only tracks and moves that pointer along on one branch at a time. The branch you selected with Git checkout is considered your “working tree”. Just like a tree in the forest, a Git worktree can have several branches at once, which is exactly what the Git worktree command allows you to do. To keep things organized, Git worktree places each branch into a different specified folder in your file system. To move between the multiple branches on the worktree, you simply change directory to work against the needed branch.

![](https://www.gitkraken.com/wp-content/uploads/2022/03/Worktrees-01-1024x460.png.webp)

A Git worktree will always point to a folder on your file system while referencing a particular commit object, like a branch. In order to work in multiple checked out branches at once, you need to add each branch as a new working tree to the Git worktree. There are 4 possible scenarios you can encounter when using Git worktree add:

- Add a new working tree to a directory that shares the same name as the branch (the most common method)
- Add a new working tree to a directory with a different name as the branch
- Create a new Git branch and add a new working tree to a directory that shares the same name as the branch
- Create a new branch and add a new working tree to a directory with a different name as the new branch
