---
title: "Gauntlet: Screenshake Follows Player"
id: "079"
status: "done"
priority: 01
sprint: alpha
category: BUG
description: "Screenshake effect does not follow player movement during gameplay."
assignee: "default"
cron_job: "pending"
modified: "2026-06-08"
---

# Gauntlet: Screenshake Follows Player

## Problem
Screenshake effect stays at world origin instead of following the player's camera, breaking immersion when player moves.

## Solution
Attach screenshake to player camera or update offset to match player position.

### Technical Details
1. Locate screenshake implementation (likely in camera or game manager).
2. Ensure shake offset is applied relative to player/camera position.
3. If using `Camera2D`/`Camera3D`, apply shake to the camera node itself.
4. Update shake calculation to account for player movement each frame.

## Acceptance Criteria
- Screenshake follows player position during gameplay.
- Shake feels centered on the player, not the world.
- No visual jitter or position lag during fast movement.

## Migration Checklist
- [ ] Identify screenshake implementation location.
- [ ] Parent shake effect to player camera.
- [ ] Update shake offset to be camera-local, not world-global.
- [ ] Test with player movement at various speeds.
