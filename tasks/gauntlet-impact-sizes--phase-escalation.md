---
title: "Gauntlet: Growth Phase Escalation (Replaces Impact Sizes)"
id: "070"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Implement phase-based difficulty escalation for the ground growth system, replacing the old impact shape (1×1, 1×2, 2×2) system."
modified: "2026-06-18"
---

# Gauntlet: Growth Phase Escalation

## Problem
In v1, difficulty escalated via larger impact shapes (1×1 → 1×2 → 2×2). In v2, difficulty escalates via **more cells per growth tick** and **shifting layer targeting** — the outer arena fills first, then pressure moves inward.

## Solution
Phase-based growth configuration replacing the old shape weight system:

### Phase Structure
| Phase | Time | Name | Cells/Tick | Primary Target |
|---|---|---|---|---|
| 1 | 0:00–1:00 | Outer Pressure | 4–6 | Outer Layer (75%) |
| 2 | 1:00–2:00 | Middle Pressure | 6–8 | Middle Layer (50%) |
| 3 | 2:00–3:00 | Inner Survival | 8–10 | Inner Layer (35%) |

### Layer Targeting Distribution
**Phase 1 (Outer Pressure):**
- 75% Outer Layer
- 10% Middle Layer (early warning)
- 10% Near-Player pressure
- 5% Random irregular growth

**Phase 2 (Middle Pressure):**
- 50% Middle Layer
- 20% Outer Layer continuation
- 15% Near-Player pressure
- 10% Sticky cluster expansion
- 5% Random irregular growth

**Phase 3 (Inner Survival):**
- 35% Inner Layer
- 25% Middle Layer
- 15% Near-Player pressure
- 15% Sticky cluster expansion
- 10% Random irregular growth

### What Was Removed (v1 → v2)
- `phase_weights` for 1×1, 1×2, 2×2 shapes — replaced by `phase_growth_config`
- `_get_shape_footprint()` — not needed (cells are individual, not shaped)
- Shape-based impact — each cell is selected independently via candidate scoring

### Candy Bubble Disruption (New in v2)
In addition to normal growth, candy bubbles provide anti-camping disruption:
- Phase 1: 0 bubbles
- Phase 2: 2 bubbles total
- Phase 3: 3 bubbles total
- Each bubble grows 2.5–3s then explodes into 3×3 sticky area

## Acceptance Criteria
- Phase 1 fills outer arena, Phase 2 fills middle, Phase 3 pressures inner
- Growth rate increases each phase (4–6 → 6–8 → 8–10)
- Candy bubbles spawn 0/2/3 per phase
- Phase transitions are clearly visible to players

## Migration Checklist
- [ ] Replace `phase_configs` (cannon-based) with `phase_growth_config` (growth-based)
- [ ] Implement layer-based targeting distribution per phase
- [ ] Update `_start_phase()` to configure growth parameters instead of cannon parameters
- [ ] Add bubble spawn timing per phase
- [ ] Remove old impact shape logic
- [ ] Update phase HUD labels: "Outer Pressure" → "Middle Pressure" → "Inner Survival"
