---
name: release
description: Create a GitHub release with auto-generated notes from merged PRs. Usage: /release v1.2.0 or /release v1.2.0 "optional title"
---

Create a GitHub release for this repo using `gh`.

Parse `$ARGUMENTS`:
- First token = version tag (e.g. `v1.2.0`). Required — if missing, ask the user.
- Remaining tokens (optional) = release title override. Default title: same as tag.

Steps:

1. Validate tag format matches `vMAJOR.MINOR.PATCH` (semver). Warn if not, but proceed if user explicitly provided it.

2. Check if tag already exists:
```
git tag -l <tag>
```
If exists, stop and warn user.

3. Show what will be included — commits since last tag:
```
git log $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --oneline
```
If no prior tag, show all commits.

4. Confirm with user before creating release. Show:
   - Tag to create: `<tag>`
   - Branch: current branch
   - Notes: auto-generated from merged PRs (via `.github/release.yml`)

5. Create release:
```
gh release create <tag> \
  --title "<title>" \
  --generate-notes \
  --latest
```

6. Report release URL.

Safety rules:
- Never delete or overwrite existing tags.
- Never force push tags.
- If `--generate-notes` fails (no PRs merged), offer to open `--notes-start-tag` fallback or manual notes via `--notes-file`.
- Do NOT mark as prerelease unless tag contains `-alpha`, `-beta`, `-rc`. In that case add `--prerelease` flag automatically.
