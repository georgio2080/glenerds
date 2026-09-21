# Competition BBQ Expense & Payout Tracker — Change Log

## 2026-09-21 — Header spec normalization + expanded clickability (Glenerds sweep, retrofit pass)
- Header cluster normalized to the HenTrack reference spec: More Apps pill now `var(--g-accent,#4f46e5)` with white text in both modes; theme toggle is emoji (🌙/☀️ at 1.65rem, icon shows the mode you get) instead of the SVG moon/sun experiment; sound toggle is emoji at 1.65rem on a white round button; flask is spec #14 SVG with larger bubbles rendered at 26px; sample-ON state is the accent-soft tint (no solid fill). Header prints hidden.
- Clickability expanded per the "natural charts" rule: contest table rows are now keyboard-accessible buttons — activating one spotlights the matching chart bar and shows the full cost breakdown (Remove button still works independently); the totals line (Total spent/won/net) is clickable and reveals the per-contest season breakdown. Esc now restores any spotlight; SVG focus uses drop-shadow, never rectangular outlines.
- Sample-data restore is now byte-identical: the raw localStorage string is snapshotted on toggle-on and restored verbatim on toggle-off (or the key is removed if it did not exist).

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `bbqcost.sound`. Wired into theme toggle, contest add (success; validation error on missing name), export backup, and remove.
- Made the net-result bars interactive: each contest bar is a keyboard-accessible button — activating it spotlights the contest and shows the full cost breakdown (entry, meat, fuel, lodging, supplies, total spent, payout, net) in a detail line; activating again restores.

## 2026-09-21 — Sample-data toggle + baseline corrections (sweep retro-fix)
- Added the icon-only "Try sample data" flask toggle as the first row of the main content area: circular 44x44px button with flask SVG, accent tint when on, muted hint line next to it, aria-label/title "Try sample data"/"Clear sample data", aria-pressed state, Enter/Space support, hidden in print. ON snapshots the current contest list and fills three realistic contests (one profitable, two losing) that exercise the diverging net bars, totals, and per-contest breakdowns; OFF restores the snapshot (user data never destroyed, sample data never persisted).
- Shared `.round-btn` class now carries the round shape for both theme and sound buttons (no ID-only shape rules).
- Hardened the sound engine: oscillator scheduling now happens after `AudioContext.resume()` resolves, so the first click always sounds.
- Sound preference key corrected to `bbq-contest-cost-tracker.sound`.
- Added the standard bottom cross-promo ("Like this tool? Check out our other apps →" to the Gumroad store), hidden in print.

## 2026-09-21 — Sample icon locked to Glen's pick #14
- Replaced the placeholder flask SVG in the sample-data toggle with Glen's chosen icon #14 (flask with 3 bubbles), verbatim from ~/workspace/your_files/icon-final-14.svg (stroke=currentColor, 18px render size via existing CSS).
- No behavior change: snapshot/restore, aria labels, accent tint, Sound.click(), print hiding all unchanged.
