---
name: fitness-coach-analyze
description: >
  Validate and analyze one complete weekly athlete report, rotate immutable
  weekly history, and update only confirmed current profile state. Use only
  after `$fitness-coach analyze NOME` routes here.
---

## purpose

Analyze one complete report for the explicitly selected athlete and active
`Plan week: W<N>`. Preserve every diary field, rotate immutable history, update
only confirmed current profile state, and never change the mother plan.

## load

- Receive the dispatcher's validated, case-sensitive `<Nome>`; never normalize,
  infer, enumerate or change it.
- First read only `Profiles/<Nome>/profile.md` and `plan.md`, retaining their
  exact bytes. Check whether `history/last-week.md` exists. For W1, stop on
  existence without reading its content; for W2+, read it exactly once.
- Never read another profile, weekly/plan archive or artifact. Archive paths may
  only be checked for existence.
- Load `references/recovery-and-deload.md` only for unusual fatigue, poor
  recovery, falling performance or possible plateau; `common-injuries.md` only
  for pain, injury, swelling, weakness, numbness, tingling or aggravating
  movement; `mobility-and-flexibility.md` only for worsened mobility, poor
  cool-down adherence or mobility feedback requiring adaptation. Load another
  reference only when one explicit datum requires it. Scientific explanations
  requested by the athlete require cited authoritative primary sources and
  uncertainty labels.

## scope

- Compare planned/performed work, adherence, volume, RPE, performance, sleep,
  stress, energy, pain, mobility, recovery and weight. A plateau requires at
  least two comparable stagnant weeks.
- For travel or an unplanned stop, assess duration/constraints and, when
  applicable, recommend maintenance, gradual return and a recalculated timeline.
- Publish one canonical `history/last-week.md`. Preserve every supplied datum:
  map structured values to the nearest section and retain extra/unknown fields
  verbatim under `Note atleta`; no loss, silent normalization or summary in
  place of detail.
- Update only confirmed current state allowed below. Keep W<N+1>
  recommendations in `Analisi coach` for `fitness-coach-plan`.

## deny

- Any invalid input or state stops with zero writes and one exact combined list
  of conflicts/missing fields. Never infer missing data.
- Reject missing/malformed profile or plan, identity/cycle mismatch, W0,
  missing planned-session definitions, report week unequal to `Plan week`, or
  invalid/ambiguous dates. Interval dates must be chronological, cover the
  reported week, and end on `Data report`.
- Require every prescribed session, including explicit skipped status/reason;
  every performed exercise's prescribed and performed sets/reps/holds/load plus
  RPE; energy, sleep, stress, latest confirmed weight, pain status/details,
  cool-down adherence, mobility trend/notes, and athlete notes or `nessuna`.
- Never overwrite an archive or other existing destination. Never update weight
  from estimates, benchmarks from unconfirmed/incomparable/non-improving tests,
  or infer goals, diagnoses, training type, skills or goal flags.
- Do not modify `plan.md`, revise the mother plan, create JSON/HTML/reminders,
  schedule follow-ups or re-profile the athlete. Preserve profile frontmatter,
  history, whitespace and every byte outside permitted field replacements.
- Do not diagnose, prescribe drugs/steroids or train through unresolved warning
  signs. Acute pain, swelling, sudden strength loss, persistent night pain,
  numbness or tingling requires doctor/physiotherapist referral and prudent
  reduction, pause or non-aggravating alternative in `Analisi coach`.
- Any validation, rendering, publication or verification error must restore the
  original profile, plan and current report byte-for-byte, remove only files
  created by this transaction, and never remove a pre-existing file.

## procedure

1. Validate profile/plan identity and cycle, parse N >= 1, and derive all
   prescribed W<N> sessions. Apply the `load` history rule. No preflight writes.

2. Validate the entire report against `deny`, planned names and prescriptions.
   Preserve supplied extra fields. Report all problems together and stop.

