# Git Commit Message Template

- Create your template `~/.gitmessage` (this template get from [here](https://gist.github.com/lisawolderiksen/a7b99d94c92c6671181611be1641c733)):

```txt
# Title: Summary, imperative, start upper case, don't end with a period
# No more than 50 chars. #### 50 chars is here:  #

# Remember blank line between title and body.

# Body: Explain *what* and *why* (not *how*). Include task ID (Jira issue).
# Wrap at 72 chars. ################################## which is here:  #


# At the end: Include Co-authored-by for all contributors.
# Include at least one empty line before it. Format:
# Co-authored-by: name <user@users.noreply.github.com>
#
# How to Write a Git Commit Message:
# https://chris.beams.io/posts/git-commit/
#
# 1. Separate subject from body with a blank line
# 2. Limit the subject line to 50 characters
# 3. Capitalize the subject line
# 4. Do not end the subject line with a period
# 5. Use the imperative mood in the subject line
# 6. Wrap the body at 72 characters
# 7. Use the body to explain what and why vs. how
```

- Automation: To tell Git to use the template file, you can use the [following command](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration) (or simply edit your `~/.gitconfig` directly).

```bash
git config --global commit.template ~/.gitmessage
```

- When you run `git commit`, you will see a message consists of two parts: template, then Git's standard message asking to "Please enter the commit message".
- Note that, _do not_ use `git commit -m "Commit message"`.
- Share this template with your team, everyone should follow the rules.
