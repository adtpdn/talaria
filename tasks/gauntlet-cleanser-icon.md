---
title: "Gauntlet: Cleanser Icon Fix"
id: "077"
status: "done"
priority: 01
sprint: alpha
category: BUG
description: "Cleanser power-up does not display an icon like other power-ups."
assignee: "default"
cron_job: "pending"
modified: "2026-06-08"
---

# Gauntlet: Cleanser Icon Fix

## Problem
The Cleanser power-up does not display an icon in the HUD/inventory like other power-ups (Smack, etc.), making it invisible to players.

## Solution
Add icon display for Cleanser, consistent with existing power-up icon treatment.

### Technical Details
1. Locate Cleanser HUD/inventory element in the UI code.
2. Add or enable icon asset for Cleanser (similar to Smack icon).
3. Ensure icon displays when Cleanser is available and when active.

## Acceptance Criteria
- Cleanser icon is visible in HUD when available.
- Cleanser icon matches the visual style of other power-up icons.
- Icon disappears when Cleanser is consumed.

## Migration Checklist
- [ ] Add Cleanser icon asset if missing.
- [ ] Update HUD/inventory code to render Cleanser icon.
- [ ] Verify icon shows/hides correctly with Cleanser state.
