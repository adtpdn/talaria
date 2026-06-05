---
title: "Configure Platform-Specific Export Presets"
id: "031"
status: done
priority: 01
sprint: alpha
category: DEVOPS
description: "Establish and optimize Godot export presets for Windows, Linux, macOS, Android, and iOS to ensure stable production builds."
---

# Configure Platform-Specific Export Presets

## Problem
Exporting to multiple platforms without standardized presets leads to "works on my machine" bugs and inconsistent performance. Platform-specific requirements (Android keystores, iOS provisioning, Windows `.exe` embedding) must be centrally managed to avoid manual errors during release.

## Solution
Configure a complete set of optimized export presets in `export_presets.cfg` and document the required SDK/signing environment.

### Implementation Details
1. **Standardized Presets:** Create dedicated presets for Windows, Linux, macOS, Android, and iOS with optimized compression.
2. **Signing Integration:** Configure production signing certificates and keystores for Android and iOS, stored securely.
3. **Platform Optimization:**
    - **Android:** Optimize target SDK levels, architecture (arm64-v8a), and permissions.
    - **Windows/Linux:** Configure executable embedding and icon assets.
    - **macOS:** Set up app bundling and notarization.
4. **Validation Loop:** Perform smoke test exports for every platform to verify successful launch.

## Benefits
- **Release Consistency:** Every developer and CI agent produces an identical binary.
- **Faster Deployment:** One-click exports for all target platforms.
- **Compliance:** Ensures all platform-specific requirements (e.g., Android API levels) are met for store submission.

## Acceptance Criteria
- **Preset Availability:** All 5 target platforms are present in the Godot Export menu.
- **Signing Verification:** Android and iOS exports use production keystores/profiles (not debug).
- **Optimized Settings:** Confirm "Export with Debug" is disabled and "Embed Pck" is enabled where appropriate.
- **Build Success:** A successful build is generated for each platform that launches to the main menu.
- **Asset Integrity:** Verify platform-specific icons and splash screens are correctly embedded.

## Migration Checklist
- [x] Install Godot export templates for the current engine version.
- [x] Configure Windows, Linux, and macOS presets in `export_presets.cfg`.
- [x] Install Android SDK/NDK and configure the Android export preset.
- [x] Set up iOS export presets and link provisioning profiles.
- [x] Import production signing certificates and keystores.
- [x] Execute a test export for all 5 platforms and verify launch.
