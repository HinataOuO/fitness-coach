---
name: fitness-coach-plan
description: >
  Build and transactionally publish the validated current weekly plan for one
  athlete already selected by the fitness-coach dispatcher. Use only after
  `$fitness-coach plan` routing for a named athlete, with optional explicit
  HTML delivery.
---

## purpose

Build the selected athlete's current week from the mother plan. Publish validated
JSON as canonical; publish HTML only when explicitly requested.

## load

- Receive the dispatcher's validated, case-sensitive `<Nome>` exactly; never
  normalize, infer, enumerate or change it.
- Read once, progressively: `Profiles/<Nome>/profile.md`; after a valid week,
  `plan.md`; then `history/last-week.md` only when the matrix requires it. Retain
  inputs for later silent comparison; never print them.
- Read canonicals only immediately before publication. Snapshot via filesystem
  copies; use silent metadata, hashes or byte comparisons for all checks.
- Never read another profile, archive, reference, schema, template or
  non-canonical artifact.

## scope

- Derive N exclusively from the one exact `Plan week: W<N>` field in
  `profile.md`; require a full line, accept 1-53 and never a separate argument.
- Build W<N> exclusively from the matching athlete/cycle prescription in
  `plan.md`. Apply only concrete adaptations in the pertinent report's complete
  `Analisi coach` that explicitly target W<N>, identify the session/exercise and
  changed prescription; preserve every other mother-plan value.
- Publish only `Profiles/<Nome>/artifacts/week-W<N>.json` and
  `Profiles/<Nome>/artifacts/week-W<N>.html`. Treat JSON as canonical.
- Preserve the legacy deterministic ID algorithm. Normalize every key with
  Unicode NFKC, compress spaces, lowercase, UTF-8 encode, then append the first
  12 hex characters of its SHA-256 digest to a readable prefix. Keys are
  plan=`<athlete-slug>|<plan-identity>`, session=`<plan-id>|<day>|<session-name>`,
  exercise=`<session-id>|<zero-based-position>|<exercise-name>`. For the athlete
  slug use Unicode NFKD, lowercase ASCII alphanumerics, one `-` per
  non-alphanumeric sequence, discard non-transliterable non-ASCII letters,
  compress/trim hyphens, and reject an empty slug.

## deny

- Missing, duplicate, malformed or out-of-range week; malformed profile/plan;
  identity/cycle mismatch; incomplete W<N> prescription; or invalid required
  history stops with one exact conflict list and zero writes.
- Do not invent sessions, exercises, loads, constraints, progressions or
  adaptations; notes and implicit trends are not adaptations.
- Do not modify profile, plan, history, schema, generator or template. Never
  hand-write HTML, publish unvalidated/mismatched data, partially publish, or
  access a path outside the selected athlete's `artifacts/` directory.
- Any error must restore every pre-existing canonical artifact byte-for-byte,
  restore prior absence, and leave no transaction temporary.

## procedure

1. Follow `load`. Parse the entire profile and validate one week before reading
   the plan. Validate identity, cycle and complete prescription. Zero writes
   before preflight completes. History behavior is:

   | Week | `last-week.md` | Use |
   |---|---|---|
   | W1 | read only if it exists | only if canonical heading, coherent interval, matching final `Data report`, and explicit W1 adaptations are all present; otherwise ignore |
   | W2+ | required, report for exactly W<N-1> | require those structural checks; use only explicit W<N> adaptations |

2. Build complete JSON in memory. Resolve `artifacts/`, both canonicals and every
   future temporary with `Path.resolve()`; before writing require every candidate
   to satisfy `candidate.is_relative_to(artifacts.resolve())`. Re-read each
   consumed input once and compare silently with its retained snapshot. Any
   change or path failure stops with zero writes.

3. Create unique transaction files exclusively inside `artifacts/`. Serialize
   only JSON manually as UTF-8; flush and `fsync` before validation. Validate
   only with:

   `python3 scripts/generate_week_plan.py <temp-json>`

   Require exit status zero. For explicit HTML, generate only with:

   `python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>`

   Require exit status zero; use the same validated JSON and `fsync` generator
   output without editing it. JSON-only creates no HTML temporary.

4. Immediately before publication, inspect only both canonical paths. For each
   present file create an exclusive, byte-exact filesystem rollback copy, flush
   and `fsync` it; record absence otherwise. Publish one rollback-protected
   logical transaction with `os.replace` and this matrix:

   | Request | Publication |
   |---|---|
   | JSON-only | replace JSON; remove existing HTML because JSON-only publication removes an existing HTML as stale |
   | JSON+HTML | replace JSON, then HTML from the same temporary JSON |

   | Previous canonical | Rollback |
   |---|---|
   | present | atomically restore its byte-exact copy |
   | absent | remove only the canonical created by this transaction |

   Verify expected bytes and presence/absence after every operation. On failure,
   restore all prior state atomically and verify it before reporting. Never
   overwrite/delete rollback copies before full verification.

5. In `finally`, remove every transaction-created JSON, HTML and rollback file
   on success or error. Success reports W<N> and canonical JSON plus HTML when
   requested; failure reports unchanged canonical state only after restoration.

## done

- Week, identity, cycle, complete prescription, permitted history/adaptations and
  stable IDs passed before publication.
- Exact validator succeeded. HTML is absent for JSON-only or was generated from
  the same JSON by the exact command after explicit request.
- Every path was confined; success and failure leave no transaction temporary;
  failure restores exact previous bytes and absence.
