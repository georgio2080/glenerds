# Used Commercial Espresso Machine Inspection Checklist — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right; the whole cluster hides in print.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `espresso.sound`. Wired into theme toggle, print, reset, and checklist status changes (pass=click, flag=select, fail=error).
- Made the per-category stacked bars interactive: each category bar is a keyboard-accessible button — activating it spotlights the category and itemizes the flagged/failed inspection points with their repair ranges in a detail line; activating again restores.
