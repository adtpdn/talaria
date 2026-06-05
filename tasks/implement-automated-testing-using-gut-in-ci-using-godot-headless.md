---
title: "Automated Testing via GUT & Godot Headless"
id: "028"
status: done
priority: 01
sprint: alpha
category: DEVOPS
description: "Technical implementation of the headless GUT test runner within the GitHub Actions CI pipeline."
---

# Automated Testing via GUT & Godot Headless

## Problem
Running tests in CI is challenging because Godot typically requires a display server. Without a headless configuration, CI agents (CLI-only Linux VMs) crash when attempting to run tests that instantiate a `Node` or `Scene`.

## Solution
Utilize Godot 4's native `--headless` mode combined with the GUT CLI to execute tests without a graphical interface.

### Technical Implementation
1. **Headless Configuration:** Use the `--headless` flag in the Godot command to bypass the display server.
2. **GUT CLI Integration:** Call the GUT command-line interface (`gut_cmdln.gd`) to run tests and export results as JUnit XML.
3. **CI Environment Setup:** Configure the GitHub Actions runner to use a Godot-ready Docker image (e.g., `chickensoft-games/setup-godot`).
4. **Result Parsing:** Use a post-processing step in the pipeline to parse XML and generate a human-readable summary in the PR.

## Benefits
- **Infrastructure Independence:** Tests run on any server, regardless of GPU/monitor availability.
- **Speed:** Headless mode is significantly faster by skipping rendering overhead.
- **Reliability:** Eliminates flaky tests caused by varying GPU drivers or resolution settings.

## Acceptance Criteria
- **Headless Success:** Verify that `godot --headless -s addons/gut/gut_cmdln.gd` executes and returns non-zero only on failure.
- **CI Pipeline Integration:** Confirm `.github/workflows/tests.yml` initializes the Godot environment and triggers the headless runner.
- **Result Visibility:** Verify test results are correctly surfaced in GitHub Actions logs and PR comments.
- **Zero-Crash Baseline:** Confirm the test suite runs to completion without "Display Server" or "Vulkan" errors.

## Migration Checklist
- [x] Verify all tests in `tests/` are compatible with headless mode (no `get_viewport().size` calls).
- [x] Configure GitHub Actions workflow with correct Godot version and headless flags.
- [x] Set up GUT CLI command to point to the `res://tests/` directory.
- [x] Implement the JUnit XML export in the GUT command.
- [x] Test the pipeline by pushing a commit that triggers the workflow.
