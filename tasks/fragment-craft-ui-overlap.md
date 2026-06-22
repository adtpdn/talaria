---
title: "Fix FragmentCraftPanel UI Overlap"
id: "101"
status: done
priority: 03
sprint: beta
category: UI
description: "Fixed overlapping UI elements in FragmentCraftPanel due to incorrect container layout modes."
modified: "2026-06-22"
---
### Goal / Risk
The Common, Uncommon, and Rare fragment panels were overlapping horizontally when the text values changed, as they were using absolute anchors inside `Panel` nodes instead of expanding properly.

### Solution
- Changed `CommonPanel`, `UncommonPanel`, and `RarePanel` to `PanelContainer` nodes.
- Set their inner `MarginContainer`s to `layout_mode = 2` (Container sorting) instead of `1` (Anchors).
- Cleaned up duplicate node definitions and duplicate `unique_name_in_owner` properties.
