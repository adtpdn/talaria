---
title: "Gauntlet: Polish — VFX, SFX, HUD & Arena Scene"
id: "076"
status: "in_progress"
priority: 02
sprint: alpha
category: POLISH
description: "Final visual and auditory polish of the Gauntlet mode, including a dedicated 3D arena scene and growth tick VFX."
modified: "2026-06-10"
---

# Gauntlet: Polish — VFX, SFX, HUD & Arena Scene

## Problem
The mode currently feels like a prototype. To meet the "Candy Chaos" fantasy, it needs high-impact feedback, a themed environment, and a polished HUD.

## Solution
Develop a dedicated 3D scene and mode-specific polish assets.

### Polish Suite
1. **Dedicated Arena (`gauntlet.tscn`):** Stylized, colorful environment with a 3D Candy Pump NPC and "candy factory" lighting.
2. **Visual Effects (VFX):**
    - **Growth Tick Impact:** Candy splash particles and light screen-shake on each growth tick.
    - **Telegraph:** Amber/syrup glow on telegraphed cells, pulsing animation.
    - **Bubble Spawn:** Growing bubble animation (1×1 → larger, brighter, shaking).
    - **Bubble Explosion:** Syrup splash particles, 3×3 sticky area, screen-shake ("medium").
    - **Smack:** Wind-up effect for attacker, hit spark for target.
    - **Cleanser:** Trailing sparkle effect during traversal.
3. **Sound Effects (SFX):**
    - **Growth Tick:** Soft "squish" (cell becomes sticky).
    - **Telegraph:** Rising pitch (build-up) → "pop" (transition).
    - **Bubble:** Growing hum → "burst" (explosion).
    - **Smack:** "Pop" or "Slap" sound.
    - **HUD:** "Ding" for missions, "Warning" buzzer for phase changes.
4. **HUD Polish:** Animated mission labels (bounce effect), glowing cleanser icon, and prominent phase banners.
5. **Phase Labels:** "Outer Pressure" → "Middle Pressure" → "Inner Survival" (replaces old phase names).

## Benefits
- **Emotional Impact:** Transforms a mechanical loop into a satisfying experience.
- **Communication:** Clear SFX/HUD ensure players understand why they were trapped or what the goal is.
- **Marketability:** A visually distinct arena makes the mode a standout feature.

## Acceptance Criteria
- **Scene Check:** Confirm `gauntlet.tscn` loads correctly with the Candy Pump centered.
- **Growth VFX:** Verify candy splash particles trigger on each growth tick.
- **Telegraph VFX:** Verify amber glow appears 1s before cells become sticky.
- **Bubble VFX:** Verify grow animation and explosion particles.
- **HUD Clarity:** Confirm mission and phase labels are legible and animate correctly.
- **Performance:** Ensure VFX do not cause frame drops in an 8-player match.

## Migration Checklist
- [ ] Create `scenes/arena/gauntlet.tscn` with Candy Pump NPC (not Cannon)
- [ ] Implement growth tick impact particles in `VFXManager`
- [ ] Implement bubble grow/shake/explosion VFX
- [ ] Integrate all SFX cues into `GauntletManager` events
- [ ] Polish HUD labels with Tweens
- [ ] Update phase banner text: "Outer Pressure" → "Middle Pressure" → "Inner Survival"
- [ ] Replace all prototype placeholders with final assets
