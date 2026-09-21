# Used Boat Inspection Checklist — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title — no more text label), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `boatcheck.sound`, wired into theme toggle, inspection item status changes, print, and reset (success/cancel).
- Made the per-category pass/flag/fail bars interactive: each row is a keyboard-accessible button — activating it spotlights the row and lists that category's flagged/failed items with their repair ranges plus the unchecked count in a detail line; activating again restores.
