---
title: "Gauntlet: Impact Sizes & Phase Escalation"
id: "070"
status: "done"
priority: 01
sprint: alpha
category: CORE
description: "Implement variable impact shapes (1x1, 1x2, 2x2) and the phase-based difficulty escalation."
modified: "2026-06-03"
---

# Gauntlet: Impact Sizes & Phase Escalation

## Problem
Single-cell impacts would leave the arena too open. To reach 80% sticky coverage in 3 minutes, the cannon must "cut" routes using larger shapes. The difficulty must also escalate to prevent mid-game stagnation.

## Solution
Implement a weighted random selection system for impact shapes that shifts based on the current match phase.

### Phase-Based Weights
| Phase | Timing | 1×1 | 1×2 | 2×2 | Goal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1: Open** | 0:00–1:00 | 60% | 40% | 0% | Slow pressure |
| **2: Pressure** | 1:00–2:00 | 30% | 55% | 15% | Route cutting |
| **3: Survival** | 2:00–3:00 | 15% | 55% | 30% | Endgame pressure |

### Implementation Details
1. **Phase Manager:** Track `current_phase` in `GauntletManager` based on `elapsed_time`. Broadcast `rpc("sync_phase", phase_index)`.
2. **Shape Application:** When a shape (e.g., 2×2) is selected, identify the anchor cell and apply `TILE_STICKY` to all cells in the footprint.

## Benefits
- **Dynamic Pacing:** Mirrors the intended emotional curve (playful $\rightarrow$ desperate).
- **Strategic Depth:** Large impacts seal quadrants, forcing high-stakes movement.
- **Balanced Difficulty:** Prevents early-game frustration while ensuring a challenging finale.

## Acceptance Criteria
- **Probability Check:** Verify 0% 2×2 shots in Phase 1 and ~30% in Phase 3.
- **Shape Accuracy:** Confirm 1×2 and 2×2 shapes impact the correct number of cells.
- **Transition Timing:** Verify weights switch instantly at 1:00 and 2:00.
- **HUD Sync:** Confirm UI displays the correct phase name.

## Migration Checklist
- [ ] Implement `phase_weights` in `CandyCannonController`.
- [ ] Add `current_phase` logic to `GauntletManager._process()`.
- [ ] Implement `_get_shape_footprint(anchor, size)` for cell lists.
- [ ] Update `_fire_volley()` to use phase-based weights.
- [ ] Implement `sync_phase` RPC and HUD label update.
