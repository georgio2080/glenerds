# GradePlan changelog

## 2026-09-20 — v1.2 (bench-review fixes)
- Fixed: Honors/AP-weighted F no longer gains +1.0 quality point — an F stays 0.0 even when weighted + H/AP checked (was: 3-credit Honors F counted 1.0)
- Added: incomplete course/GPA rows are now announced ("N incomplete categor(ies)/course(s) not counted") instead of silently ignored
- Fixed: loading saved state no longer re-saves during restore (showTab skipSave)
- Hardened: saved-value validation now strictly numeric (rejects "85garbage"-style strings on restore)
- QA: 11/11 Playwright regression checks pass in system Chromium (weighted-F math, incomplete-row notes, strict restore validation, no-mutation reload, core math, dark persistence), zero page errors

## 2026-09-20 — v1.1 (QA fixes)
- Fixed: 0-credit courses no longer trigger a contradictory "Credits must be between 0 and 12." error — they are excluded from the GPA like blank rows (audit courses don't affect GPA)
- Added: pure-CSS bar visuals on all three result panels (final-exam target marker on a 0–100 scale, per-category score bars, per-course grade-point bars + overall GPA bar); zero external requests, dark-mode aware, XSS-escaped labels
- QA: 16/16 jsdom DOM checks pass (0-credit math, bar rendering, XSS escaping, dark mode + persistence), zero JS errors

## 2026-09-19 — v1.0 (initial build)
- Final exam solver: required-score math with impossible/guaranteed verdicts
- Weighted course grade calculator with auto-scaling weights
- GPA calculator: 4.0 scale, weighted/unweighted toggle (+1.0 Honors/AP)
- Show-your-work formula blocks on every result
- Dark mode (toggle, prefers-color-scheme, persisted)
- localStorage persistence with strict validation (corrupt storage falls back to defaults)
- Print stylesheet, mobile-friendly layout, zero external requests
- QA: 20/20 Playwright checks pass in system Chromium, 0 console/page errors (light, dark, mobile)
