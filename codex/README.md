# Codex Skills

This folder contains Codex-native adaptations of the old `.claude/commands/`
workflows.

## Install

Copy any skill directory into your Codex skills directory:

```bash
cp -a codex/skills/push "$CODEX_HOME/skills/push"
cp -a codex/skills/release "$CODEX_HOME/skills/release"
cp -a codex/skills/git-issue "$CODEX_HOME/skills/git-issue"
```

Then invoke them by mentioning the skill name, for example:

- `$push` to commit and push relevant changes
- `$release v1.2.0` to create a GitHub release
- `$git-issue 6` to inspect and plan work for issue `#6`

## Notes

- These skills do not use Claude command syntax.
- They rely on standard Codex tools, shell commands, and explicit user approval
  where the action changes remote state.
- Keep repository-specific assumptions inside the skill body instead of hidden
  Claude memory files.
