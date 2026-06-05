---
title: "Gauntlet: Polish — VFX, SFX, HUD & Arena Scene"
id: "076"
status: todo
priority: 02
sprint: alpha
category: POLISH
description: "Final visual and auditory polish of the Gauntlet mode, including a dedicated 3D arena scene."
---

# Gauntlet: Polish — VFX, SFX, HUD & Arena Scene

## Problem
The mode currently feels like a prototype. To meet the "Candy Chaos" fantasy, it needs high-impact feedback, a themed environment, and a polished HUD.

## Solution
Develop a dedicated 3D scene and mode-specific polish assets.

### Polish Suite
1. **Dedicated Arena (`gauntlet.tscn`):** Stylized, colorful environment with a 3D Candy Cannon NPC and "candy factory" lighting.
2. **Visual Effects (VFX):**
    - **Impacts:** Candy splash particles and screen-shake.
    - **Smack:** Wind-up effect for attacker, hit spark for target.
    - **Cleanser:** Trailing sparkle effect during traversal.
3. **Sound Effects (SFX):**
    - **Cannon:** Thump (fire) $\rightarrow$ Whiz (travel) $\rightarrow$ Splat (impact).
    - **Smack:** "Pop" or "Slap" sound.
    - **HUD:** "Ding" for missions, "Warning" buzzer for phase changes.
4. **HUD Polish:** Animated mission labels (bounce effect), glowing cleanser icon, and prominent phase banners.

## Benefits
- **Emotional Impact:** Transforms a mechanical loop into a satisfying experience.
- **Communication:** Clear SFX/HUD ensure players understand why they were trapped or what the goal is.
- **Marketability:** A visually distinct arena makes the mode a standout feature.

## Acceptance Criteria
- **Scene Check:** Confirm `gauntlet.tscn` loads correctly with the Candy Cannon centered.
- **AV Sync:** Verify "Splat" sounds and particles trigger exactly at impact.
- **HUD Clarity:** Confirm mission and phase labels are legible and animate correctly.
- **Performance:** Ensure VFX do not cause frame drops in an 8-player match.

## Migration Checklist
- [ ] Create `scenes/arena/gauntlet.tscn` and `scenes/candy_cannon.tscn`.
- [ ] Implement impact particles in `VFXManager`.
- [ ] Integrate all SFX cues into `GauntletManager` events.
- [ ] Polish HUD labels with Tweens.
- [ ] Replace all prototype placeholders with final assets.
