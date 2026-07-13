# Fitness Coach Skill

Fitness Coach is a persistent, multi-athlete Codex coaching system for
calisthenics, gym training, running and general athletic development. R2 uses
an explicit command, four focused internal skills and athlete-local data.

## Usage

```text
$fitness-coach <skill> <Nome>
```

`<Nome>` is the exact, case-sensitive athlete directory name. Valid skills:

| Skill | Responsibility |
|---|---|
| `profile` | Run the mandatory new-athlete interview and create the confirmed profile |
| `planning` | Create the initial mother plan or replace an expired cycle after confirmation |
| `analyze` | Validate one complete weekly report, rotate history and update confirmed current state |
| `plan` | Build and publish the current validated weekly artifact, optionally as HTML |

Examples:

```text
$fitness-coach profile Mario Rossi
$fitness-coach planning Mario Rossi
$fitness-coach analyze Mario Rossi
$fitness-coach plan Mario Rossi
$fitness-coach plan Mario Rossi export
```

The dispatcher validates the skill before the athlete name and routes exactly
one internal skill. It does not infer identity or answer generic coaching
requests without a valid route.

## R2 Architecture

```text
fitness-coach/
├── SKILL.md
├── .agents/skills/
│   ├── fitness-coach-profile/SKILL.md
│   ├── fitness-coach-planning/SKILL.md
│   ├── fitness-coach-analyze/SKILL.md
│   └── fitness-coach-plan/SKILL.md
├── Profiles/<Nome>/
│   ├── profile.md
│   ├── plan.md
│   ├── artifacts/
│   │   └── week-W<N>.{json,html}
│   └── history/
│       ├── last-week.md
│       ├── weeks/
│       │   └── W<N>-<data-report>.md
│       └── plans/
│           └── <cycle-start>-<duration>m.md
├── references/
├── assets/
│   ├── week-plan.schema.json
│   └── fitness-coach-log.html
└── scripts/
    └── generate_week_plan.py
```

Each athlete owns one canonical profile, one active mother plan, immutable
per-file weekly and cycle history, and generated weekly artifacts. Athlete
data is never selected by fuzzy matching.

## Weekly Artifact Pipeline

The `plan` skill builds `Profiles/<Nome>/artifacts/week-W<N>.json` from the
selected athlete's active state. JSON is canonical and must pass:

```text
python3 scripts/generate_week_plan.py <temp-json>
```

HTML is produced only when explicitly requested, from the same validated JSON:

```text
python3 scripts/generate_week_plan.py <temp-json> --output <temp-html>
```

Publication is transactional. Failed validation or generation preserves prior
artifacts byte-for-byte.

## Athlete Levels

Level assignment uses training history and demonstrated benchmarks, never
years alone.

| Level | Label | R2 definition |
|---|---|---|
| 1 | Beginner | 0–6 months, no base; basic motor patterns and low loads |
| 2 | Novice | 6–18 months; linear progression works and technique is developing |
| 3 | Intermediate | 1.5–3 years; periodization is needed and plateaus are common |
| 4 | Advanced | 3–6 years; complex periodization and high specificity |
| 5 | Elite | 6+ years and competitive; fully individualized programming |

## Boundaries

- Training plans integrate goal compatibility, recoverability, mobility,
  progression, deload and injury-aware safety rules.
- The coach does not diagnose medical conditions or advise drugs or steroids.
- Detailed nutrition planning belongs to `meal-planner`.
- Scientific research uses authoritative primary sources with citations.
