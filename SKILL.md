---
name: fitness-coach
description: >
  Dispatcher for athlete profiling, planning, analysis and plan delivery.
  Use only with `$fitness-coach <skill> <Nome>`, where skill is `profile`,
  `planning`, `analyze` or `plan`.
---

## purpose

Route one explicit athlete and fitness skill to the matching internal skill.
Do not provide fitness coaching directly.

Public syntax:

`$fitness-coach <skill> <Nome>`

Valid skills: `profile`, `planning`, `analyze`, `plan`.

## load

Validate `<skill>` before inspecting `Profiles/` or reading any athlete file.

After validation, route exactly as follows:

| Skill | Internal skill |
|---|---|
| `profile` | `.agents/skills/fitness-coach-profile/SKILL.md` |
| `planning` | `.agents/skills/fitness-coach-planning/SKILL.md` |
| `analyze` | `.agents/skills/fitness-coach-analyze/SKILL.md` |
| `plan` | `.agents/skills/fitness-coach-plan/SKILL.md` |

The selected internal skill owns all further reads and protocol. Except for
the export action below, this dispatcher must not open profiles, plans,
history, artifacts or references.

## scope

- Accept complete, case-sensitive athlete directory basenames, including
  names containing spaces.
- Allow `profile <Nome>` when `<Nome>` is a safe new athlete name without an
  existing directory.
- Require an existing immediate `Profiles/<Nome>/` directory for `planning`,
  `analyze` and `plan`.
- Support export after a valid route with
  `$fitness-coach <skill> <Nome> export`. Treat trailing `esporta profilo` and
  `/fitness-export` as equivalent export actions.

## deny

- Missing or invalid skill: output only
  `$fitness-coach <skill> <Nome>` and the four valid values `profile`,
  `planning`, `analyze`, `plan`. Do not inspect `Profiles/`.
- Missing athlete name after a valid skill: list only basenames of immediate
  directories under `Profiles/`, without reading their files. If `Profiles/`
  is missing or has no immediate directories, report that no athletes are
  available.
- Reject absolute paths; names containing `/` or `\`; names equal to `.` or
  `..`; traversal; partial or fuzzy matches; case-insensitive matches; and any
  inferred identity.
- Do not diagnose medical conditions or advise drugs or steroids. Route
  detailed nutrition planning to `meal-planner`.
- Do not answer generic fitness requests without a valid route. Request the
  canonical command and athlete; provide no technical coaching.

## procedure

1. Parse and validate `<skill>`. On failure, apply the skill error in `deny`
   and stop.
2. Parse the complete `<Nome>`, excluding a recognized trailing export action.
3. If `<Nome>` is absent, apply the missing-athlete behavior in `deny` and
   stop.
4. Apply every name rejection in `deny` before filesystem lookup.
5. Match `<Nome>` exactly to one real, immediate directory under `Profiles/`.
   Do not search recursively, normalize, guess or select a near match.
6. If no directory matches, continue only for `profile`; for every other
   skill, report that the athlete does not exist and stop.
7. Without an export action, open the mapped internal `SKILL.md` and hand off
   all remaining reads and behavior to it.
8. With an export action, require the exact athlete directory and verify both
   `Profiles/<Nome>/profile.md` and `Profiles/<Nome>/plan.md` exist before
   reading either. If either is missing, report the missing file explicitly
   and emit no export blocks. Otherwise read only those two files and output:

   ```text
   === PROFILO ESPORTATO ===
   [contenuto di Profiles/<Nome>/profile.md]
   === PIANO ATTIVO ===
   [contenuto di Profiles/<Nome>/plan.md]
   === FINE ESPORTAZIONE ===
   ```

For web research performed by a routed internal skill, use authoritative
primary sources and cite them. Keep tone direct and non-judgmental.

## done

- Skill and athlete were validated in that order.
- Exactly one internal skill received the request, or one complete isolated
  export was produced.
- No unrelated athlete data or dispatcher-owned fitness advice was read or
  emitted.
