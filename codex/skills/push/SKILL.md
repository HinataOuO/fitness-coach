---
name: push
description: >
  Quick git commit and push workflow for Codex. Use when the user asks to
  commit, push, run "push", publish current changes, or wants a concise git
  commit created from the current worktree.
---

# Push

Commit and push relevant changes from the current repository.

## Workflow

1. Inspect changes:
   - Run `git status --short`
   - Run `git diff`
   - Run `git diff --staged`
   - Run `git log --oneline -5` to match commit style
2. Identify which changed files belong to the user's request.
3. Never stage secrets, credentials, `.env` files, private profiles, or unrelated
   user changes.
4. Stage only specific files with `git add <path>...`.
5. If the user supplied commit text after the skill name, use it as the commit
   message. Otherwise write a concise message matching repo style.
6. Commit with `git commit -m "<message>"`.
7. Show the created commit before pushing:
   - Run `git show --stat --oneline --summary HEAD`
   - Report the commit hash, message, branch, and included files.
8. Ask the user for explicit confirmation before pushing.
   - Do not run `git push` until the user confirms.
9. Push to the current branch with `git push`.
10. Report:
   - commit hash and message
   - branch
   - remote push result
   - files included

## Safety

- Do not force push.
- Do not skip hooks with `--no-verify`.
- Do not use `git add -A` unless every changed file is clearly safe and related.
- Always show the created commit and ask for confirmation before pushing.
- If push fails because history diverged, stop and report the error. Do not
  rebase, merge, or reset without user confirmation.
- If there are unrelated unstaged changes, leave them alone and mention them.
