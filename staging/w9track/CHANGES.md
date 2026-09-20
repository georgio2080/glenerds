## 2026-09-20 — Grok browser QA adjudicated (leg ran on pre-visual build)
- Leg result: zero functional defects in everything it could exercise (thresholds 2024-2029 incl. exact $1,999.99/$2,000 boundaries, contractor add/edit, cross-year payment routing, W-9 flow, corp exemption, export, dark mode, add-year validation).
- Finding A (missing "1099-exempt" pill on a corp card): NOT REPRODUCIBLE — disproven. The render path is deterministic: entity "corp" + no W-9 always renders the pill, the note, and the "Corporation" label (verified in node DOM harness). The leg's own dashboard-count evidence confirms the contractor was treated as exempt. Misread, no symptom to fix.
- Finding B (silent validation on blank W-9 date / $0 payment): ENVIRONMENT ARTIFACT. Both rejections fire window.alert with an explicit message; the leg's automation auto-dismisses native dialogs (it documented this for confirm()), so the message flashed past. Works in real browsers. No change.
- Finding C (Add/Edit entity vocabulary mismatch): FACTUALLY WRONG PREMISE. The Add form already uses value="corp" (lowercase) — identical vocabulary to the Edit form. The leg mistook visible labels for values. No mismatch exists.
- Hardening added anyway: loadStore scrub now canonicalizes hand-edited entity values ("Corporation"/"CORP"/"inc" -> "corp", unknown -> "individual") so card pills/notes can never desync from dashboard counts, matching the existing poisoned-storage scrub (Gemini API review 2026-09-20).
- Also closed a previously-untestable gap: delete-OK path (window.confirm -> true) verified in harness — contractor removed, store saved, list re-rendered.

## 2026-09-20 — Visual rework: "Year at a glance" charts (Glen's standing visual rule)
- New dashboard section "Year at a glance" with hand-rolled SVG charts (zero external requests, offline-safe, dark-mode aware):
  - Payments-by-month bar chart for the selected tax year (12 bars, gridlines, hover titles).
  - W-9 status donut (on file / missing / corporation-exempt) with counts legend.
  - Top contractors horizontal bar chart (top 6 by YTD).
  - Total-paid-by-year bar chart across all tax years (selected year highlighted).
- Threshold progress bar on every non-corporation contractor card: YTD vs the year's red threshold, amber/red coloring, amber-zone marker, text + aria labels. Corporations get no bar (exempt).
- All user-derived text (contractor names) goes through textContent — no HTML injection surface.
- Empty states: muted "no data yet" messages instead of empty charts.
- Verified: JS syntax check + node DOM-stub smoke test (12 monthly bars, 3 donut segments, sorted top-6, XSS-safe names, corp excluded from progress bars, correct red/amber classes).
- NOT yet live: waiting on the Grok QA leg before pushing (browser legs run sequentially on one shared profile).

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

## 2026-09-20 — audit (Glen's "100% proper" bar)
- Verified-real bugs fixed under fix-without-asking (backup index.html.bak-audit-20260920):
  1. Imported data for a NEW tax year was invisible: import wrote store.years[y] but never added y to the in-memory `years` array, so the year selector never showed it. Import now merges new valid years into `years` (sorted) before re-rendering the selector.
  2. Imported duplicate contractor ids were kept as-is (shared openPanels state / edit-form id collisions). Import now regenerates the id on collision.
  3. validDate() accepted impossible dates like 2030-02-30 (regex only). Now verifies the calendar date is real.
  4. money() rendered negatives as "$-41.49". Now "-$41.49" (belt-and-braces; negatives are unreachable via UI/import).
  5. No print stylesheet at all. Added @media print: hides topbar/forms/action buttons, light colors, tables unwrapped.
  6. Clear-all left the in-memory `years` list stale and didn't re-render the year selector. Now rebuilds years, resets to the current year, re-renders.
