# Fitness Coach Skill

An expert fitness coaching system for Claude Code that provides personalized training plans, weekly monitoring, and evidence-based programming for bodyweight (calisthenics, street lifting, gymnastics) and gym-based training.

## Overview

The skill acts as a persistent, profile-aware coach. It stores user data (goals, level, injuries, training history) across sessions and adapts plans over time. It supports multiple user profiles simultaneously.

## Usage

```
/fitness-coach
```

Invoke from any Claude Code session. The skill auto-detects context (new user vs returning, which phase to enter) and guides the conversation accordingly.

## Phases

| Phase | Trigger | Description |
|-------|---------|-------------|
| **Profiling** | First use or explicit re-profiling | Collects biometric data, training history, goals, equipment, injuries, lifestyle |
| **Planning** | After profiling or plan request | Builds a periodized weekly plan with exercises, loads, RPE, rest, mobility |
| **Monitoring** | Weekly log submission | Processes session logs, adjusts progressions, flags plateaus or overreaching |

## Features

### Training Modalities
- Bodyweight / calisthenics (push, pull, skill, lower progressions)
- Gym hypertrophy, strength, fat loss, body recomposition
- Running and cardio endurance integration
- Lower body plyometrics

### Programming
- Linear, DUP, and block periodization
- RPE-based autoregulation
- Deload protocols and overreaching detection
- 6–12 month periodization templates

### Safety & Injury Management
- Goal compatibility validation (flags incompatible objective combinations)
- Injury-aware plan modification (suspends affected muscle groups)
- Corrective exercise protocols for common injuries (shoulder, elbow, wrist, back, knee)
- Mandatory mobility integration rules

### Analysis
- Visual/technical form analysis via photo protocol
- Postural assessment checklists
- Exercise-specific form cues (calisthenics and gym)

### HTML Training Log
An offline, mobile-friendly training log app (`assets/fitness-coach-log.html`) is generated and updated with each plan. Features:
- Session logging (reps, time, distance, mobility)
- Vitals tracking (energy, sleep, stress, RPE, weight)
- Pain/injury tracking
- Weekly report generation with clipboard export

## File Structure

```
fitness-coach/
├── SKILL.md                        # Main dispatcher and core protocol
├── phases/
│   ├── profiling.md                # User assessment protocol
│   ├── planning.md                 # Plan construction rules
│   └── monitoring.md               # Weekly log processing
├── references/
│   ├── goal-compatibility.md       # Goal matrix, volume limits, timelines
│   ├── bodyweight-progressions.md  # Calisthenics progressive overload
│   ├── gym-progressions.md         # Gym training parameters
│   ├── advanced-programming.md     # Periodization, RPE, templates
│   ├── recovery-and-deload.md      # Sleep, stress, deload protocols
│   ├── common-injuries.md          # Injury management and correctives
│   ├── mobility-and-flexibility.md # Stretching, CARs, foam rolling
│   ├── running-and-endurance.md    # Cardio integration, HR zones
│   ├── legs-and-glutes.md          # Lower body evidence-based guide
│   ├── lower-body-bodyweight-plyometrics.md  # Plyometric progressions
│   ├── visual-technical-analysis.md # Form analysis protocol
│   └── scientific-sources.md       # ACSM, NSCA, research references
├── profile/                        # Active user profile (git-ignored)
│   ├── profile-core.md             # Biometrics, goals, injuries, level
│   ├── profile-plan-current.md     # Active training plan
│   └── profile-log-history.md      # Session and weekly logs
└── assets/
    └── fitness-coach-log.html      # Offline training log app
```

## User Levels

| Level | Label | Description |
|-------|-------|-------------|
| 1 | Beginner | No consistent training history |
| 2 | Novice | 3–12 months consistent training |
| 3 | Intermediate | 1–3 years, basic technique solid |
| 4 | Advanced | 3+ years, advanced skills or heavy compound lifts |

## Evidence Base

Programming references cite ACSM, NSCA, WHO guidelines plus peer-reviewed hypertrophy and strength research (Schoenfeld, Krieger, Helms, Contreras, among others).

## Multi-User Support

Multiple profiles can coexist in separate directories (e.g., `profile/` and `backupPietro/`). Profile directories are git-ignored by default to protect user data.
