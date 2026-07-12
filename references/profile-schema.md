# Persisted athlete profile schema

Load this file only when creating, importing or structurally repairing an
athlete profile. Replace `<athlete>` with the explicitly selected athlete.

## `<athlete>/profile-core.md`

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
- Plan week: W1
- Last log: YYYY-MM-DD

## Flags
- has_injury: false
- training_type: gym | bodyweight | both
- active_skills: []
- running_goal: false
- mobility_goal: false
- level: 1
```

## `<athlete>/profile-plan-current.md`

```markdown
---
updated: YYYY-MM-DD
week: W1
goal: [primary goal]
---
# Piano Attivo — [Nome]

## Struttura
[Frequency, session names, periodization model]

## Sessioni
[Exercises, sets, reps, loads and rest periods]

## Progressione
[Week-over-week progression for key lifts or skills]

## Note coach
[Relevant adjustments and watch-points]
```

## Import block

```text
=== PROFILO ESPORTATO ===
[profile-core.md]

=== PIANO ATTIVO ===
[profile-plan-current.md]
=== FINE ESPORTAZIONE ===
```
