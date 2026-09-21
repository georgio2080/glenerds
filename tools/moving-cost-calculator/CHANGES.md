# Moving Company Quote Comparison (moving-cost-calculator) — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `movecost.sound`, wired into theme toggle and the Estimate button.
- Made the cost-breakdown rows interactive: each row is a keyboard-accessible button — activating it spotlights the row and shows a plain-English explanation of that line's math in a detail line; activating again restores.