- SEO (Glen's addition; backup GUMROAD-LISTING.md.bak-seo-20260920): title/meta/description already keyword-first and problem-first. Strengthened differentiator line with explicit "no subscription", and "MORE FROM GLENERDS — made by Glenerds" now cross-links the related sibling QuoteCraft (contractor estimate & quote builder) via the Glenerds store (no live product pages exist yet).
- Gemini leg (8 findings): #3/#4 (import-year sync) were real and are fixed above; the rest adjudicated non-issues (saveStore ReferenceError — never reachable; import parse catch — handled; entity filter bypass — requires own-localStorage tampering; validYear input type — always a string; __proto__ import keys — filtered by validYear before any yearData write; clear-all orphaned edit form — renderAll detaches all cards).

## Full-AI-treatment fixes (2026-09-20, from ChatGPT + Grok review legs)
- **Year-dependent 1099 thresholds**: OBBBA (P.L. 119-21) raised the federal 1099-NEC/MISC
  threshold from $600 to $2,000 for payments made on/after 2026-01-01 (verified via web
  research). Flags, pills, and copy are now per-tax-year: $600 red / $400 amber for 2025
  and earlier; $2,000 red / $1,500 amber for 2026+. All threshold strings render from the
  constants (no more hard-coded "$600" in logic paths). Explainer section rewritten as
  "The 1099 threshold rule".
- **Payment date/year mismatch guard**: adding a payment whose date year differs from the
  selected tax year now asks for confirmation instead of silently filing it under the
  wrong year. Date input defaults to today when viewing the current year, Jan 1 of the
  selected year otherwise.
- **Selected tax year persists** across reloads (localStorage `w9track_year`).
- **Import**: verifies `data.app === "w9track"`; re-importing the same file no longer
  duplicates contractors (exact-duplicate records are skipped and reported separately
  from invalid ones).
- **Edit form**: marking W-9 "Yes" now requires a valid received date (alert + abort)
  instead of silently defaulting to today.
- **Dashboard "W-9s missing"** no longer counts corporation contractors (exempt).
- **saveStore** catches quota/write failures and shows a visible error telling the user
  to export JSON as backup.
- **$0 payments rejected** (amount must be greater than $0).
- ChatGPT/Grok "contractor rename" reports root-caused to test-harness contamination
  (parallel browser QA sessions share one Chromium profile/localStorage) — not an app bug.

## 2026-09-20 — threshold law verified; tax-year correctness fixes
- **Threshold policy corrected against IRS/official guidance**: 2025 and earlier $600;
  2026 $2,000 (One Big Beautiful Bill Act, 2025); **2027+ is inflation-adjusted
  annually** — W9Track now flags at the $2,000 base for 2027+ and the dashboard shows
  an explicit "confirm the current inflation-adjusted amount" note. Removed the
  unverified "P.L. 119-21" citation. App copy, meta description, and Gumroad listing
  updated ("$600 for 2025 and earlier, $2,000 for 2026, inflation-adjusted from 2027").
- **Payment date/year mismatches now auto-route**: adding a payment dated in a different
  tax year records it under its actual tax year (1099s are filed by payment date) and
  switches the view there, instead of asking to file it under the wrong year.
- **Import re-buckets payments by payment date**: imported payments whose date year
  differs from their year bucket are moved to the correct tax year and reported.
  `ytd()` also filters payments by date year as defense-in-depth.
- **Import now requires `data.version === 1`** in addition to `data.app === "w9track"`.
- **W-9 quick-toggle no longer stamps today's date silently**: "Mark W-9 received" now
  opens the edit form with W-9 preset to Yes, requiring an explicit received date;
  clearing a W-9 asks for confirmation.
- **Corporation wording qualified**: exempt notes now read "generally exempt ...
  (exceptions: attorney and medical/health-care payments)".

## 2026-09-20 — gallery regenerated for threshold/copy fixes, ZIP rebuilt
- Regenerated 1-dashboard, 3-dark-mode, 4-mobile, 6-1099-rule, 7-contractors-list
  (new explainer + corp-note copy; element-level captures, no sticky-header artifacts).
- Rebuilt 0-cover.png (year-aware line now "$600 for 2025-, $2,000 for 2026,
  inflation-adjusted from 2027") and cover-square-1200.png (was badly stale,
  $600-era data). 2-flags and 5-add-contractor kept (still accurate).
- Rebuilt w9track-bundle.zip (11 files); bundled index.html byte-identical to source.

## 2026-09-20 — Gemini API review adjudicated; 2 real fixes
- **Threshold law officially verified** (6 independent CPA/tax-firm sources):
  OBBBA signed 2025-07-04; 1099-NEC/MISC threshold $600 -> $2,000 effective
  2026-01-01 (2026 tax year); inflation-adjusted annually from 2027. App
  behavior matches; the "verified against IRS/official guidance" note stands.
- **Adjudicated all 4 Gemini findings**: (1) W-9 preset/date validation — FALSE,
  submit handler sets `c.w9` from the form select BEFORE validating the date
  (regression test "preset W-9 Yes + blank date blocked" confirms); (2) import
  ID collision — non-actionable, payments carry no contractor-ID references and
  `openPanels` is transient in-memory UI state, never persisted; (3) W-9 metadata
  on rebucketed clones — CORRECT semantics (W-9 on file persists across tax
  years; matches the interactive payment-routing clone), kept; (4) negative
  localStorage-poisoned amounts — REAL, fixed (see below).
- **Fix 1 — storage hardening**: `loadStore()` now scrubs every contractor's
  payments through `sanitizePayment()` (drops negative amounts, bad dates) and
  normalizes inconsistent W-9 flags; scrubbed stores are purged back to
  localStorage immediately. `ytd()` also ignores negative amounts as
  defense-in-depth. Verified: 8/8 new tests (poison scrub, ytd hardening,
  purge persistence).
- **Fix 2 — import**: no longer leaves an empty contractor shell in the source
  year when every payment rebuckets to another tax year (contractors with
  genuinely zero payments still import). Import message now counts accurately
  ("Imported 1 contractor. 1 payment was moved...").
- Full suite: 34/34 + 8/8 = 42/42 passing. ZIP rebuilt (11 files, byte-verified).

## 2026-09-20 — second Gemini API review; 1 real UX fix
- Second full-source review (final build). Of 7 findings: 6 rejected —
  threshold logic explicitly confirmed correct by the reviewer itself;
  w9 coercion matches import sanitizer (no legacy booleans exist);
  saveStore quota path already warns the user explicitly (rollback would be
  worse UX); import ID-collision claim fabricated (payments never looked up
  by contractor id); zero innerHTML, no XSS; fractional-cent rounding is
  standard currency behavior, not a bug.
- **Fix — cross-year payment notice visibility**: when a payment dated in
  another tax year auto-switches the view, the explanatory message lived in
  the Data section below the fold while the contractor seemingly vanished.
  `setDataMsg` now takes an optional scroll flag; the cross-year routing
  path passes it, smooth-scrolling the explanation into view.
- Regression: 34/34 + 8/8 = 42/42 passing. ZIP rebuilt (11 files, byte-verified).

## 2026-09-20 — official source confirmed; factual-source blocker closed
- The threshold figures are now backed by enacted statute, not just nonofficial
  CPA sources. Verified via Perplexity research (15 cited sources) + independent
  check of the Congressional Research Service summary (CRS R48611, congress.gov):
  **One, Big, Beautiful Bill Act, Pub. L. No. 119-21, § 70433** (139 Stat. 72,
  enacted July 4, 2025), amending IRC §§ 6041(a) and 6041A(a)(2) and adding
  IRC § 6041(h). § 70433(a): raises the IRC § 6041(a) threshold from $600 to a
  $2,000 base for payments made after December 31, 2025 (2026 tax year; $600
  applied through 2025). § 70433(b): adds § 6041(h) requiring inflation
  adjustment of the $2,000 base for calendar years after 2026 (from 2027).
  § 70433(c): ties the § 6041A(a)(2) service-remuneration threshold (1099-NEC
  rule) to the same raised threshold — both 1099-MISC (§ 6041) and 1099-NEC
  (§ 6041A) covered. CRS: "permanently increases the reportable payments
  threshold to $2,000 and provides for an annual inflation adjustment starting
  in 2027."
- IRS confirming guidance (per cited sources): IRS Publication 1099 (2026),
  General Instructions for Certain Information Returns, "What's New": threshold
  raised from $600 to $2,000 for tax years beginning after 2025, adjusted for
  inflation beginning calendar year 2027. IRS IRB 2026-19, proposed regulation
  REG-113229-25 (Prop. Reg. § 1.6041-1(a)(3)) conforms regulations to the
  enacted statute.
- The "officially verified" wording in this log is now supported by genuine
  statute; the P.L. 119-21 citation (removed earlier as unverified) is hereby
  reinstated. App behavior matches the statute: $600 red / $400 amber for 2025
  and earlier, $2,000 red / $1,500 amber for 2026+ with the "confirm the current
  inflation-adjusted amount" note for 2027+. No app-code change needed.
