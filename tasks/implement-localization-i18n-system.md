---
title: "Implement Localization & i18n System"
id: "011"
status: todo
priority: 01
sprint: alpha
category: CLIENT
description: "Implement a comprehensive internationalization (i18n) system to support multi-region deployment across EU, APAC, China, Japan, and Korea."
---

# Implement Localization & i18n System

## Problem
The project is currently "English-only," with all text hardcoded. This prevents expansion into global markets and fails regulatory compliance. Specifically, the project lacks translation infrastructure, locale awareness, CJK typography support, and dynamic regional formatting.

## Solution
Implement Godot's built-in localization system complemented by a custom `LocalizationManager`.

### Implementation Path
1. **Translation Pipeline:** Create a master `translations.csv` for supported locales (EN, DE, FR, ES, ZH_CN, JA, KO, TH, VI) and import them as `.translation` resources.
2. **Localization Manager:** Implement a singleton `LocalizationManager` to handle locale detection (`OS.get_locale()`), manual overrides, and a `tr()` helper for variable substitution.
3. **Typography Engine:** Integrate Noto Sans CJK font and implement a font-switching mechanism that updates the global theme based on the active locale.
4. **Regional Formatting:** Implement locale-aware formatting for numbers and dates.

## Benefits
- **Global Reach:** Enables launching in all major target regions with native-feeling content.
- **Regulatory Compliance:** Meets requirements for localized terms of service and privacy policies.
- **Improved UX:** Players can interact with the game in their native language.

## Acceptance Criteria
- **Translation Coverage:** 100% of UI labels, error messages, and item descriptions are mapped to translation keys.
- **Locale Detection:** Game automatically starts in the correct language based on system settings.
- **Manual Override:** Users can change language in Settings, and the change is reflected instantly.
- **CJK Rendering:** Verify Simplified Chinese, Japanese, and Korean text renders perfectly.
- **Variable Substitution:** Confirm dynamic strings (e.g., "Welcome, [Name]!") are correctly formatted.
- **Cross-Region Verification:** Audit confirms no English strings remain in localized modes.

## Migration Checklist
- [ ] Create `translations.csv` master file with all identified UI keys.
- [ ] Implement `scripts/managers/localization_manager.gd` as an autoload singleton.
- [ ] Integrate Noto Sans CJK font into `assets/fonts/`.
- [ ] Replace all hardcoded strings in `scripts/ui/` and `.tscn` files with `tr()` calls.
- [ ] Add generated `.translation` files to Project Settings.
- [ ] Implement the language selection dropdown in the Settings UI.
- [ ] Perform a smoke test in at least one CJK and one EU locale.
