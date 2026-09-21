# Net Worth Tracker — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title — no more "◐ Dark" text label), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `networth.sound`, wired into theme toggle, add asset/debt (validation error and success), item remove, and export.
- Made the assets-vs-debts bars interactive: each row is a keyboard-accessible button — activating it spotlights the row and shows the total across items plus an item-by-item breakdown in a detail line; activating again restores.
