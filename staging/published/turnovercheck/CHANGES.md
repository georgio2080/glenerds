# TurnoverCheck — Build Log (CHANGES.md)

## 2026-09-21 — visual representation pass (Glen's "spruce up" order)
- **New "Room progress" card** on the Checklist tab, between the overall
  progress card and the room list: per-room completion bars (name, done/total
  with %, gradient progress fill), live-updating as tasks are checked, each
  track an aria progressbar plus a group-level aria summary. Card hides when
  there are no rooms. Verified headlessly: 6 room bars, correct counts,
  live update on task toggle (0/8 -> 1/8 = 13%); screenshot inspected.

App #3 of the free-product loop. Single-file offline HTML micro-tool.
Spec: `~/workspace/microtool-research/free-loop/app3-turnovercheck-SPEC.md` (v1, picked 2026-09-19).

## Build — 2026-09-19

- Built `index.html` from scratch (IP clean-room: no copied code, copy, or branding).
- Two tabs with `role=tablist`/`tab`/`tabpanel`; mouse click + ArrowLeft/ArrowRight/Home/End
  keyboard navigation; roving tabindex.
- **Checklist tab:** 6 default rooms (Kitchen, Living Room, Bedroom(s), Bathroom(s), Laundry,
  Outdoor / Entry) with 41 default tasks total. Check/uncheck with per-room counts, overall
  progress bar (`role=progressbar` + `aria-valuenow`), "Start turnover" timestamp, per-room
  start/stop elapsed timers (persist across reload, resume correctly), confirm-armed
  "Reset for next guest" (unchecks all, clears clock/timers), completion summary with
  `aria-live="polite"` showing total time. Tasks: add / delete / move up-down. Rooms:
  add / rename (inline) / remove (confirm-armed).
- **Damage Log tab:** property name; incident form (room dropdown synced to room list,
  item/area, type damage|missing|excessive cleaning, severity minor|moderate|major,
  description, photo-reference text note — no photo upload). Incident list with edit
  (reuses the form, Cancel edit button) and delete (confirm-armed). "Generate report"
  renders a plain-text block (property, date, numbered incidents with severity/type/
  timestamp/details/photo ref, totals line) into a `<pre>` + "Copy report" button
  (Clipboard API with textarea+execCommand fallback).
- **Data:** localStorage persistence (saved on every mutation + beforeunload/hidden tab).
  Export JSON downloads a timestamped backup. Import sanitizes everything: allowlisted
  enums, finite numbers, length-capped strings (60–2000 chars), capped array sizes;
  invalid entries dropped, missing ids generated; running timers without a valid
  `since` are stopped. Demo data (sample turnover + 2 incidents) and clear-all, both
  confirm-armed (two-tap inline confirm, 6 s expiry).
- **Security:** zero `innerHTML` in app code; all dynamic DOM via `createElement` +
  `textContent` / `.value`. Zero external requests (only link is the footer anchor).
- **Dark mode standard:** visible toggle, `prefers-color-scheme` default, localStorage
  persistence, CSS-variable palette, readable contrast in both themes.
- **Mobile-first:** 390px viewport verified, no horizontal overflow, all interactive
  elements ≥ 40 px tap targets, labeled inputs, no emojis in UI chrome.
- **Footer:** discreet "by Glenerds" → https://glenerds.gumroad.com.

## Defects found and fixed (fix-without-asking)

1. **`hidden` attribute ignored on buttons (2026-09-19, caught by Playwright QA).**
   `.btn { display: inline-flex }` overrode the UA stylesheet's `[hidden] { display: none }`,
   so "Start turnover"/"Restart clock"/"Cancel edit" never actually hid. Fix: added global
   `[hidden] { display: none !important }` rule. QA re-run confirms correct show/hide.

## QA results (Playwright, system Chromium /opt/meta-chromium/chrome, headless, 390×844)

41/41 passed. Per-check list (spec QA list mapping):

- no console errors (load + full run): PASS
- zero external requests: PASS
- checklist check/uncheck + progress math (Kitchen 8 tasks, 41 total, 1/41 → 2%, aria-valuenow, revert): PASS
- custom room add / task add / task delete / room remove: PASS
- timer start/stop (ticks, stops accumulating, elapsed persists across reload): PASS
- reset confirm (requires second tap, resets checks + clock + timers): PASS
- incident add / edit / delete (fields, severity badge, photo note): PASS
- report text contains all incidents + severity + property + totals line: PASS
- copy button works (clipboard read-back verified): PASS
- export/import round-trip (fresh browser profile, file carries property + 2 incidents): PASS
- hostile import sanitization (script/img/svg payloads render as inert text, zero injected
  elements, enum fallbacks minor/damage, 2000-char cap, invalid numbers dropped): PASS
- demo data + clear-all: PASS
- dark mode persists across reload: PASS
- 390px mobile (no h-overflow, touch targets ≥ 40 px): PASS
- aria-live="polite" on completion summary: PASS
- tab keyboard navigation (arrow keys): PASS

Full QA script: `/tmp/tc_qa.py` (ephemeral; re-runnable against the file).

## 2026-09-19 — outside-AI QA defect fixes (verified headless Chromium)
- Deleting an incident now invalidates the generated incident report: added
  `clearReport()` (clears text, hides output, disables Copy) and called it in
  the incident delete handler. Previously the report snapshot stayed on screen
  after the last incident was deleted.
- "Outdoor / Entry never shows 0:00 timer" report investigated: could not
  reproduce — all six room cards render "0:00" initially, the Outdoor/Entry
  timer counts while running, freezes on stop, and persists across reload. No
  code change.
- Verified in headless Chromium (Playwright): report cleared/hidden/copy
  disabled after deleting the last incident; regenerating with zero incidents
  yields "No incidents recorded."; all six timers show "0:00"; zero
  console/page errors.

## 2026-09-19 — review round-1 defect fixes (verified headless Chromium)
- Stale incident report: `clearReport()` was only called from the incident
  delete handler. Now also called from the incident save handler, the import
  success path, the demo loader, and clear-all — the generated report is
  invalidated on every incident-list mutation. Verified: report generated ->
  incident edited -> report box hidden and Copy disabled; zero page errors.
- Silent storage failure: `save()` swallowed failures with only a comment.
  Added `storageOK` flag + `showStorageWarn()` surfacing a persistent
  `role="alert"` banner ("Browser storage failed — your changes are only kept
  until this tab closes."). `load()` failure also shows it. Same issue class
  previously fixed in SubAudit.
- Import now uses the app's two-tap `armConfirm` ("Tap again to import")
  instead of silently replacing all state on file pick — matches the
  demo-load/clear-all destructive-action pattern. Verified armed label.
- SEO: Gumroad listing description rewritten keyword-first
  ("Free Airbnb Turnover Checklist & Damage Log — TurnoverCheck").