3. Validate history using this matrix:

   | State | Required history | Archive destination | Publication |
   |---|---|---|---|
   | W1 | `last-week.md` absent; existence is a conflict, content is not read | none | create current report, replace profile |
   | W2+ | one read of valid W<N-1>, with valid interval and final date equal to its `Data report` | `history/weeks/W<N-1>-<previous-final-date>.md`, derived only from previous content and absent | create byte-exact archive, replace current report and profile |

   Never derive archive metadata from filenames, the current report or profile.

4. Analyze valid data: planned versus completed sessions/work; comparable
   volume, load, reps or hold time; target versus actual RPE; performance and
   recovery signals together. Use previous history only for direct comparison.
   Before changing work for a qualifying plateau, consider adherence, sleep,
   nutrition context, stress, recovery and programming evidence. Produce direct,
   non-judgmental analysis for the recorded level, stating evidence,
   uncertainties and contradictions. Add supported W<N+1> progression,
   unchanged work, regression, recovery, deload, pain and interruption guidance;
   this never authorizes a plan edit.

5. Render in memory with exactly this structure, retaining every submitted
   value, original detail, meaningful order and unit:

   ```markdown
   # Report settimana W<N> — <Nome>

   - Intervallo: YYYY-MM-DD → YYYY-MM-DD
   - Data report: YYYY-MM-DD

   ## Dati giornalieri
   [Every session; prescribed, performed and RPE for every exercise; skipped
   sessions and reasons; daily energy, sleep and stress]

   ## Metriche
   [Latest confirmed weight, weekly changes, adherence and comparable volume,
   load, repetition, hold or performance metrics]

   ## Dolore e mobilità
   [Pain status/details, aggravating movements, cool-down adherence, mobility
   trend and mobility notes]

   ## Note atleta
   [Complete athlete notes, relevant events and every extra/unmapped field]

   ## Analisi coach
   [Evidence-based assessment, safety guidance and W<N+1> recommendations]
   ```

   Keep explicitly reported unknown, not-applicable, skipped and
   absent-by-design values; invent nothing. A field-by-field round trip must
   prove every source field remains before publication.

6. From the exact profile snapshot, require one unambiguous match and change
   only: newer confirmed `Peso`; an existing comparable benchmark when a
   confirmed result strictly improves it, preserving baseline and recording the
   confirmed test date; `Last log` to report final date; `Plan week` from W<N>
   to exactly W<N+1>; or a flag contradicted by an explicit confirmed current
   fact, never an athlete goal. Do not reflow or normalize anything.

7. Immediately before persistence, use non-verbose byte comparisons (never
   print already loaded content) to recheck profile, plan, history state and all
   destinations against snapshots. Concurrent change or collision stops with
   zero writes. In unique same-filesystem temporaries, stage the new report,
   profile and exact snapshots; validate temporaries and round trip.

8. Publish one rollback-protected logical transaction with atomic no-replace
   creation for new destinations and atomic replacement otherwise, following
   the matrix order. Verify the archive copy when applicable, complete report,
   allowed profile-only changes, and byte-exact `plan.md` without emitting file
   contents. On any error, atomically restore exact original profile and, for
   W2+, `last-week.md`; remove only the transaction-created current report (W1)
   or archive (W2+) and temporaries; verify restoration and report failure.
   Never remove a pre-existing archive.

9. On success remove temporaries and output coach analysis, current report path,
   archive path for W2+, new `Last log`, new `Plan week`, and confirmation that
   `plan.md` remained byte-for-byte unchanged.

## done

- Validation and field-by-field round trip passed before writes; all sessions,
  exercises, recovery, safety, mobility, notes and extra fields are present.
- W1 created only current history; W2+ also archived exact W<N-1>; no existing
  destination was overwritten.
- Only permitted confirmed profile fields changed; `Last log` and W<N+1> are
  correct; `plan.md` is byte-identical.
- Success reports paths/state. Failure restores exact prior state and leaves no
  transaction-created file.
