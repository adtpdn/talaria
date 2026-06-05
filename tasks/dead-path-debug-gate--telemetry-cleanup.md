---
title: "Dead Path, Debug Gate & Telemetry Cleanup"
id: "017"
status: todo
priority: 02
sprint: alpha
category: CORE
description: "Clean up debug hooks and implement a telemetry-driven removal matrix for dead code and logs."
---

# Dead Path, Debug Gate & Telemetry Cleanup

## Problem
The codebase is littered with debug-only hooks (e.g., `KEY_F9`), excessive `print()` statements, and "dead paths" (unused code). These create "noise" in release builds, potentially leak internal state, and make logic harder to follow. There is no telemetry to prove whether "placeholder" scripts are actually used.

## Solution
Implement a structured "Cleanup and Instrument" workflow.

### Technical Approach
1. **Removal Matrix:** Categorize all suspected dead paths and debug hooks into `Keep`, `Safe-Remove`, `Needs-Runtime-Proof`, and `Feature-Flag`.
2. **Debug Gating:** Wrap all essential debug tools in `OS.has_feature("debug")` blocks to ensure they are stripped from release exports.
3. **Telemetry Instrumentation:** Instrument critical lifecycle events (`room_joined`, `preflight_pass`, `loading_screen_start/finish`, `match_sync_complete`, `reconnect_success/fail`) to track reachability.
4. **SLO Dashboard:** Use gathered telemetry to create a Service Level Objective (SLO) dashboard for the lobby-to-match transition.

## Benefits
- **Cleaner Binaries:** Reduces binary size and removes accidental leaks of debug information.
- **Improved Performance:** Removing excessive prints and unused logic reduces CPU overhead.
- **Data-Driven Cleanup:** Prevents accidental deletion of critical edge-case code by requiring telemetry proof.

## Acceptance Criteria
- **Debug Hook Removal:** A global search for `Input.is_key_pressed()` for debug keys (e.g., `F9`) returns zero results in production paths.
- **Print Audit:** No `print()` statements remain in core managers unless wrapped in a debug feature flag.
- **Telemetry Coverage:** All specified lifecycle events are correctly fired and logged.
- **Evidence-Based Deletion:** Every deleted script is cross-referenced against the telemetry matrix as "not reached".
- **Release Integrity:** Production export is verified to be free of debug consoles and shortcuts.

## Migration Checklist
- [ ] Scan `main.gd`, `player.gd`, and `login_screen.gd` for debug keys and prints.
- [ ] Build the "Remove/Keep/Flag" matrix for all suspected dead paths.
- [ ] Implement the `OS.has_feature("debug")` wrapper for all essential debug tools.
- [ ] Add telemetry event triggers to the lobby-to-match lifecycle.
- [ ] Analyze telemetry data to confirm "safe-remove" candidates.
- [ ] Delete verified dead scripts and functions.
