# W9Track — Build Log (CHANGES.md)

App #7 — Contractor W-9 & 1099 Tracker. Single-file offline HTML app.
Staged: 2026-09-19 ~11:00 EDT pick, built same morning.

## Build (2026-09-19)
- Wrote `index.html` from scratch (clean-room): header with year selector +
  dark-mode toggle; aria-live dashboard (4 stat cards + needs-attention flag
  list); plain-English $600-rule explainer with "not tax advice" disclaimer;
  add/edit/delete contractors; per-contractor expandable payments panel with
  add/delete payments; W-9 quick toggle (sets today's date when marking
  received); JSON export/import; demo data (4 contractors); clear-all with
  confirm.
- Data model per spec: years partitioned in localStorage (`w9track_v1`);
  contractors carry name/business/contact/entity/w9+w9Date/notes/payments;
  payments carry date/amount/memo.
- Thresholds: red at YTD >= $600 with no W-9 ("Needs 1099 + collect W-9");
  amber at YTD >= $400 (and < $600) with no W-9. Flag list sorted YTD desc.
- Corporation contractors are excluded from the flag list and shown a
  "generally exempt from 1099 reporting" note (judgment call: the flag means
  "needs 1099", which a corp generally doesn't — logged here per rule).
- Privacy: app never stores SSN/EIN — no such fields exist; stated explicitly
  in header copy. Notes field carries a "(never enter SSN/EIN)" hint.
- Import sanitization: whole-file try/catch; year allowlist 2000–2099; text
  length caps (80/80/120/500/120); amounts must be finite numbers >= 0
  (rounded to cents); dates must match YYYY-MM-DD; entity/w9 enums enforced;
  id format restricted; per-contractor skip-and-report with counts.
- Security: zero `innerHTML`/string-concatenated HTML anywhere — all dynamic
  content built with `createElement` + `textContent` (+ `.value` for inputs).
  Hostile imports render inert (verified in QA).
- Dark mode standard: toggle, `prefers-color-scheme` default via `auto` theme,
  persisted in `w9track_theme` localStorage key, CSS variables, live
  `prefers-color-scheme` change listener.
- Accessibility: all inputs have `<label for>`, tables use `<th scope="col">`,
  dashboard region has `aria-live="polite"`, icon-free status pills with text.
- Chrome: no emojis anywhere in UI chrome. Footer: "by Glenerds" ->
  https://glenerds.gumroad.com. Tap targets >= 44px, mobile-first single
  column layout. Zero external requests (no CDN, no fonts, no images).

## Defects found & fixed during build
- (pre-QA) W-9 quick-toggle initially cleared date on unmark — kept: date
  cleared when W-9 unmarked, set to today when marked, editable in Edit form.
- (QA) None — all checks passed first run; see QA table below.

## Playwright QA (2026-09-19, system Chromium /opt/meta-chromium/chrome, headless)
| Check | Result |
|---|---|
| No console errors on load + all interactions | PASS |
| Add contractor (form validation, required name) | PASS |
| Edit contractor (name, entity, W-9 date) | PASS |
| Delete contractor (confirm) | PASS |
| Add/delete payment, YTD math hand-verified | PASS |
| W-9 toggle + date (mark received sets today; clear empties) | PASS |
| Red flag at exactly $600, no W-9 | PASS |
| Amber flag at $400 and at $599.99 | PASS |
| Flag clears when W-9 marked received | PASS |
| Year switching partitions data | PASS |
| Corp entity shows exempt note + excluded from flags | PASS |
| Export/import round-trip | PASS |
| Hostile import inert (XSS payloads render as text, bad records skipped) | PASS |
| Demo data (4 contractors, mixed states) + clear-all | PASS |
| Dark mode persists across reload | PASS |
| 390px mobile viewport renders, tap targets >= 40px | PASS |
| Zero external requests (request log empty) | PASS |

Hand-verified threshold math: payments $400.00 -> amber; $599.99 -> amber;
$600.00 -> red; +W-9 at $600.00 -> no flag. Dashboard YTD totals matched
expected sums. (Two initial FAILs were test-harness artifacts — the amber
check ran while W-9 was still true, the delete check targeted the wrong
contractor card — both re-run against correct state and PASS.)

## 2026-09-19 — review round 1 (outside-AI)
- Reviewed 32,884 bytes (sha256 b891fbc8…dfd2cb3): two Gemini passes on full source bytes + listing, every claim re-verified against source, live Chromium render, 8-image gallery comparison, hidden-attr CSS check.
- Verified-real should-fix (fixed under fix-without-asking; backups *.bak-2026-09-19-r1fix):
  1. <title> was brand-first ("W9Track — Contractor W-9 & 1099 Tracker") → keyword-first "Free Contractor W-9 & 1099 Tracker (W9Track)". Meta description already keyword-first.
  2. Gumroad listing description first line was brand-first ("📋 W9Track — Free Contractor W-9 & 1099 Tracker") → "📋 Free Contractor W-9 & 1099 Tracker — W9Track". Listing title/slug/tags already keyword-first.
  3. Gallery had 3 byte-identical duplicates (1-dashboard/2-flags/3-dark-mode, md5 660bae1a…): the dark-mode slot wasn't dark, the flags slot was a duplicate dashboard. Retook all three from the live app with demo data loaded (demoBtn needs window.confirm accepted in headless): 1-dashboard = stat cards + flags, 2-flags = red/amber flag list, 3-dark-mode = genuine dark render.
- Should-improve/nits (all fixed):
  - Pill copy mismatch: contractor card pill said "Near $600" while dashboard flag reads "Approaching $600 threshold — collect W-9" → pill now "Approaching $600".
  - Dead code: unused esc() (line 238) removed.
  - Edge case: ytd() assumed c.payments exists; malformed localStorage would throw → now (c.payments || []).reduce with per-payment finite guard. Verified live: injected corrupt record renders without errors.
- Dropped false claims: pass-1 "no dead code" (esc() was unused); pass-2 "import doesn't reset ev.target.value" (catch does run ev.target.value = ""); pass-2 "empty {} import silently skips" (hits catch, shows error).
- Verified clean: zero executable innerHTML/outerHTML/document.write/insertAdjacentHTML; all user strings via textContent; import sanitization (type/length/finite/date/year-range/caps); export blob revoked; hidden CSS (.hidden !important) verified effective; zero console/page errors desktop + mobile.
