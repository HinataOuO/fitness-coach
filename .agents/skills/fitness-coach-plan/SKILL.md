---
name: fitness-coach-plan
description: >
  Build and transactionally publish the validated current weekly plan for one
  athlete already selected by the fitness-coach dispatcher. Use only after
  `$fitness-coach plan` routing for a named athlete, with optional explicit
  HTML delivery.
---

## purpose

Build the current week from the selected athlete's mother plan and publish its
validated JSON as the canonical artifact. Publish the matching standalone HTML
only when explicitly requested, always from that same JSON through the project
generator.

## load

- Receive the already validated, case-sensitive `<Nome>` from the dispatcher.
  Do not normalize, infer, enumerate or change it.
- Read only `Profiles/<Nome>/profile.md` and `Profiles/<Nome>/plan.md` first.
- Inspect `Profiles/<Nome>/history/last-week.md` only as follows: for W1 read it
  only when it exists, and use it only when valid and explicitly pertinent to
  W1; for W2+ require and read it as the report for exactly W<N-1>.
- Do not read other profiles, history, archives, references or artifacts.
  Existing canonical artifact paths may be read only to snapshot their bytes
  for rollback and verification.

## scope

- Derive N exclusively from the one exact `Plan week: W<N>` field in
  `profile.md`; accept only N from 1 through 53. Never accept a separate week
  argument.
- Build W<N> exclusively from `plan.md`. Apply only concrete W<N> adaptations
  explicitly written in the pertinent report's `Analisi coach`; otherwise
  preserve the mother-plan prescription.
- Publish only `Profiles/<Nome>/artifacts/week-W<N>.json` and, on explicit HTML
  request, `Profiles/<Nome>/artifacts/week-W<N>.html`.
- Treat JSON as canonical. JSON-only publication removes an existing HTML for
  that week because it would be stale; HTML publication replaces JSON and HTML
  as one rollback-protected logical transaction.
- Keep deterministic IDs stable across equivalent regenerations by preserving
  the legacy algorithm: normalize each key with Unicode NFKC, compress spaces,
  lowercase, encode as UTF-8, and append the first 12 hexadecimal characters
  of its SHA-256 digest to a readable prefix. Keys are
  plan=`<athlete-slug>|<plan-identity>`,
  session=`<plan-id>|<day>|<session-name>`, and
  exercise=`<session-id>|<zero-based-position>|<exercise-name>`. Build the
  athlete slug with Unicode NFKD, lowercase ASCII alphanumerics, `-` for each
  non-alphanumeric sequence, discarded non-transliterable non-ASCII letters,
  compressed hyphens and no edge hyphens; reject an empty slug.

## deny

- Missing, duplicate, malformed or out-of-range `Plan week`; missing or
  malformed profile or mother plan; athlete/cycle mismatch; or missing W<N>
  prescription stops with zero writes and lists the exact conflict.
- W2+ without one valid `last-week.md` for exactly W<N-1> stops with zero
  writes. Require its canonical heading, coherent interval and matching final
  `Data report`. For W1, absence is allowed; ignore an existing report unless
  it passes those structural checks and explicitly contains adaptations for
  current W1.
- Do not invent sessions, exercises, loads, constraints, progressions or
  adaptations. Do not treat athlete notes or implicit trends as adaptations.
- Do not modify profile, mother plan, history, schema, generator or template.
  Do not write HTML manually or publish unvalidated JSON, HTML generated from
  another payload, a partial transaction or any path outside the selected
  athlete's `artifacts/` directory.
- Any preflight, serialization, validation, generation, publication or
  verification error must restore every pre-existing canonical artifact
  byte-for-byte, restore prior absence where applicable, and leave no
  transaction temporary.

## procedure

1. Read and snapshot the allowed profile and mother plan. Parse the entire
   profile and require exactly one full-line `Plan week: W<N>` with N in 1-53.
   Validate athlete identity, matching cycle metadata and a complete W<N>
   prescription in the mother plan before any write.

2. Apply the history rules in `load` and `deny`. For a usable report, read its
   complete `Analisi coach` and apply only adaptations that explicitly target
   W<N> and identify the affected session or exercise and changed prescription.
   Keep every other mother-plan value unchanged.

3. Build the complete weekly JSON in memory, preserving the deterministic ID
   algorithm in `scope`. Resolve `Profiles/<Nome>/artifacts/`, canonical files
   and every future temporary with `Path.resolve()` and require each candidate
   to satisfy `candidate.is_relative_to(artifacts.resolve())`. Reject any path
   failure before writing.

4. Re-read and byte-compare profile, plan and any consumed report with their
   snapshots. Snapshot the existence and exact bytes of both canonical
   artifacts. Concurrent change stops with zero writes. Create all unique
   transaction files inside `artifacts/` using exclusive creation. Serialize
   only JSON manually as UTF-8, then flush and `fsync` it before validation.
   Flush and `fsync` byte-exact rollback copies; after generator success,
   `fsync` its HTML output without editing it.

5. Validate the temporary JSON only with this exact command:

   `python3 scripts/generate_week_plan.py <temp-json>`

   Require exit status zero. Do not substitute schema libraries or another
   validator.

6. For an explicit HTML request, generate the temporary HTML only with:

   `python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>`

   Require exit status zero, confirm the input is the same validated temporary
   JSON from step 5, and never render or edit HTML manually. For JSON-only,
   create no HTML temporary.

7. Publish with `os.replace` and rollback protection. Keep byte-exact rollback
   copies for each pre-existing canonical file and record which files were
   absent. In JSON-only mode, replace the canonical JSON, then remove canonical
   HTML if it existed. In HTML mode, replace canonical JSON, then canonical
   HTML. After each operation verify bytes and required presence or absence.
   If any operation or verification fails, atomically restore every prior file
   from its rollback copy and remove only canonical files created by this
   transaction where prior state was absent; verify byte identity and absence.
   Report failure only after restoration succeeds. Never delete or overwrite a
   rollback copy before the whole transaction verifies.

8. In a `finally` cleanup, remove every transaction-created JSON, HTML and
   rollback temporary from `artifacts/`, whether validation, generation,
   publication or rollback succeeded. On success report canonical JSON and,
   when requested, HTML paths plus W<N>; otherwise confirm no canonical state
   changed.

## done

- Week came only from one valid profile `Plan week`, mother plan and permitted
  explicit prior analysis; W1 worked without history and W2+ used valid W<N-1>
  history.
- Canonical JSON passed the exact validator command and has stable IDs. HTML is
  absent after JSON-only publication, or exists and came from the exact same
  JSON through the exact generator command after explicit request.
- Every canonical path is under `Profiles/<Nome>/artifacts/`; success left no
  temporary, while every failure preserved previous artifacts byte-for-byte
  and restored previous absence.
