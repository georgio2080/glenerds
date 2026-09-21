# Moving Company Quote Comparison (moving-cost-calculator) — Change Log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `movecost.sound`, wired into theme toggle and the Estimate button.
- Made the cost-breakdown rows interactive: each row is a keyboard-accessible button — activating it spotlights the row and shows a plain-English explanation of that line's math in a detail line; activating again restores.

## 2026-09-21 — Sample-data toggle + baseline corrections (sweep retro-fix)
- Added the icon-only "Try sample data" flask toggle as the first row of the main content area: circular 44x44px button with flask SVG, accent tint when on, muted hint line next to it, aria-label/title "Try sample data"/"Clear sample data", aria-pressed state, Enter/Space support, hidden in print. ON snapshots current inputs and fills a realistic 3-bedroom full-service 1,200-mile move with packing, storage, and valuation that exercises every breakdown row; OFF restores the snapshot (user data never destroyed, sample data never persisted).
- Shared `.round-btn` class now carries the round shape for both theme and sound buttons (no ID-only shape rules).
- Hardened the sound engine: oscillator scheduling now happens after `AudioContext.resume()` resolves, so the first click always sounds.
- Sound preference key corrected to `moving-cost-calculator.sound`.
- Added the standard bottom cross-promo ("Like this tool? Check out our other apps →" to the Gumroad store), hidden in print.
