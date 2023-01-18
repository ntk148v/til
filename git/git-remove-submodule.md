# How to remove a submodule?

Source: <https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule>

In modern git, this has become quite simple. Just run:

```bash
git rm <path-to-submodule>
# commit your change
```

This removes the filetree at `<path-to-module>`, and the submodule's entry in the `.gitmodules` file, i.e. all traces of the submodule in your repository proper are removed.

As [the docs note](https://git-scm.com/docs/gitsubmodules#:%7E:text=file%20system%2C%20but-,the%20Git%20directory%20is%20kept%20around,-as%20it%20to), however, the `.git` dir of the submodule is kept around (in the `modules` directory of the main project's `.git` dir), to make it possible to checkout past commits without requiring fetching from another repository.

If you nonetheless want to remove this info, manually delete the submodule's directory in `.git/modules`, and remove the submodule's entry in the file `.git/config`. These steps can be automated using the commands:

```bash
rm -rf .git/modules/<path-to-submodule>
git config --remove-section submodule.<path-to-submodule>
```

```bash
#/bin/bash
submodule=$1
git rm $submodule
rm -rf .git/modules/$submodule
git config --remove-section submodule.$submodule
```
