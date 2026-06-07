---
name: release
description: >
  Create a GitHub release with generated notes. Use when the user asks for a
  release, GitHub release, tag release, or invokes a version such as
  "$release v1.2.0".
---

# Release

Create a GitHub release for the current repository using `gh`.

## Inputs

Expected user input:

```text
$release v1.2.0
$release v1.2.0 Optional title
```

- First token after the skill name is the tag.
- Remaining text is the optional release title.
- Default title is the tag.

If no tag is provided, ask the user for the tag.

## Workflow

1. Validate the tag format.
   - Expected stable release format: `vMAJOR.MINOR.PATCH`
   - Warn if the tag does not match semver.
   - Continue only if the user clearly supplied that tag.
2. Check if the tag already exists:
   - Run `git tag -l <tag>`
   - If it exists, stop and warn the user.
3. Show commits included since the previous tag:
   - Find previous tag with `git describe --tags --abbrev=0`
   - If no previous tag exists, show all commits.
   - Show `git log <range> --oneline`.
4. Confirm with the user before creating the release.
   Show:
   - tag
   - title
   - current branch
   - whether `--prerelease` will be used
   - notes mode: `--generate-notes`
5. Create the release:
   - `gh release create <tag> --title "<title>" --generate-notes --latest`
   - If the tag contains `-alpha`, `-beta`, or `-rc`, add `--prerelease`.
6. Report the release URL.

## Safety

- Never delete or overwrite existing tags.
- Never force push tags.
- Do not create a release without explicit user confirmation after showing what
  will be included.
- If generated notes fail, report the error and offer a manual notes fallback.
