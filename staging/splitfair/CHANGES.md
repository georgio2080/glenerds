# SplitFair — build log

## 2026-09-19 — Initial build (app #5, free loop)

Built per `~/workspace/microtool-research/free-loop/app5-splitfair-SPEC.md` (v1, picked 2026-09-19).

### What was built
- Single-file `index.html` (~33 KB), zero external requests, works from `file://`.
- People: name + optional room sqft; add/remove; sqft edits update results live.
- Bills: preset types (Electric, Gas, Internet, Water, Trash) + custom name, amount,
  period start/end, split method (Equal / By square footage / By occupancy); inline
  edit + delete per bill.
- Occupancy editor per bill: days present (defaults to period length) + guest days
  (each guest day = 0.5 occupant-day, rule shown in UI).
- Results (`aria-live="polite"`): per-bill share table with math note, totals table,
  settle-up list.
- Math core works in integer cents; each share rounded to cents; rounding drift
  (bill total − sum of rounded shares) assigned to the largest share (first wins
  ties); per-bill note shows the exact adjustment. Sqft fallback: total sqft = 0 →
  equal split with note. Occupancy fallback: total weight = 0 → equal split with note.
- localStorage persistence (`splitfair.state.v1`); JSON export/import with full
  sanitization (finite-number ranges, 60-char name caps, enum allowlist for method,
  date format check, per-array count caps).
- Demo data (3 roommates, Electric by sqft + Internet by occupancy) + Clear all
  (confirm dialog).
- Dark mode standard: early-script theme set (no flash), toggle button with
  `aria-pressed`, `prefers-color-scheme` default, `localStorage` persistence
  (`splitfair.theme.v1`), CSS-variable palette.
- Discreet footer: "by Glenerds" → https://glenerds.gumroad.com. No emojis in UI.
- Accessibility: every input labeled (visible labels + aria-labels on dynamic rows),
  `scope="col"`/`scope="row"` on table headers, results region `aria-live="polite"`,
  44px minimum tap targets, mobile-first layout.
- Security: zero `innerHTML` / string-concatenated HTML anywhere; all dynamic content
  built with `document.createElement` + `textContent` / `.value`. Import sanitized
  before touching state.

### Defects fixed during build
- None in the app itself. Code review + the full QA suite below passed with no
  app changes required. Two issues found were in the QA harness only (a duplicated
  hostile-import fixture dict and two competing dialog handlers), not in the app;
  both were corrected in the test script and the suite re-run green (38/38).

### QA (Playwright, real Chromium, headless) — see QA report for per-check results
Hand-verified math case: 3-person equal split of $100.00 → raw $33.333… each,
rounded $33.33 × 3 = $99.99, $0.01 drift to the largest share (first, Alice):
$33.34 + $33.33 + $33.33 = $100.00 exactly. Occupancy case: $90 over 30 days,
weights 30 / 22 (20 + 0.5×4) / 11 (10 + 0.5×2), total 63 → A: 90×30/63 =
$42.857→$42.86; B: 90×22/63 = $31.429→$31.43; C: 90×11/63 = $15.714→$15.71;
sum $90.00 exactly, no drift. Sqft case verified against demo data in the report.

## 2026-09-19 — outside-AI QA defect fixes (verified headless Chromium)
- Empty "days present" no longer becomes 0 after a reload. Root cause: the
  occupancy sanitizer ran `cleanNum(row.days, ...)`, and `Number(null) === 0`
  coerced the null "use period-length default" sentinel into an explicit 0,
  so after reloading a touched-but-empty days field the person got a 0-day
  weight. The sanitizer now preserves null/undefined/"" as null for days.
- "Method/rounding footnotes render twice" investigated: could not reproduce
  as a code bug — `renderResults` clears its container on every render and
  appends exactly one `.math-note` per bill (verified with 1–2 bills, method
  changes, and rapid re-renders). Identical footnote text under multiple bills
  sharing one method is one footnote per bill section, by design. No change.
