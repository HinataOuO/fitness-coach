---
name: fitness-coach-analyze
description: >
  Validate and analyze one complete weekly athlete report, rotate immutable
  weekly history, and update only confirmed current profile state. Use only
  after `$fitness-coach analyze NOME` routes here.
---

## purpose

Analyze one complete weekly report for the explicitly selected athlete. Keep
every supplied diary field, publish the report as current weekly history,
rotate the previous report without loss, and update only confirmed current
state in `profile.md`. Never change the mother plan.

## load

- Receive the already validated, case-sensitive `<Nome>` from the dispatcher.
  Do not normalize, infer, enumerate or change it.
- Read only `Profiles/<Nome>/profile.md` and `Profiles/<Nome>/plan.md` first.
  Read `Profiles/<Nome>/history/last-week.md` only when it exists. Do not read
  other profiles, weekly archives, plan archives or artifacts; archive paths
  may be checked for existence without reading them.
- Load `references/recovery-and-deload.md` only when the report shows unusual
  fatigue, poor recovery, falling performance or a plateau.
- Load `references/common-injuries.md` only when pain, injury, swelling,
  weakness, numbness, tingling or an aggravating movement is reported.
- Load `references/mobility-and-flexibility.md` only when mobility worsened,
  cool-down adherence is poor or mobility feedback requires adaptation.
- Load any other reference only when one explicit report datum makes it
  necessary. For scientific explanations requested by the athlete, use
  authoritative primary sources, cite them, and label uncertain or empirical
  conclusions.

## scope

- Accept one complete report for exactly the `Plan week: W<N>` recorded in the
  selected profile, where `N >= 1`.
- Compare planned and performed work, adherence, volume, RPE, performance,
  sleep, stress, energy, pain, mobility, recovery and weight. Assess a plateau
  only from at least two comparable weeks of stagnation.
- When the report documents travel or an unplanned stop, assess its duration
  and constraints, recommend an adapted maintenance option when applicable,
  and prescribe a gradual return with a recalculated timeline.
- Render one compact, complete `history/last-week.md` using canonical sections:
  interval and report date, daily data, metrics, pain and mobility, athlete
  notes, and coach analysis.
- Preserve every original report datum. Map structured values to the nearest
  canonical section and retain unknown or extra fields verbatim under `Note
  atleta`; never discard, silently normalize or replace detail with a summary.
- Update only the latest confirmed weight, strictly improved confirmed
  benchmarks with their dates, `Last log`, `Plan week`, and flags made
  necessary by explicit current facts in `profile.md`.
- Keep next-week recommendations inside `Analisi coach` for later consumption
  by `fitness-coach-plan`.

## deny

- Missing or malformed `profile.md` or `plan.md`, mismatched athlete/cycle
  state, `Plan week: W0`, or a missing planned-session definition stops the
  analysis with zero writes. List each exact conflict or missing field.
- Report week must equal the profile's `Plan week`. Its start and end must be
  valid dates in chronological order, cover the reported week, and its final
  date must equal `Data report`. Contradictions or ambiguous dates stop with
  zero writes.
- Require every session prescribed for that week, including each skipped
  session explicitly marked as skipped with its reason. For every performed
  exercise require prescribed work, performed work and RPE. Require complete
  recovery data for energy, sleep and stress; latest weight; pain status and
  details when present; cool-down adherence, mobility trend and mobility
  notes; and athlete notes or an explicit `nessuna`. List every missing item
  before requesting corrections. Never fill gaps by inference.
- W1 requires no existing `history/last-week.md`; any existing file is a
  conflict. W2 and later require one valid previous `last-week.md` for exactly
  W<N-1>, with a coherent final date. Missing, malformed or wrong-week history
  stops with zero writes.
- Never overwrite an existing weekly archive. A destination collision stops
  before any write and reports its exact path.
- Do not update weight from an estimate, benchmark from an unconfirmed or
  incomparable test, or benchmark that did not strictly improve. Do not infer
  goals, diagnoses, training type, skills or goal flags from weekly behavior.
  Preserve every unrelated profile byte, including frontmatter and historical
  profile text.
- Do not modify `plan.md`, revise the mother plan, create JSON or HTML, create
  reminders, schedule follow-ups or re-profile the athlete.
- Do not diagnose medical conditions, prescribe drugs or steroids, or train
  through unresolved warning signs. Acute pain, swelling, sudden strength
  loss, persistent night pain, numbness or tingling requires a doctor or
  physiotherapist recommendation and a prudent next-week reduction, pause or
  non-aggravating alternative in `Analisi coach`.
- Any validation, rendering, publication or verification error must leave the
  original profile, plan and current report byte-for-byte unchanged and must
  not remove a pre-existing file.

## procedure

1. Read the selected profile and plan as specified in `load`; snapshot their
   complete bytes in memory. Validate canonical identity and cycle metadata,
   parse `Plan week: W<N>`, and derive the complete set of sessions prescribed
   for W<N>. Inspect whether `history/last-week.md` exists and read it only if
   present. Do not write during preflight.

