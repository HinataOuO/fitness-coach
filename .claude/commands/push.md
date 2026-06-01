---
name: push
description: Quick git commit + push. Stages changes, generates commit message, commits, pushes to current branch remote.
---

Execute a full git commit and push flow for the current repository.

Steps (run sequentially):

1. Run `git status` and `git diff` in parallel to see what changed.
2. Run `git log --oneline -5` to check recent commit style.
3. Analyze the changes. Stage only relevant modified/new files (never `.env`, credentials, secrets). Use `git add <specific files>` — avoid `git add -A` unless all changes are clearly safe.
4. Draft a concise commit message (1-2 sentences, focus on WHY not WHAT). Use the repo's existing commit style.
5. Commit with:
```
git commit -m "$(cat <<'EOF'
<message>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```
6. Push to current branch: `git push` (add `-u origin <branch>` if no upstream set).
7. Report: what was committed, what was pushed, branch name.

If `$ARGUMENTS` is non-empty, use it as the commit message instead of generating one.

Safety rules:
- Never force push.
- Never skip hooks (`--no-verify`).
- If push fails due to diverged history, report the error and stop — do NOT rebase or reset without user confirmation.
