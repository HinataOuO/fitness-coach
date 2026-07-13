---
name: fitness-coach-planning
description: >
  Build one confirmed initial mother plan or replace one expired cycle for an
  already selected athlete. Use only after fitness-coach planning routing or
  the fitness-coach-profile handoff.
---

## purpose

Build the complete mother plan for one explicitly selected athlete. Create an
initial cycle from a complete W0 profile, or archive and replace only an
expired cycle. Keep all work in conversation until the athlete explicitly
confirms the complete plan and filesystem changes.

## load

- Receive the already validated, case-sensitive `<Nome>` from the dispatcher
  or `fitness-coach-profile`. Do not normalize, infer, enumerate or change it.
- Read only `Profiles/<Nome>/profile.md` first. Athlete data from any other
  directory is forbidden.
- Always load `references/goal-compatibility.md` and
  `references/mobility-and-flexibility.md` after the selected profile.
- Load only references required by that profile and proposed cycle:
  - `references/bodyweight-progressions.md` for `bodyweight`, `both` or active
    calisthenics skills;
  - `references/gym-progressions.md` for `gym` or `both`;
  - `references/advanced-programming.md` for level 3-5, advanced skills,
    autoregulation, complex multi-goal periodization or a 6-12 month cycle;
  - `references/recovery-and-deload.md` for high volume, level 4-5, unusual
    fatigue, sleep, stress or recovery constraints;
  - `references/common-injuries.md` only when injuries, pain or limitations
    are recorded;
  - `references/running-and-endurance.md` only for a running or endurance goal;
  - `references/legs-and-glutes.md` only for a lower-body strength,
    hypertrophy or glute goal;
  - `references/lower-body-bodyweight-plyometrics.md` only for bodyweight
    lower-body power, jumping or plyometric work.
- Inspect only existence of `Profiles/<Nome>/plan.md` until state mode is
  known. Read that file only for a revision candidate, then verify its
  frontmatter against the selected profile.
- Load `references/profile-schema.md` only after explicit confirmation,
  immediately before persistence.

## scope

- Initial mode requires a complete canonical `profile.md`, `Plan week: W0`,
  unset cycle metadata and no `plan.md`.
- Revision mode requires `plan.md`, valid matching cycle metadata and a
  current date later than the inclusive `Plan end`.
- Select exactly `3`, `6`, `9` or `12` months through stated coaching judgment
  based on level, goals and horizon. The athlete may express a preference but
  does not choose duration arbitrarily.
- Build a cycle-specific mother plan with dates, periodization, recoverable
  frequency, complete sessions, progression, deload and recovery criteria.
- On confirmed initial planning, create `plan.md` and change cycle metadata in
  `profile.md`, including `Plan week: W1`.
- On confirmed revision, first archive the expired plan, then replace
  `plan.md` and cycle metadata in `profile.md`, including `Plan week: W1`.

## deny

- Missing, incomplete or malformed canonical profile: stop with zero writes
  and list exact missing or invalid fields. Do not infer data or repair it.
- Every state other than the two modes in `scope` is inconsistent. Stop with
  zero writes and report the conflicting files/metadata explicitly.
- When current date is on or before `Plan end`, refuse revision with zero
  writes. State first eligible date, exactly the day after `Plan end`, and
  route emergencies or weekly constraints to `fitness-coach analyze <Nome>`.
- Reject any duration outside `3`, `6`, `9` or `12` months. Reject an athlete
  duration demand that conflicts with coaching judgment, goal compatibility,
  recoverability or realistic horizon; explain why and propose allowed viable
  duration(s). Do not use a rigid level-to-duration matrix.
- Do not exceed level-specific session, duration, muscle-set or total-set
  ceilings from `references/goal-compatibility.md`. Do not proceed with an
  incompatible goal combination, excess active goals or unrealistic horizon.
- Do not diagnose, prescribe around unresolved pain, or advise drugs or
  steroids. Refer warning signs to a qualified clinician. Detailed nutrition
  belongs to `meal-planner`.
