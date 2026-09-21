# 52-Week Savings Challenge Tracker — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title — no more "◐ Dark" text label), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `savings52.sound`, wired into theme toggle, week checkbox toggles, and reset (success/cancel).
- Made the cumulative savings chart interactive: every week now has a keyboard-accessible dot marker (mouse, Enter, Space) — activating it spotlights the week and shows that week's save amount, running total, and done status in a detail line; activating again restores.
