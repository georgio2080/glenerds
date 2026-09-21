# Free Habit Tracker — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title — no more "◐ Dark" text label), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `habitfree.sound`, wired into theme toggle, add habit (validation error and success), date-dot toggles, habit delete, and export.
- Made habit names interactive: clicking (or Enter/Space on) a habit name spotlights the habit card and shows its 14-day summary (done count, completion %, current streak, total check-ins) in a detail line; activating again restores.
