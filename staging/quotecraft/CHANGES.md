# QuoteCraft — CHANGES.md

Build log for the single-file offline app at `index.html` (this directory).
Built 2026-09-19 per `~/workspace/microtool-research/free-loop/app9-quotecraft-SPEC.md`.
Everything written from scratch (IP clean-room); no external requests; works from file://.

## 2026-09-20 — functional-bench fixes (parent adjudicated ChatGPT/Grok/Gemini findings)
- **Exact-decimal money math.** New `lineCents(qty, unitCents)` helper computes line
  totals in integer space from the decimal representation of qty, eliminating the
  IEEE 754 half-cent-down error Grok proved (e.g. 4.1 × $3.25 was $13.32, now the
  correct $13.33). Used in `calcTotals`, the items table, the print view, and the
  flat-discount cap check. Verified in node against Grok's swept failing cases.
- **Exact-decimal `toCents`.** Currency strings are now parsed decimally instead of
  via binary float, so `$10.005` correctly becomes 1001¢ (was 1000¢).
- **UI entry now matches import caps.** Add-item form rejects qty > 1,000,000 and
  unit price > $1,000,000, mirroring `cleanQty`/`cleanUnitCents` (ChatGPT #4/#5).
- **Percent discounts clamped to 2 decimals** on live entry and import
  (ChatGPT #1).
- **Totals panel now shows the actual taxed base.** Added a "Taxable subtotal (after
  discount)" row next to the existing before-discount row, so the tax figure is
  fully explained (ChatGPT #7). `calcTotals` returns `taxableAfterDiscount`.
- **Import accounting is honest.** `cleanQuote` now counts dropped line items
  (over the 500 cap + failed validations) into `stats.dropped`, which
  `sanitizeState` folds into the reported `skipped` total (Grok #2). Duplicate
  imported item ids are regenerated so edit/delete can't hit the wrong rows
  (Grok #6 / ChatGPT #10).
- **Delete-while-editing no longer strands the form.** The item delete handler
  clears the stale `editId` and resets the button to "Add item" (Grok #3).
- **Clear-all resets the full default state**, including `editedByUser:false`
  (ChatGPT #3).
- **Export is sanitized.** `exportJSON` runs state through `sanitizeState` before
  serializing, so hand-edited localStorage can't leak malformed data
  (ChatGPT #9).
- **Print view item table gains a Tax column** (Yes/— per line), so customers can
  see why tax was charged (ChatGPT #11).
- **Import status via inline live region** (`#data-status`, role=status) instead of
  `alert()` dialogs (ChatGPT #16).
- **Debounced persistence.** Keystroke handlers (`bindEditor`, business-profile
  inputs) now use `saveSoon()` (400 ms debounce); discrete actions still save
  immediately (ChatGPT #15).
- Findings reviewed and explicitly NOT changed: invalid-date entry visibly reverts
  the field to the last valid date (acceptable); `storageOK` latch is intentional
  (avoids throwing on every keystroke once storage fails); sparse quote numbers
  after import are not a defect; `renderAll` editor reopen is harmless.

## What was built
- **Business profile:** name, phone, email, tagline (text branding only) — prints on
  every customer quote. Persists on every keystroke.
- **Quotes list:** table (number, date, customer, status badge, total), newest first,
  tap-to-open. Quote numbers auto-increment `Q-0001…` via a monotonic counter that
  never reuses a number, even after deletion; imports fast-forward the counter past
  the highest imported number.
- **Quote editor:** customer name + optional address/phone, quote date, valid-until
  date, status (Draft/Sent/Accepted/Declined). Line items: description, quantity
  (fractional allowed, e.g. 2.5 hrs), unit price, taxable checkbox → line total;
  add/edit/delete with validation (description required, qty/price ≥ 0, finite).
- **Discount & tax:** none / percent / flat-$ discount; tax rate % (0–100).
  Totals panel (Subtotal, Discount, Taxable subtotal, Tax, Grand total) with
  `aria-live="polite"`.
- **Money math — integer cents, exact to the cent.** Unit prices are stored as whole
  cents; line total = round(qty × unitCents). Percent discount = round(subtotal ×
  pct/100); flat discount clamped to ≤ subtotal. Tax-after-discount rule, documented
  in a UI footnote: the discount is pro-rated across taxable vs non-taxable lines in
  proportion to each side's share of the subtotal; tax = round((taxable subtotal −
  its share of discount) × tax rate / 100). The rule and the whole-cents guarantee
  are stated in the totals-panel footnote.
- **Print view:** customer document (business header, bill-to block, quote meta,
  item table, totals, terms, signature lines) behind a print stylesheet. The
  discreet "by Glenerds" footer (→ https://glenerds.gumroad.com) exists only in the
  screen chrome — the printed quote carries no Glenerds branding.
- **Persistence:** localStorage (`quotecraft.data.v1`) with a visible notice if
  storage is unavailable (in-memory fallback for the session).
- **JSON export/import:** export downloads `quotecraft-backup-YYYY-MM-DD.json`;
  import is confirm-gated replace with full sanitization — finite numbers ≥ 0,
  length caps, status-enum allowlist, date-format checks, quote-number uniqueness
  (dup numbers skipped and counted), bad records skipped and counted.
- **Demo data:** fictional business + 2 quotes (one with 10% discount and mixed
  taxable/non-taxable items, one plain) + Clear all, both confirm-gated.
- **Dark mode standard:** visible toggle ("Dark mode: on/off", `aria-pressed`),
  `prefers-color-scheme` honored with no stored preference, persisted
  (`quotecraft.theme.v1`), CSS-variable palette, contrast-checked in both modes.
- **Security:** zero `innerHTML`/string-concatenated HTML from user or imported
  data — all rendering via `createElement`/`textContent`/`.value`.
- **Accessibility:** `<label>` on every input, tables with `<caption>` and
  `scope="col"`, `aria-live="polite"` totals, status badges as text, native
  keyboard-operable controls, no emojis in chrome.
- **Mobile-first:** 390px-tested, no horizontal page overflow, all visible tap
  targets ≥ 40px, tables scroll horizontally inside cards.

## Fixes during build / QA
1. **Reload re-sanitization multiplied unit prices ×100 (fixed).** `cleanItem()`
   applied `toCents()` (dollars→cents) to `unitCents` values already in cents, so
   every localStorage load multiplied all prices by 100 (caught by QA: totals
   jumped from $130.00 to $13,000.00 after a reload). Fix: `cleanUnitCents()` now
   takes an `alreadyCents` flag — stored/exported `unitCents` are validated as
   integer cents (no conversion); only a legacy `unitPrice` (dollars) field is
   converted.
2. **`showView()` null error on tab switch to editor (fixed).** The old code built
   a tab id `tab-edit` that doesn't exist and called `setAttribute` on null (page
   error on load). Fix: explicit view→tab mapping (`edit` selects the Quotes tab).
3. **Discount/tax fields only recomputed totals on blur (fixed).** Now bound to
   `input` as well, so totals update live while typing.
4. **QA script artifacts (test-only, not app bugs):** removed a leftover placeholder
   `evaluate`, pointed the print-view text check at `textContent` (the print view is
   `display:none` on screen so `inner_text()` is empty), opened the correct quote row
   for print verification (Q-0001, not the newest empty draft), scoped the tap-target
   check to visible buttons, and checked the hostile payload in the items table where
   it actually renders.

## QA evidence (Playwright, system Chromium, headless, file://)
**41/41 checks passed** — script: `/tmp/quotecraft-qa.py` (ephemeral; rerun anytime):
- Load: no console errors, no page errors, zero external http(s) requests,
  localStorage works on file://, totals `aria-live="polite"`, all 12 `th` have
  `scope="col"`, every input labeled.
- **Hand-verified totals (mixed taxable, % discount, tax):** items 2×$50.00 taxable
  + 1×$30.00 non-taxable, 10% discount, 8% tax → Subtotal $130.00, Discount −$13.00
  (round(13000×10/100)=1300¢), Taxable subtotal $100.00, Tax $7.20
  (taxable discount = round(1300×10000/13000)=1000¢; taxable after = 9000¢;
  round(9000×8/100)=720¢), Grand total $124.20. App matched exactly.
- **Flat discount hand-verified:** $20 flat on the same items → taxable discount
  round(2000×10000/13000)=1538¢; taxable after 8462¢; tax round(8462×8/100)=677¢ =
  $6.77; total $116.77. App matched exactly.
- Tax-after-discount rule + whole-cents guarantee documented in the UI footnote.
- Zero-qty/zero-price line renders $0.00 and leaves totals unchanged.
- Item edit (prefill + save) and delete via UI.
- Quote numbering: Q-0001 → Q-0002 created, deleted, next created was Q-0003
  (never reuses).
- Status change (Sent→Accepted) and discount type persist across reload.
- Print: button triggers print; print view renders the customer document (header,
  bill-to, items, totals, terms, signature lines) with **no Glenerds footer**;
  print CSS hides all screen chrome (`.screen-only` under `@media print`).
- Export produced valid JSON (2 quotes); storage wipe + import round-trip
  restored both quotes.
- Hostile import (`<img onerror>`, `<script>`, `<svg onload>`, `<iframe
  src=javascript:>`): zero script/svg/iframe elements created; payloads render as
  inert text via textContent.
- Demo loads 2 quotes (first has percent discount + mixed taxable items);
  clear-all empties the list.
- Dark-mode toggle sets `data-theme="dark"` and persists across reload; business
  profile persists across reload.
- 390px viewport: 0px horizontal page overflow, no console errors, all visible tap
  targets ≥ 40px.

## 2026-09-19 — validation defect fixes (independent ChatGPT-directed QA)
Backup: `index.html.bak-2026-09-19-quotefix`. All verified in headless Chromium
(29/29 checks, zero console/page errors); bundle ZIP rebuilt.
- **Duplicate descriptions rejected:** `addOrSaveItem()` now enforces case-insensitive
  description uniqueness within a quote ("Description must be unique within a
  quote." in the existing `ni-err` style). Editing an item keeps its own
  description without a false duplicate.
- **Quantity must be ≥ 1:** `addOrSaveItem()` rejects qty 0 and negatives
  ("Quantity must be 1 or more."); `cleanQty()` (import sanitizer) now treats
  qty < 1 as invalid so imported zero-qty records are skipped, consistent with
  the "invalid records are skipped" import rule.
- **Negative tax rate:** `bindEditor()` now shows a visible inline message in the
  new `dt-err` error container ("Tax rate must be 0 or more."), clamps the model
  to 0 and writes 0 back to the field. Message clears once the value is valid.
- **Negative discount value:** same pattern — visible inline message
  ("Discount value must be 0 or more."), clamp to 0, field written back.

## 2026-09-19 — review round 1 fixes (outside-AI review round)
Backup: `index.html.bak-2026-09-19-r1`.
- **Fractional quantities allowed:** qty rule corrected to > 0 (was ≥ 1, a
  regression — demo data uses qty 2.5 and half-hour billing is standard).
  Message is now "Quantity must be more than 0." Fixed in both
  `addOrSaveItem()` and `cleanQty()` (import sanitizer). Qty 0 and negatives
  still rejected.
- **Tax rate > 100%:** `bindEditor()` now shows a visible inline message
  ("Tax rate can't be more than 100%.") in `dt-err`, writes 100 back to the
  field, and uses 100 in the model. Message clears once the value is valid.
- **Mid-session storage failure:** `save()` now calls `showStorageNotice()`
  whenever the in-memory fallback engages (quota/disabled mid-session), so the
  `#storage-notice` banner warns the user edits aren't persisting. Init uses
  the same helper.
- **SEO metadata** (GUMROAD-LISTING.md only; staging folder/URL untouched):
  title → "Free Contractor Estimate & Quote Builder | Printable Template";
  slug → `free-contractor-quote-builder`; description opens with the new
  keyword-first paragraph; tags drop `small business`/`invoice quote` and add
  `proposal generator`, `handyman estimate template`, `freelance invoice maker`,
  `offline estimate app`.

## 2026-09-19 — review round 2 fixes (outside-AI review round 2)
Backup: `index.html.bak-2026-09-19-r2`.
- **Quote date clear write-back (FIX 1):** in `bindEditor()`, clearing the quote
  date input used to leave stale state — the field showed empty while `q.date`
  silently kept its old value, so the totals list / print view showed a date the
  user thought they removed. Now the field is written back to `q.date` when the
  input is empty/invalid (same write-back pattern as the tax-rate fix), so field
  and state always agree. `validUntil` already handled empty correctly.
- **Description keyword-first (FIX 2):** GUMROAD-LISTING.md description now opens
  with "Free contractor estimate and quote builder app. Create printable job
  proposals, service estimates, and invoices offline instantly with no signup
  required." before the brand line; rest of the description unchanged.

## 2026-09-20 (re-verification pass)
- **Cover dimensions (FIX 3):** gallery/0-cover.png center-cropped from 1280x800 to
  1280x720 to match the established cover standard (W9Track, ZoneSync precedent).
  Square thumbnail unchanged at 1200x1200.
- **ZIP rebuilt:** quotecraft-bundle.zip regenerated with the new cover; excludes
  local .bak working files (was 15 entries incl. .bak files, now 13 clean entries).
  index.html in ZIP byte-matches the live source.

## 2026-09-20 (outside-AI browser QA findings — parent fixes)
- **FIX 4 — Stale quotes list on tab switch (real defect, low-medium severity):**
  the "Quotes" tab handler called `showView("list")` without `renderList()`, so
  the list showed stale customer/total after edits until the editor "Back" button
  or a page reload. The tab handler now calls `renderList()` when switching to
  the list view (matches the Back-button path). Retested: list shows $124.00
  after editing $80.00 -> $124.00 and returning via the Quotes tab.
- **FIX 5 — Discount cap feedback (very low):** percent discounts over 100% and
  flat discounts over the subtotal were silently capped (total $0.00, no negative),
  while tax>100 showed "Tax rate can't be more than 100%." bindEditor now shows
  "Discount percent can't be more than 100%." / "Discount can't be more than the
  subtotal." and clamps the input value, mirroring the tax pattern.
- **FIX 6 — Strict ISO date validation (very low):** the `/^\d{4}-\d{2}-\d{2}$/`
  check accepted impossible calendar dates like "2026-13-99" from crafted imports.
  New `isDateISO()` helper validates month 01-12 and day ranges incl. leap years;
  used at all 4 date sites (import sanitize + editor write-back). Bad dates fall
  back to today (import) or restore the stored date (editor).
- **FIX 7 — Totals label clarity (very low):** the "Taxable subtotal" row showed
  pre-discount taxable lines while tax is computed on the post-discount base.
  Relabeled "Taxable subtotal (before discount)"; behavior unchanged, footnote
  still documents the tax-after-discount rule.
- **Regression retest:** full Playwright harness 11/11 PASS on the fixed source;
  targeted fix suite 8/8 PASS (tab refresh, both discount messages + clamps,
  import/editor date rejection, zero JS errors).
- **FIX 8 — Cover re-crop (top-crop):** the 1280x720 center-crop clipped the
  QuoteCraft header title. Regenerated as a top-crop from gallery/1-quotes-list.png
  (verified byte-identical to the center-crop source before replacing); full
  header, product name, tagline, and populated quotes table now visible.
- **Gallery note:** gallery/2-editor-items.png still shows the pre-FIX-7 totals
  row label "Taxable subtotal" (now "Taxable subtotal (before discount)" in the
  UI). Layout, data, and totals unchanged; screenshot otherwise current.
