---
name: pr
description: Create a new branch, commit all changes, push, and open a pull request
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash(git *), Bash(gh *)
argument-hint: [branch-name] [commit-message]
---

# Create Branch, Commit, Push, and Open PR

Create a new branch, commit all changes, push to remote, and open a pull request using the gh CLI.

## Arguments

- `$0` — branch name (required)
- Remaining arguments (`$1...`) — commit message (required)

If arguments are missing, ask the user for the missing information before proceeding.

## Steps

1. **Validate** — Ensure there are staged or unstaged changes to commit. If there are no changes, inform the user and stop.

2. **Create branch** — Run `git checkout -b $0` to create and switch to the new branch.

3. **Stage changes** — Run `git add -A` to stage all changes.

4. **Commit** — Create a commit with the provided message. Do NOT include a Co-Authored-By line.

5. **Push** — Run `git push -u origin $0` to push the branch and set upstream tracking.

6. **Open PR** — Run `gh pr create` targeting the `main` branch:
   - Use the commit message as the PR title
   - Generate a concise PR body with a `## Summary` section describing the changes and a `## Test plan` section

7. **Report** — Output the PR URL to the user.

## Important

- If any step fails, stop and report the error. Do not continue to subsequent steps.
- Never force push.
- Never amend existing commits.
- If the branch already exists, inform the user and stop.
