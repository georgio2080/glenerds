# ZoneSync — build log

## 2026-09-20 — audit fixes (fix-without-asking)
1. **Import no longer duplicates members.** Re-importing an export (or any JSON
   containing a name already on the team, case-insensitive) now skips the
   duplicate instead of appending it, so export→import round-trips are
   idempotent. Skipped duplicates count in the "skipped N invalid entries"
   message.
2. **Member cap (200).** Import, the add-member form, and localStorage load all
   cap the team at 200 members so a hostile/oversized JSON payload can't bloat
   the DOM.
3. **SEO listing touch-ups** (GUMROAD-LISTING.md): added explicit
   "no subscription" to the free-line differentiators; "MORE FROM GLENERDS"
   now reads as an explicit "Made by Glenerds" line.
All verified with a 58-check Playwright QA (file://, offline, dark mode,
validation, DST gap, mobile 360x800) — zero console/page errors.

## 2026-09-19 — initial build (app #8, free-loop)
Single-file offline app per SPEC v1: team time-zone overlap heatmap,
golden-hour detection, meeting planner, JSON export/import, demo data,
dark-mode standard, "by Glenerds" footer. All code written from scratch
(clean-room); zero external requests; works from file://.

Time math: every conversion goes through `Intl.DateTimeFormat` with an
explicit `timeZone` on real `Date` instants — no hand-rolled UTC offsets.
Wall-clock-to-UTC uses a fixed-point iteration `U = W - off(U)` against the
real tz database (DST-safe). All DOM built with `createElement` /
`textContent` / `.value` — no `innerHTML` anywhere. Time zones allowlisted
against `Intl.supportedValuesOf('timeZone')` (+ curated fallback);
imported members fully sanitized (name <= 50 chars, tz in allowlist,
hours integer 0–23).

## Defects found and fixed (all during Playwright QA, fix-without-asking)
1. **`Intl.supportedValuesOf('timeZone')` omits `UTC` in this Chromium build**
   (418 zones, no `UTC`). `select_option('UTC')` failed and the default viewer
   zone silently fell back to the first list entry. Fix: always append `UTC`
   to the list if missing.
2. **`zonedToUtc` fixed-point bug (real correctness bug).** The iteration was
   `U = U - off(U)` (anchored on the moving guess) instead of `U = W - off(U)`
   (anchored on the fixed wall time). It converged correctly only when the
   offset was 0, so every UTC-viewer test passed while any other viewer zone
   was shifted (caught by the hand-verified NY golden-hour check: got
   01:00–02:00, correct is 09:00–10:00). Rewrote the iteration; verified across
   UTC, America/New_York, Europe/Berlin, Asia/Tokyo, Australia/Sydney,
   America/Los_Angeles.
3. **Members table overflowed the page on 390px** (intrinsic table width
   pushed `scrollWidth` 32px past the viewport). Fix: `#members-list` and
   `#plan-results` get `overflow-x: auto` like the heatmap wrapper.
4. **Midnight chip rendered "23:00–24:00".** Golden range end now wraps
   (`% 24`) → "23:00–00:00".

## QA (Playwright, headless system Chromium /opt/meta-chromium/chrome)
49/49 checks pass. Coverage: page load; demo data; hand-verified heatmap math
(viewer UTC hour 13 → NY 09:00 / London 14:00 / Berlin 15:00 / Tokyo 22:00,
all in work hours, count 4, golden chip 13:00–14:00; hour 14 → Tokyo 23:00
end-exclusive off, count 3; hour 0 → count 0); overnight shift wrap
(22→06: Tokyo 22:00 in, 21:00 out, 05:00 in; golden 13:00–15:00); golden-hour
detection incl. chip ranges; no-overlap message + tip; meeting planner
(2026-09-19 13:00 UTC → Tokyo 22:00 in work hours, verified against known
UTC+9 offset; NY 09:00 in work hours); viewer tz change re-renders
(NY → golden 09:00–10:00); add/edit/delete members; localStorage persistence
across reload (members + viewer tz); export/import round-trip; hostile import
(bad tz string, hour 99, negative hour rejected — 2 skipped, 1 valid imported,
`<b>` name rendered as escaped text, page intact); demo + clear-all (confirm
dialog); dark mode toggle + persistence + prefers-color-scheme default;
zero console errors; zero page errors; zero external requests; 390px mobile
(heatmap scrolls horizontally, no page-level overflow, all visible buttons
>= 40px); aria-live="polite" on golden hours; scope="col"/"row" on table
headers; labeled inputs.

## Open / uncertain
- Reference date for the heatmap is "today" in the viewer time zone; hours
  are whole hours only (no :30 granularity) — matches the spec.
- `start == end` (e.g. 9→9) is treated as zero work hours, documented in the
  form hint only via the end-exclusive note.

## 2026-09-19 — outside-AI QA defect fixes (verified headless Chromium)
- Meeting planner local-times table now refreshes after member add/edit/
  delete. Root cause: the planner table was built once on form submit and
  `renderAll()` never re-rendered it, so it went stale. Fix: plan generation
  extracted into `renderPlan()` with a `planGenerated` flag; `renderAll()`
  re-renders the plan when one is showing (also keeps it correct on viewer
  time-zone change).
- Work start == end (e.g. 9 to 9) is now rejected with an inline warning
  ("that would be a zero-hour shift...") instead of silently saving a member
  who is never in work hours. Overnight ranges like 22 to 6 still work.
- Duplicate member names are now rejected with an inline message
  ("A team member named X already exists..."). Check is case-insensitive and
  excludes the member being edited, so saving an edit without renaming still
  works.
- Verified in headless Chromium (Playwright): plan table went 1 -> 2 rows on
  add, renamed Ava/Liam to Ava/Emma on edit, back to 1 row on delete;
  9->9 rejected with the zero-hour warning, 22->6 accepted; "ava"
  rejected as duplicate of "Ava"; self-edit rename-safe; zero console/page
  errors.

## 2026-09-19 — review round 1 fixes (outside-AI review)
- <title> changed from brand-first "ZoneSync — Remote Team Time-Zone Overlap"
  to keyword-first "Free Time Zone Overlap Calculator for Remote Teams (ZoneSync)".
- Meta description changed from brand-first to keyword-first:
  "Find the best meeting times for your distributed team with a free offline
  time zone overlap calculator and 24-hour heatmap. Works fully offline."
- Gumroad listing description first line changed from brand-first
  "🌍 ZoneSync — Free Remote Team Time-Zone Overlap Visualizer" to keyword-first
  "🌍 Free Time Zone Overlap Calculator — ZoneSync: Find Meeting Times for Remote Teams".
  (Gumroad title was already keyword-first; no change.)
- "Load demo team" no longer silently wipes existing members: when members exist
  it now asks "Replace your current team with the demo team? This cannot be
  undone." (same pattern as clear-all). With an empty member list it loads
  directly without a dialog.
- Verified live in headless Chromium (Playwright, system Chrome): add member,
  demo-click with members -> confirm fires -> dismiss keeps the member ->
  accept loads the demo team (Ava, Liam, Mia, Kenji); dark mode persists across
  reload; zero console/page errors.
