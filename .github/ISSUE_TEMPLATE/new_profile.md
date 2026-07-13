---
name: New Athlete Profile
about: Request profiling for a new athlete through the canonical R2 command
title: "[PROFILE] "
labels: profile, P1-high
assignees: HinataOuO
---

## Athlete

- **Exact name / alias:**

## Canonical Command

```text
$fitness-coach profile <Nome>
```

Replace `<Nome>` with the exact, case-sensitive name above. The name must be
safe and `Profiles/<Nome>/` must not already exist.

## Expected Workflow

- [ ] Complete mandatory interview Blocks A–I
- [ ] Confirm first summary
- [ ] Pass goal and recoverability checks
- [ ] Confirm final summary and profile creation
- [ ] Create `Profiles/<Nome>/profile.md` and required empty R2 directories atomically
- [ ] Hand off to `fitness-coach-planning`

## Notes

<!-- Relevant request context only. Collect private athlete data during the profiling interview. -->
