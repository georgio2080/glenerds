# HOA Special Assessment Calculator — Change Log

## 2026-09-21 — Header spec normalization + expanded clickability (Glenerds sweep, retrofit pass)
- Header cluster normalized to the HenTrack reference spec: More Apps pill now `var(--g-accent,#4f46e5)` with white text in both modes; theme toggle is emoji (🌙/☀️ at 1.65rem, icon shows the mode you get) instead of the SVG moon/sun experiment; sound toggle is emoji at 1.65rem on a white round button; flask is spec #14 SVG with larger bubbles rendered at 26px; sample-ON state is the accent-soft tint (no solid fill). Header prints hidden.
- Clickability expanded per the "natural charts" rule: the "Your estimated share" headline is now a keyboard-accessible button that reveals the full calculation chain (gross share − reserve share = out of pocket, months of dues). Result table rows were already clickable; Esc now restores any row spotlight. SVG focus uses drop-shadow, never rectangular outlines.
- Sample-data restore is now byte-identical: the raw localStorage string is snapshotted on toggle-on and restored verbatim on toggle-off (with a skip-save guard so the restore calc pass cannot rewrite the key; key removed if it did not exist).

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, dynamic aria-label/title — no more text label), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `hoacalc.sound`, wired into theme toggle and the Calculate button.
- Made the result table rows interactive: each row is a keyboard-accessible button — activating it spotlights the row and shows a plain-English explanation of that line's math in a detail line; activating again restores.

## 2026-09-21 — Sample-data toggle + baseline corrections (sweep retro-fix)
- Added the icon-only "Try sample data" flask toggle as the first row of the main content area: circular 44x44px button with flask SVG, accent tint when on, muted hint line next to it, aria-label/title "Try sample data"/"Clear sample data", aria-pressed state, Enter/Space support, hidden in print. ON snapshots current inputs and fills a realistic $240,000 roof / 40-unit / $60,000 reserve scenario that exercises every result row including the thin-reserves warning; OFF restores the snapshot (user data never destroyed, sample data never persisted).
- Shared `.round-btn` class now carries the round shape for both theme and sound buttons (no ID-only shape rules).
- Hardened the sound engine: oscillator scheduling now happens after `AudioContext.resume()` resolves, so the first click always sounds.
- Sound preference key corrected to `hoa-special-assessment-calculator.sound`.
- Added the standard bottom cross-promo ("Like this tool? Check out our other apps →" to the Gumroad store), hidden in print.

## 2026-09-21 — Sample icon locked to Glen's pick #14
- Replaced the placeholder flask SVG in the sample-data toggle with Glen's chosen icon #14 (flask with 3 bubbles), verbatim from ~/workspace/your_files/icon-final-14.svg (stroke=currentColor, 18px render size via existing CSS).
- No behavior change: snapshot/restore, aria labels, accent tint, Sound.click(), print hiding all unchanged.

## 2026-09-21 — Sample toggle moved into header cluster (Glen's placement call)
- Moved the #14 flask sample-data toggle from the first row of main content into the top-bar `.g-header-actions` cluster, immediately right of the More Apps pill (header order: More Apps, flask, dark-mode, sound).
- Button now shares the `round-btn` class with the theme/sound buttons (44x44px circular, same border/bg/shadow); kept the `.sample-toggle` class for the accent active tint and print hiding.
- Added `flex:none` to the toggle SVG so the #14 icon renders at the intended 18x18px (a flex-shrink quirk was squeezing it to 12px wide in some contexts).
- Removed the now-unneeded `.sample-row` wrapper and muted hint line; behavior (snapshot/restore, aria labels, Sound.click()) unchanged.