- Do not create weekly reports, weekly adaptations, JSON, HTML or artifacts.
  These belong to `analyze` and `plan`.
- Missing, negative or ambiguous confirmation causes zero writes. Any athlete
  correction changes the proposal and invalidates every previous confirmation.
- Never overwrite an archive or publish over an unexpected `plan.md` state.
  Any collision or failed validation aborts the transaction.

## procedure

1. Read the selected profile as specified in `load`. Validate every canonical
   section and field needed for planning, including level, training type,
   equipment, availability, goals, horizon, benchmarks, injuries,
   preferences, state and flags. Values explicitly marked unknown or declined
   remain unknown; planning-critical gaps block planning.

2. Determine mode without writing:

   - Initial: require `Plan week: W0`, `Plan start`, `Plan end` and
     `Plan duration` all exactly `non impostato`, and no `plan.md`.
   - Revision: require `plan.md`; parse `Plan start`, `Plan end`,
     `Plan duration` and `Plan week`; require `Plan week: W<N>` with `N >= 1`
     and duration in the allowed set;
     require profile values to match `cycle_start`, `cycle_end` and
     `duration_months` in plan frontmatter; require current date later than
     `Plan end`.

   Apply the relevant `deny` rule to every other combination. Treat `Plan end`
   as inclusive and compute revision eligibility as `Plan end + 1 day`.

3. Load mandatory and conditional references. Re-run, in order, goal-pair
   compatibility, maximum active goals by level, realistic horizon,
   recoverable volume ceilings and multi-goal penalty. Resolve every failure
   with athlete choice before constructing a plan; changed goals or priorities
   require all five checks again.

4. Select `3`, `6`, `9` or `12` months. State coaching rationale using the
   athlete's level, goal magnitude/compatibility and horizon. Use no automatic
   matrix. Reject all other durations and any user preference that would make
   the plan unsafe, unrecoverable or unrealistic.

5. Build the complete plan in memory. Use the date of eventual confirmation
   as `cycle_start`; compute inclusive `cycle_end` by adding the selected
   calendar months, preserving the day when it exists and otherwise using the
   destination month's last day. Include:

   - primary and compatible secondary outcomes, cycle dates and duration;
   - a coherent model: linear only for levels 1-2; DUP, blocks or
     autoregulation only where level and objective justify them;
   - weekly frequency within the athlete's recoverable ceiling, plus the
     minimum realistic sessions and minutes needed for the objective. If
     availability is insufficient, state the minimum and offer a smaller goal
     or longer horizon instead of weakening requirements silently;
   - specificity to goals, weekly/microcycle progressive overload, and a rule
     that technique must be correct before load or exercise progression;
   - for every session, an estimated duration and a dynamic warm-up with
     5-8 minutes of specific mobility plus appropriate ramp-up work;
   - every exercise with name, sets, repetitions or hold time, external load
     or bodyweight variant, target RPE/RIR and explicit rest. Use 3-4 minutes
     for static skills and never less than 3, 2-3 minutes for heavy strength,
     90 seconds-2 minutes for hypertrophy/volume and never more than 2 minutes,
     60-90 seconds for shoulder accessories,
     handstand and core, 2-3 minutes for reactive plyometrics or 90 seconds for
     volume plyometrics, and 30 seconds between mobility exercises;
   - session-duration estimates using work-set recovery, execution time,
     approximately 10 minutes warm-up and at least 5 minutes cool-down as the
     calculation basis; cross-check against level maximum session duration;
   - a written mobility block in every session, normally a 5-10 minute
     cool-down of static stretching, with exercises, sets and duration chosen
     first for trained muscles, then skill demands, sedentary tight areas and
     declared mobility goals. Move it to the start only when the profile shows
     the athlete historically skips cool-down; in an HS + core + mobility
     session keep mobility as the final block. Add dedicated mobility on a
     recovery day or for a mobility goal, with baseline, progression and tests
     every 2-4 weeks. Keep pre-workout static holds under 60 seconds per muscle;
   - starting loads grounded in recorded benchmarks. Mark uncertain estimates
     conservatively as `stimato @RPE7`; round gym loads to practical available
     increments and use regressions/progressions for bodyweight work;
   - explicit progression rules for load, reps, holds or exercise difficulty,
     including stall and technique gates;
   - planned deloads every 4-8 weeks, with frequency normally unchanged and
     volume reduced 30-40% for moderate fatigue, 50-60% for high fatigue or
     70-90% for extreme fatigue; reduce intensity only when needed;
   - recovery criteria covering sleep, stress, performance trend, pain and
     accumulated fatigue. State thresholds that trigger a deload, clinician
     referral or later `analyze` review without embedding weekly adaptations;
   - when the profile marks a sedentary baseline, an initial 4-6 week
     movement-acclimation phase using basic bodyweight work, walking and
     stretching, no external load, and consistency over intensity.

