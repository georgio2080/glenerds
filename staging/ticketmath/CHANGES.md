# TicketMath — build log

Single-file offline app: `index.html`. All code hand-written (clean-room).

## Design notes
- All DOM built with `document.createElement` / `createElementNS`; all user or
  imported strings rendered via `textContent` / `.value`. No `innerHTML` anywhere
  in the app, and no string-concatenated HTML/SVG.
- SVG bar chart hand-rolled with `createElementNS("http://www.w3.org/2000/svg", …)`;
  bar fills read from the `--accent` CSS variable so it matches the theme.
- Break-even: `tickets = ceil(fixedCosts / weightedAvgPrice)` with a 1e-9 epsilon
  to avoid float noise (e.g. 65.0000000001 → 66). Graceful notes when fixed costs
  are $0 (break even immediately) or weighted price is $0 (cannot compute).
- Sanitization (imports + live inputs): finite numbers ≥ 0, money rounded to
  cents and capped at 1e12, counts floored/int and capped at 1e9, string length
  caps (200/100/60/30), ≤50 costs, ≤4 tiers, each tier allocation ≤ capacity,
  total allocation ≤ capacity or the import is rejected with a message.
- Persistence: `ticketmath-state-v1`; theme: `ticketmath-theme`; theme default
  follows `prefers-color-scheme`.
- Sell-through uses a native range + number pair (both keyboard-operable).
- Tap targets ≥ 44px; inputs use 16px font to avoid mobile zoom.

## Defects fixed during build
1. `renderResults`: removed a dead duplicate `textContent` assignment on the
   profit KPI (first assignment was immediately overwritten).
2. None other — chart, math, and import validation written defensively the
   first time.

## QA (Playwright, headless system Chromium) — 2026-09-19
22/22 checks passed (plus 4 supplemental edge-case checks, all passed).
No console errors on load or at end; zero external HTTP requests;
dark mode toggle persists across reload; demo/clear-all/export-import
round-trip; hostile import rejected or rendered inert (script/onerror
strings shown as literal text via textContent, negatives clamped to 0,
over-limit tiers rejected with message); allocation > capacity shows an
error banner that clears on fix; add-tier capped at 4 with the button
disabled; SVG chart renders one bar per tier (3 on demo, 4 when full);
loss shows negative profit with profit-bad styling; 390px mobile renders
with 44px tap targets; break-even edge cases (fixed costs $0, weighted
price $0) show graceful notes; contribution shares correct
(15.5% / 49.6% / 34.9% on demo data).

Hand-verified break-even (demo data): fixed costs $2,000 + $800 = $2,800;
tier revenue 25×40=$1,000 + 40×80=$3,200 + 75×30=$2,250 → full-house
$6,450 over 150 allocated tickets → weighted avg $6,450/150 = $43.00;
tickets = ceil($2,800 / $43) = ceil(65.116…) = 66 → 66/150 = 44%.
App displays "Sell 66 of 150 allocated tickets (~44%)" — matches.

Defect found by QA run itself (script-side, not app): my first QA script
clicked a correctly-disabled Add-tier button and timed out; fixed the
script to assert disabled instead of clicking.

## 2026-09-19 — outside-AI QA defect fix (verified headless Chromium)
- The "Demo data loaded" status no longer lingers after the user edits or
  deletes. Root cause: the notice described a one-time event but nothing ever
  dismissed it, so it stayed factually wrong after any mutation. Fix: a
  `demoNotice` flag set by `loadDemo()` (after its own save/showStatus);
  any subsequent `save()` — which every edit and delete path calls —
  clears the flag and hides the status. Showing any other status supersedes
  the flag, so error/import/export notices are unaffected.
- Verified in headless Chromium (Playwright): notice shows on demo load;
  cleared after tier-price edit, tier delete, and event-name edit; no phantom
  status after reload; zero console/page errors.

## 2026-09-19 — review round 1 (outside-AI)
- Reviewed 30,487 bytes (sha256 54ad15ae…54af): two Gemini passes on full source bytes + listing, every claim re-verified against source, live Chromium render, 8-image gallery comparison, hidden-attr CSS check.
- Verified-real should-fix (fixed under fix-without-asking; backups *.bak-2026-09-19-r1fix):
  1. <title> was brand-first ("TicketMath — Event Ticket Tier & Revenue Projector") → keyword-first "Free Event Ticket Pricing Calculator (TicketMath)".
  2. Meta description was brand-first ("TicketMath: a free offline calculator…") → keyword-first "Free event ticket pricing calculator: model venue capacity, fixed costs, and up to 4 ticket tiers to find break-even points and projected profit. Offline, single-file tool (TicketMath)."
  3. Gumroad listing description first line was brand-first ("🎟️ TicketMath — Free Event Ticket Pricing Calculator") → "🎟️ Free Event Ticket Pricing Calculator — TicketMath". Listing title already keyword-first.
  4. 5-mobile.png was not taken at a real mobile viewport — retook at 390×844 with is_mobile/has_touch, demo loaded, scrolled to top; zero console/page errors.
- Both AI passes and live render otherwise clean; no false claims to drop; hidden-attr CSS check passed (no defeated hidden elements).

## 2026-09-19 — review round 2: ZERO ISSUES, signed off
- Round 2 ran against the exact updated bytes (30,498; sha256 2d6f7ce5…80b08f): two Gemini passes on full source bytes + listing, independent source verification, headless Chromium live render, all 8 gallery PNGs visually compared.
- All 4 round-1 fixes confirmed in place (keyword-first title/meta/listing, 5-mobile.png real mobile render).
- Demo math hand-verified (fixed costs $2,800.00; full-house $6,450.00; profit $3,650.00; break-even 66/150 ~44% @ $43.00 avg); tier edit recomputes live; dark mode persists; export valid; break-even epsilon logic correct; zero console/page errors.
- Should-fix: none. Should-improve: none. Nits: none.
- Parent verified final bytes independently (hash, title, gallery).
- Signed off 2026-09-19 12:36 EDT. Staging row marked Passed locally. Deploy queued for when Netlify credits reset (full-site ZIP rebuilt same turn).
