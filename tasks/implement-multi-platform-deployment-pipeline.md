---
title: "Implement Multi-Platform Deployment Pipeline"
id: "012"
status: todo
priority: 02
sprint: alpha
category: DEVOPS
description: "Establish an automated CI/CD pipeline to build, sign, and deploy the project to Steam, Google Play, App Store, TapTap, and Itch.io."
---

# Implement Multi-Platform Deployment Pipeline

## Problem
The current manual export process is slow and inconsistent. Relying on local machines for production builds introduces "environment drift" and makes deploying to five different storefronts a massive time sink, preventing rapid iteration and staged rollouts.

## Solution
Implement a fully automated deployment pipeline using GitHub Actions and standardized Godot export presets.

### Pipeline Architecture
1. **CI/CD Orchestration:** Create `.github/workflows/deploy.yml` that triggers on version tags (`v*.*.*`).
2. **Platform-Specific Build Jobs:**
    - **Windows:** Headless build $\rightarrow$ Steam Deploy (via `game-ci`) $\rightarrow$ Itch.io (via `butler`).
    - **Android:** Headless build (AAB) $\rightarrow$ Sign with production keystore $\rightarrow$ Google Play $\rightarrow$ TapTap API upload.
    - **iOS:** macOS runner build (IPA) $\rightarrow$ Sign with Provisioning Profiles $\rightarrow$ App Store Connect / TestFlight.
3. **Version Automation:** Implement `tools/generate_version.py` to increment build numbers in `version.json` and `Version` GDScript class.
4. **Staged Rollout Strategy:** Configure the pipeline to support "Tracks" (Internal $\rightarrow$ Beta $\rightarrow$ Production) with gradual percentage rollouts.

## Benefits
- **Consistent Binaries:** Every release is built in a clean, immutable environment.
- **Reduced Time-to-Market:** Deploying to five stores is reduced to a single git tag.
- **Risk Mitigation:** Staged rollouts allow for safer deployments and faster rollbacks.

## Acceptance Criteria
- **Pipeline Automation:** Verify that creating a tag (e.g., `v2.1.4`) automatically triggers the full multi-platform build.
- **Build Integrity:** Verify exported binaries launch correctly and contain the correct version string.
- **Signing Verification:** Confirm Android/iOS binaries are correctly signed and accepted by store validators.
- **Version Synchronization:** Verify `Version.FULL_VERSION` is correctly incremented and embedded.
- **Deployment Confirmation:** Verify a notification is sent upon successful completion of each platform's deployment.
- **Rollout Control:** Confirm Google Play deployment can be targeted to a specific track via workflow inputs.

## Migration Checklist
- [x] Setup `export_presets.cfg` for all 5 target platforms.
- [x] Configure GitHub Secrets for all store credentials.
- [x] Implement `tools/generate_version.py` and integrate it into the workflow.
- [x] Create `.github/workflows/deploy.yml` with separate jobs for Windows, Android, and iOS.
- [x] Test "Internal" track deployment for Android and iOS.
- [x] Verify Steam upload process using `game-ci` action.
- [x] Validate the Itch.io `butler` upload.
