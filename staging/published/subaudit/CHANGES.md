# SubAudit — CHANGES.md

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px circular, moon/sun icon, dynamic aria-label/title — no more "Dark mode: on/off" text), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `subaudit.sound`, wired into theme toggle, add/edit subscription (validation errors and success), delete (success/cancel), export (success/empty error), import (success/failure), demo load (success/cancel), and clear all (success/cancel).
- Made the "cost by category" bars interactive: each row is a keyboard-accessible button — activating it spotlights the row and lists the subscriptions in that category with their monthly costs in a detail line; activating again restores.

Build log for the single-file offline app at `index.html` (this directory).
Built 2026-09-19 per `~/workspace/microtool-research/free-loop/app1-subaudit-SPEC.md`.
Everything written from scratch (IP clean-room); no external requests; works from file://.

## What was built
- Subscription CRUD via an accessible `<dialog>` form: name, cost (USD), billing
  cycle (weekly/monthly/quarterly/yearly), category (8 fixed categories), optional
  next-renewal date, optional notes. Validation: name required (<=100 chars), cost
  finite and 0–1,000,000 (no NaN/negatives), renewal must be a real calendar date,
  notes <=500 chars. Inline error messages; dialog stays open on invalid input.
- Dashboard: monthly burn, annual burn, active count, most expensive (name +
  $/mo), average $/mo. Totals region has `aria-live="polite"`.
- Renewal watch: renewals within 14 days listed soonest-first with "In N days" /
  "Renews today" badges; overdue items in their own group with "Overdue N days";
  subscriptions with no renewal date are skipped gracefully.
- Category breakdown: per-category monthly + annual totals with CSS bar chart
  (bar widths computed in JS, set via `style.width`; `role="img"` + `aria-label`
  per bar).
- Trim mode: per-row checkbox ("Consider cancelling <name>" aria-label) updates
  projected monthly + annual savings live, plus a cancel-list summary sorted by
  monthly cost. Trim state persists in localStorage.
- Sort (cost high/low, renewal soonest, name A–Z, category) + text search by name.
- Persistence: localStorage (`subaudit.data.v1`) with in-memory fallback and a
  user-visible notice if browser storage is unavailable.
- JSON export (Blob download, `subaudit-backup-YYYY-MM-DD.json`) and import
  (FileReader; every record sanitized — bad records skipped and counted, dup ids
  dropped, import is confirm-gated replace).
- Demo data (6 fictional subscriptions with relative renewal dates: one 5 days
  out, one overdue, one with no date) + Clear all, both confirm-gated.
- Dark mode: visible toggle button ("Dark mode: on/off", `aria-pressed`),
  `prefers-color-scheme` honored when no stored preference, persisted in
  localStorage (`subaudit.theme.v1`), CSS-variable palette, readable contrast in
  both modes.
- Security: zero `innerHTML`/string-concatenated HTML from user or imported data
  — all rendering via `createElement`/`textContent`/`.value`; import values
  validated (finite numbers, length caps, allow-listed cycle/category).
- Footer: discreet "by Glenerds" link to https://glenerds.gumroad.com.
- Accessibility: `<label>` on every input, native keyboard-operable controls,
  semantic `<table>` with `<caption>` and `scope="col"` headers, `aria-live`
  totals + status regions, focus moved into dialog on open, Escape/backdrop
  closes dialog.
- No emojis in UI chrome. All money via `Intl.NumberFormat` USD.

## Fixes during build / QA
1. **Mobile 390px horizontal page scroll (fixed).** Root cause: the `.sr-only`
   "Actions" span inside the table header is `position: absolute` with no
   positioned ancestor, so its containing block was the initial containing
   block (viewport) — its position extended the document's scrollable overflow
   region even though it is 1px and clipped. (Red herring chased first: the
   table's `min-width: 760px` inside the `overflow-x: auto` wrapper was innocent;
   `overflow-x: clip` on html/body also did not contain it.) Fix: added
   `position: relative` to the `table` rule so the span is contained inside the
   table's scroll container. Verified: document scroll = 0 at 390px, inner table
   scroller still works, span still exposed to assistive tech. Also added
   `html, body { overflow-x: clip; }` as a defensive guard.
2. No other defects found; invalid-input, absurd-value ($1M cap), empty-state,
   and malformed-import paths all behaved as specified on first pass.

## QA evidence (Playwright, system Chromium 152, headless, file://)
30/30 checks passed — script: `/tmp/subaudit-qa.py` (ephemeral; rerun anytime):
- No console errors, no page errors on load; zero external http(s) requests.
- localStorage works on file://; totals region `aria-live="polite"`; all `th`
  have `scope="col"`; empty state renders.
- Add flow (row appears, dashboard updates), negative-cost rejected with dialog
  kept open, edit flow updates burn, delete flow removes row.
- Trim-mode savings hand-check: seeded A=$12/mo (trim) + B=$120/yr (trim) +
  C=$10/mo (not trimmed) → app showed $22.00/mo and $264.00/yr; hand computation
  (12 + 120/12 = 22; 22×12 = 264) matches exactly. Cancel list showed A and B
  only. UI checkbox toggle also verified ($20.00/$240.00 on a $20/mo sub).
- Renewal watch: +5-day sub flagged "In 5 days", −2-day sub flagged
  "Overdue 2 days", +20-day and dateless subs correctly excluded.
- Search filters to 1 row; demo data loads 6 rows; export produced valid JSON
  with 6 subs; clear-all emptied; import round-trip restored 6 subs; malformed
  import rejected with "No valid subscriptions found (2 skipped)" and data
  left untouched.
- Dark-mode toggle → `data-theme="dark"` + localStorage value persisted across
  reload.
- 390px viewport: no horizontal page overflow, renders with demo data, no errors.

## 2026-09-19 — outside-AI QA defect fixes (verified headless Chromium)
- Edit dialog cost pre-fill now rounds to 2 decimals (`toFixed(2)`), so a stored
  float artifact like 12.989999771118164 pre-fills as "12.99".
- "Backup & demo data" status line now refreshes on every data mutation: added
  `refreshDataStatus()` ("N subscription(s) stored locally."), called after
  dialog add/edit save and after delete. Previously it kept showing e.g.
  "Demo data loaded (6 subscriptions)." after adding a 7th.
- "Cancel list renders only one" report investigated: could not reproduce in the
  shipped build — demo flow, manual-add flow, click vs keyboard check, all 6
  boxes, and reload persistence all render every checked subscription with
  correct per-item monthly values. No code change made; left as-is.
- Verified in headless Chromium (Playwright): pre-fill cases 12.989999771118164
  → "12.99", 12.99 → "12.99", 10 → "10.00"; status "Demo data loaded
  (6 subscriptions)." → "7 subscriptions stored locally." after add and after
  edit; cancel list 3/3; zero console/page errors.