6. Render the in-memory plan in the canonical `plan.md` structure with
   frontmatter fields `updated`, `cycle_start`,
   `cycle_end`, `duration_months` and `goal`, followed by `Ciclo`, `Obiettivo`,
   `Struttura`, `Sessioni`, `Progressione` and `Note coach`. Keep weekly report
   reactions out of the mother plan.

7. Show the athlete the entire proposed plan, selected duration and rationale,
   exact dates, and exact planned writes. For revision, include the immutable
   archive destination
   `Profiles/<Nome>/history/plans/<old-cycle-start>-<old-duration>m.md`.
   Ask for explicit confirmation of both plan and writes. Do not persist a
   partial preview. If confirmation occurs on a different date than the shown
   `cycle_start`, recompute dates, show the changed proposal and request a new
   confirmation.

8. After explicit confirmation, load `references/profile-schema.md`, re-read
   selected `profile.md` and recheck relevant paths/state to detect concurrent
   changes. Build and validate new `plan.md` and updated `profile.md` in unique
   temporary sibling files on the same filesystem. Update profile frontmatter
   `updated`, set `Plan start`, `Plan end`, `Plan duration` and exactly
   `Plan week: W1`, and preserve every unrelated byte and field. Keep exact
   snapshots of original files in a unique same-filesystem transaction area.

9. Publish initial mode as one rollback-protected transaction:

   - atomically rename the validated temporary plan to `plan.md` with
     no-replace semantics;
   - atomically replace `profile.md` with the validated updated profile;
   - verify both files and their matching cycle metadata;
   - on any error, restore the exact original profile, remove only the newly
     created plan and transaction temporaries, verify restoration, then report
     failure. Never leave one side updated.

10. Publish revision mode as one rollback-protected transaction:

    - recheck that archive destination does not exist;
    - create the archive from the exact complete old `plan.md` through an
      atomic no-replace rename of a validated temporary copy;
    - only after archive success, atomically replace `plan.md`, then
      atomically replace `profile.md`;
    - verify new files, matching cycle metadata and byte-for-byte archive
      equality with the old plan snapshot;
    - on any error, atomically restore exact old `plan.md` and `profile.md`,
      remove only the archive created by this transaction plus transaction
      temporaries, verify restoration, then report failure. Never remove a
      pre-existing archive or overwrite any destination.

11. On success, remove transaction temporaries and report active cycle dates,
    duration, `Plan week: W1` and archive path when applicable. Do not generate
    or modify weekly reports, JSON, HTML or artifacts.

## done

- Exactly one validated athlete and one eligible initial or expired-cycle mode
  were handled.
- Coach selected and justified one allowed duration; plan contains required
  periodization, sessions, mobility, rests, duration estimates, loads,
  RPE/RIR, progression, deload and recovery criteria.
- Full plan and all writes received explicit current confirmation.
- Initial publication left matching `plan.md` and profile cycle metadata, or
  revision also left one immutable byte-exact archive of the expired plan.
- Failure or refusal left pre-request athlete state unchanged and no temporary
  files; unrelated athlete data and weekly artifacts were untouched.
