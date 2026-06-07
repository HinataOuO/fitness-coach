---
name: git-issue
description: >
  Fetch a GitHub issue, analyze its scope, inspect relevant repository context,
  and produce a Codex task plan. Use when the user asks to work from a GitHub
  issue, inspect an issue, or mentions "$git-issue <number>".
---

# Git Issue

Fetch a GitHub issue with `gh`, analyze it, and create a practical resolution
plan for the current Codex session.

This skill plans by default. Do not edit project files unless the user asks to
start implementing after the plan.

## Inputs

Supported forms:

```text
$git-issue 6
$git-issue
```

- With a number: inspect that issue.
- Without a number: list open issues and ask which one to inspect.

## Workflow With Issue Number

1. Fetch structured issue data:

```bash
gh issue view <number> --json number,title,body,labels,comments,state
```

2. Analyze from title, body, labels, and comments:
   - scope: feature, bug, refactor, docs, release, automation, ui, backend,
     data, or other
   - layer: frontend, backend, database, cli, docs, repo, automation, or mixed
   - files and components explicitly mentioned
   - files and components inferable from repository search
3. Inspect local context:
   - Search mentioned names with `rg`.
   - Read only files needed to ground the plan.
   - If repo memory exists under `.claude/memory/`, `.agents/`, `docs/`, or
     similar local folders, read only matching scope files.
4. Produce a 3-5 step plan with exact paths where possible.
5. If the issue has label `bug`, put `Priority: high` at the top of the report.

## Workflow Without Issue Number

1. List open issues:

```bash
gh issue list --state open --json number,title,labels
```

2. Show a compact table:
   - issue number
   - title
   - labels
3. Ask the user which issue number to inspect.

## Report Format

```markdown
**Issue**
#<number> <title> - <state> - <labels>

**Scope**
<scope> - <layer>

**Files**
- <path>

**Plan**
1. ...
2. ...
3. ...

**Notes**
- <risks, ambiguities, or missing context>
```

## Safety

- Use `gh issue view` with `--json`; do not scrape terminal prose.
- If the issue is not found, say `Issue #<number> non trovato` and stop.
- If scope is ambiguous, infer from available context and label it as an
  assumption.
- Do not create hidden task objects. In Codex, represent session tasks with
  `update_plan` when implementation is requested.
