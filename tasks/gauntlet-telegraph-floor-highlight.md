---
title: "Gauntlet: Telegraph Floor Highlight Before Drop"
id: "081"
status: "in-progress"
priority: 02
sprint: alpha
category: FEATURE
description: "Add temporary floor highlight before telegraph drops to improve readability."
assignee: "default"
cron_job: "pending"
modified: "2026-06-04"
---

# Gauntlet: Telegraph Floor Highlight Before Drop

## Problem
Telegraph VFX appears suddenly on impact, giving players no visual warning on the floor before the drop.

## Solution
Add a temporary highlighter on the floor before the telegraph drops, indicating where the candy will land.

### Technical Details
1. Add floor highlight phase before existing telegraph sequence.
2. Use a distinct visual (e.g., glow, outline, pulsing tile) on the target floor cell.
3. Sync highlight across all clients via RPC.
4. Highlight appears ~0.5-1.0s before impact, then transitions to telegraph VFX.

## Acceptance Criteria
- Floor highlight appears before telegraph drops.
- Highlight is visible and distinct from normal floor.
- Highlight syncs across all clients.
- Smooth transition from highlight to telegraph VFX.

## Migration Checklist
- [ ] Add highlight phase to telegraph VFX sequence.
- [ ] Create floor highlight material/effect.
- [ ] Add RPC for sync_telegraph_highlight.
- [ ] Sequence: highlight (0.5-1.0s) → telegraph build-up → impact.