2. Validate the submitted report completely before analysis. Require:

   - exact week W<N>, interval start, interval end and matching report date;
   - one entry for every prescribed session, with skipped sessions explicit;
   - for each performed exercise, prescribed sets/reps/holds/load, performed
     sets/reps/holds/load and RPE;
   - energy, sleep, stress, latest confirmed weight, pain status, mobility and
     cool-down feedback, athlete notes and every supplied extra field.

   Compare report entries to planned session names and prescriptions. If any
   datum is absent, contradictory or ambiguous, output one precise combined
   list of missing data and conflicts, request corrections, and stop with zero
   filesystem writes.

3. Validate history state. For W1 require `last-week.md` to be absent. For W2+
   parse the complete previous report and require heading week W<N-1>, valid
   interval and a final date matching its `Data report`. Derive archive path
   only from that previous report:
   `Profiles/<Nome>/history/weeks/W<N-1>-<previous-final-date>.md`. Check that
   exact destination does not exist. Never guess a week or date from the
   filename, current report or profile.

4. Analyze the valid data. Calculate adherence from planned versus completed
   sessions and prescribed versus performed work; compare comparable weekly
   volume, load, repetitions or hold time; inspect target versus actual RPE;
   identify performance direction; and assess sleep, stress, energy, weight,
   pain, mobility and recovery together. Use the previous week only for direct
   comparisons. A plateau requires two or more comparable stagnant weeks;
   before recommending change, identify whether adherence, sleep, nutrition
   context, stress, recovery or programming evidence best explains it. Load
   only references activated by the signals described in `load`.

5. Produce direct, non-judgmental coaching analysis appropriate to the
   athlete's recorded level. State evidence, uncertainties and contradictions.
   Put specific recommendations for W<N+1> in `Analisi coach`, including
   progression, unchanged work, regression, recovery, deload or prudent pain
   adaptation when supported. For travel or an unplanned stop, include an
   adapted maintenance option when applicable, a gradual return after the
   interruption and the resulting timeline change. Recommendations do not
   authorize edits to `plan.md`.

6. Render the new report in memory with exactly this structure, while retaining
   every submitted value and original detail:

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

   Preserve meaningful ordering and units. Mark explicitly reported unknown,
   not applicable, skipped and absent-by-design values; never convert them to
   invented values. Perform a field-by-field round trip against the input and
   block publication if any source field is missing from the rendered report.

7. Build the updated profile in memory from its exact byte snapshot. Change
   only:

   - the canonical `Peso` value when the report supplies a newer confirmed
     measurement;
   - an existing comparable benchmark only when a confirmed result is strictly
     better, preserving its baseline and recording the actual test date (or
     report final date when explicitly confirmed as the test date);
   - `Last log` to the report final date;
   - `Plan week` from W<N> to exactly W<N+1>;
   - only a flag whose current value is contradicted by an explicit confirmed
     current fact, without creating or changing an athlete goal.

   Do not rewrite sections, reflow Markdown, update frontmatter, normalize
   whitespace or alter unrelated bytes. Require exactly one unambiguous match
   for every changed field; otherwise stop with zero writes.

8. Before persistence, re-read and byte-compare `profile.md`, `plan.md` and the
   existing `last-week.md` state with their snapshots; recheck all destination
   paths. Concurrent change or collision stops with zero writes. Create unique
   same-filesystem transaction temporaries containing the validated new report,
   updated profile and exact original snapshots. Validate all temporaries and
   the report round trip before publication.

9. Publish W1 as one rollback-protected logical transaction: atomically create
   `history/last-week.md` with no-replace semantics, then atomically replace
   `profile.md`, then verify both files and byte-compare `plan.md` to its
   snapshot. On any error, atomically restore the exact original profile,
   remove only `last-week.md` created by this transaction and transaction
   temporaries, verify restoration and report failure.

10. Publish W2+ as one rollback-protected logical transaction: first create the
    immutable archive from an exact byte-for-byte copy of the previous
    `last-week.md` using atomic no-replace publication; then atomically replace
    `last-week.md`; then atomically replace `profile.md`. Verify archive
    equality, complete new report, allowed profile-only changes and byte-exact
    `plan.md`. On any error, atomically restore the exact original
    `last-week.md` and `profile.md`, remove only the archive created by this
    transaction plus transaction temporaries, verify all restoration and
    report failure. Never remove a pre-existing archive.

11. On success, remove transaction temporaries and output the coach analysis,
    published report path, archive path when W2+, new `Last log`, and new
    `Plan week`. Report that `plan.md` remained byte-for-byte unchanged.

## done

- One complete report matched the selected athlete, active plan week, dates
  and every prescribed session before any write.
- Saved report passed field-by-field round trip and contains all daily data,
  metrics, pain/mobility feedback, athlete notes, extra fields and coach
  analysis without lossy summarization.
- W1 created only a new current report; W2+ also created one immutable,
  byte-exact archive of W<N-1>. No existing destination was overwritten.
- Profile changed only confirmed current state permitted by this skill, with
  `Last log` equal to report final date and `Plan week: W<N+1>`.
- Mother plan remained byte-for-byte unchanged. Success reported all paths and
  new state; failure left prior state exact and no transaction-created files.
