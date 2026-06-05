---
title: "Gauntlet: Telegraph VFX System"
id: "069"
status: todo
priority: 01
sprint: alpha
category: CORE
description: "Implement the 1-second visual and auditory warning system before Candy Cannon impacts."
---

# Gauntlet: Telegraph VFX System

## Problem
Without a telegraph, impacts feel random and unfair. Players need a readable signal to react (move or cleanse), which is the core "dodge or die" loop of the game mode.

## Solution
Implement a multi-stage warning sequence synced across all clients.

### Sequence Design
1. **Telegraph Sync:** Server sends `rpc("sync_telegraph", targets_array)`.
2. **VFX Sequence (1.0s):**
    - **Build-up (0-0.8s):** Place `TILE_TELEGRAPH = 18` (Pink glow) on Layer 2. Tween alpha 0 $\rightarrow$ 1. Play rising pitch sound.
    - **Flash (0.8-1.0s):** Flicker brightness/color to bright white/pink. Play final "pop" sound.
3. **Transition:** Replace `TILE_TELEGRAPH` with `TILE_STICKY` (ID 17) and trigger `screen_shake_manager` ("medium").
4. **Polish:** Add "syrup splash" particles at impact.

## Benefits
- **Fairness:** Shifts failure from "bad luck" to "slow reaction".
- **Anticipation:** Rising audio/visuals create psychological pressure.
- **Readability:** Clear color-coding (Glow $\rightarrow$ Sticky) defines safe zones.

## Acceptance Criteria
- **Timing Check:** Confirm telegraph lasts exactly 1.0s from glow to impact.
- **Visual Distinction:** Verify `TILE_TELEGRAPH` is clearly different from `TILE_STICKY`.
- **Audio Sync:** Confirm "charging" sound aligns with alpha fade-in.
- **Network Consistency:** Verify all clients see telegraphs simultaneously.

## Migration Checklist
- [ ] Define `TILE_TELEGRAPH = 18` in MeshLibrary.
- [ ] Implement `sync_telegraph` RPC in `GauntletManager`.
- [ ] Create local VFX animation logic (Tween + alpha).
- [ ] Integrate `screen_shake_manager` and audio cues.
