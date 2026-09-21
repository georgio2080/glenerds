# Competition BBQ Expense & Payout Tracker — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `bbqcost.sound`. Wired into theme toggle, contest add (success; validation error on missing name), export backup, and remove.
- Made the net-result bars interactive: each contest bar is a keyboard-accessible button — activating it spotlights the contest and shows the full cost breakdown (entry, meat, fuel, lodging, supplies, total spent, payout, net) in a detail line; activating again restores.
