# Persisted athlete profile schema

Load this file only when creating, importing or structurally repairing an
athlete profile. Replace `<Nome>` with the explicitly selected athlete.

## Canonical structure

```text
Profiles/<Nome>/
├── profile.md
├── plan.md
├── artifacts/
└── history/
    ├── last-week.md
    ├── weeks/
    │   └── W<N>-<YYYY-MM-DD>.md
    └── plans/
        └── <YYYY-MM-DD>-<3|6|9|12>m.md
```

`artifacts/` contains generated weekly JSON and HTML files for this athlete.

## `Profiles/<Nome>/profile.md`

```markdown
---
updated: YYYY-MM-DD
---
# Profilo — [Nome]

## Dati fisici
- Età:
- Peso: kg | Altezza: cm | BF%:
- Struttura: esile / media / robusta

## Livello e contesto
- Livello: [1–5] — [Beginner/Novice/Intermediate/Advanced/Elite]
- Training type: bodyweight | gym | both
- Equipment: [list]
- Anni sport totali: | Anni strutturato:
- Giorni/settimana: | Durata sessione:

## Obiettivi
- Principale:
- Secondario:
- Orizzonte:

## Benchmarks
- [baseline] → [current value] ([latest date])

## Infortuni e limitazioni
- Correnti:
- Passati:

## Preferenze
- Evitare:
- Stile coaching: spiegato / diretto
- Conosce RPE: sì / no

## Stato piano
- Plan start: YYYY-MM-DD
- Plan end: YYYY-MM-DD
- Plan duration: 3|6|9|12 months
- Plan week: W<N>
- Last log: YYYY-MM-DD

## Flags
- has_injury: false
- training_type: gym | bodyweight | both
- active_skills: []
- running_goal: false
- mobility_goal: false
- level: 1
```

## `Profiles/<Nome>/plan.md`

Contains only the current cycle's mother plan. Completed cycles belong in
`history/plans/`.

```markdown
---
updated: YYYY-MM-DD
cycle_start: YYYY-MM-DD
cycle_end: YYYY-MM-DD
duration_months: 3|6|9|12
goal: [primary goal]
---
# Piano madre — [Nome]

## Ciclo
[Dates, duration and periodization model]

## Obiettivo
[Primary and secondary outcomes]

## Struttura
[Frequency and session names]

## Sessioni
[Exercises, sets, reps, loads and rest periods]

## Progressione
[Cycle progression for key lifts or skills]

## Note coach
[Relevant adjustments and watch-points]
```

## `Profiles/<Nome>/history/last-week.md`

Contains the most recent complete weekly report.

```markdown
# Report settimana W<N> — [Nome]

- Intervallo: YYYY-MM-DD → YYYY-MM-DD
- Data report: YYYY-MM-DD

## Dati giornalieri
[Sessions, loads, reps, RPE, recovery and adherence by day]

## Metriche
[Current measurements and weekly changes]

## Dolore e mobilità
[Pain, limitations, mobility and safety signals]

## Note atleta
[Feedback and relevant events]

## Analisi coach
[Assessment, decisions and next-week adjustments]
```

Before replacing `last-week.md`, copy its full contents to
`history/weeks/W<N>-<YYYY-MM-DD>.md`. `<YYYY-MM-DD>` is the report's final
date, recorded as `Last log` in `profile.md`. Weekly archives are immutable:
never overwrite an existing destination. Stop and resolve the conflict first.

## `Profiles/<Nome>/history/plans/<YYYY-MM-DD>-<3|6|9|12>m.md`

Stores one completed mother plan per file. `<YYYY-MM-DD>` is the cycle start
date and the suffix is its duration. Archived plans are immutable: never
overwrite an existing destination. Stop and resolve the conflict first.

## Manual R2 migration

Migrate one explicitly selected athlete at a time:

1. Create the canonical `Profiles/<Nome>/` structure.
2. Copy `<Nome>/profile-core.md` to `profile.md` and
   `<Nome>/profile-plan-current.md` to `plan.md`.
3. Split `<Nome>/profile-log-history.md` into `history/last-week.md` and
   immutable `history/weeks/W<N>-<YYYY-MM-DD>.md` files. Do not alter technical
   text.
4. Split `<Nome>/profile-plans-archive.md` into immutable
   `history/plans/<YYYY-MM-DD>-<3|6|9|12>m.md` files. Do not alter technical
   text.
5. Verify source/destination week and plan counts, cycle dates, report dates,
   `Plan start`, `Plan end`, `Plan duration`, `Plan week`, and `Last log`.
6. Compare all contents, then remove the source files only after an exact
   match.
7. Repeat for the next athlete.

Stop that athlete's migration if dates or cycle/week attribution are ambiguous,
or if any destination already exists. Do not invent data, overwrite files,
create aliases or symlinks, or add legacy fallbacks.

## Import/export block

```text
=== PROFILO ESPORTATO ===
[profile.md]

=== PIANO ATTIVO ===
[plan.md]
=== FINE ESPORTAZIONE ===
```
