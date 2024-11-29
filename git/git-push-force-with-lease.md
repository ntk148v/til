# git push --force-with-lease

Source:

- <https://stackoverflow.com/questions/52823692/git-push-force-with-lease-vs-force>
- <https://git-scm.com/docs/git-push>

`--force` overwrites a remote branch with your local branch.

`--force-with-lease` is a safer option that will not overwrite any work on the remote branch if more commits were added to the remote branch (by another team-member or co-worker or what have you). It ensures you do not overwrite someone else work by force pushing.

For now, "some reasonable default" is tentatively defined as "the value of the remote-tracking branch we have for the ref of the remote being updated", and it is an error if we do not have such a remote-tracking branch.