- Verified in headless Chromium (Playwright): touched-but-empty days stays
  empty with the period-length placeholder after reload and computes with the
  30-day default ($67.50/$22.50 on a 30:10 weight split); explicit days
  preserved; exactly one footnote per bill; zero console/page errors.

## 2026-09-19 — review round 1 (outside-AI)
- Reviewed 33,602 bytes (sha256 d8f4483f…47ce017): two Gemini passes on full source bytes, every claim re-verified against source + live Chromium, gallery compared, demo math hand-checked to the cent.
- Verified-real should-fix (fixed under fix-without-asking; backups *.bak-2026-09-19-r1fix):
  1. <title> was brand-first ("SplitFair — Roommate Utility Split Calculator") → keyword-first "Free Roommate Utility Split Calculator (SplitFair)".
  2. Meta description was brand-first → keyword-first "Free roommate utility split calculator: split electric, gas, and internet bills equally, by room size, or by occupancy. Offline, single-file tool (SplitFair)."
  3. Gumroad listing description first line was brand-first ("⚖️ SplitFair — Free Roommate Utility Split Calculator") → "⚖️ Free Roommate Utility Split Calculator — SplitFair". Listing title/slug/tags already keyword-first.
  4. Gallery stale: 1-people.png and 2-bills.png were byte-identical duplicates; images 1/2/3/4/6 showed old 2-person demo (Jordan/Sam, 200 sq ft) while demoData() has 3 people (Alex 140, Jordan 110, Sam 90, 340 sq ft). Regenerated all 8 PNGs from the live app in headless Chromium.
  5. (found during gallery regeneration) REAL BUG round 1 missed: "Custom name" field was always visible despite the `hidden` attribute — CSS `.field{display:flex}` defeated the `hidden` UA style (offsetParent!==null with Electric selected). Fixed with `[hidden]{display:none!important}` at the top of the stylesheet. Verified: hidden with Electric, shown when Custom… is chosen, hidden again on switch back; zero console/page errors; full demo flow (load demo, add flows, results, dark mode, export) re-verified clean.
- Dropped false claims: DST ±1-day periodDays bug (false — noon-to-noon + Math.round absorbs DST offset, verified spring-forward case); MAX_AMOUNT float precision (non-issue — cents rounding, < MAX_SAFE_INTEGER); occupancy sanitization "bug" (unreachable via UI; import path uses deliberate sentinel defaults).
- Should-improve/nits: "Settle up" lists per-person balances rather than who-pays-whom (no payer data tracked — design); renderOccupancyTable writes defaults without save() (behaviorally identical via computeBill fallback).
- Verified clean: no innerHTML/outerHTML/document.write; createElement+textContent rendering; cleanStr control-char stripping; sanitizeState on load/import; Blob export; zero external requests; zero console/page errors.

## 2026-09-19 — review round 2: ZERO ISSUES, signed off
- Round 2 ran against the exact updated bytes (33,675; sha256 f96b65ca…21399): two Gemini passes on full source bytes + listing, independent source verification, headless Chromium live render, all 8 gallery PNGs visually compared.
- All 5 round-1 fixes confirmed in place: keyword-first title/meta/listing, gallery regenerated (no duplicates), [hidden]{display:none!important} verified live (custom name hidden with Electric, shown with Custom…, zero console/page errors).
- Demo math hand-verified (Electric $120 → Alex $49.42 / Jordan $38.82 / Sam $31.76; Internet $75 by occupancy); dark mode persists; export works; mobile renders.
- Should-fix: none. Should-improve: none. Nits: none.
- Parent verified final bytes independently (hash, title, listing line, gallery uniqueness).
- Signed off 2026-09-19 12:34 EDT. Staging row marked Passed locally. Deploy queued for when Netlify credits reset (full-site ZIP rebuilt same turn).
