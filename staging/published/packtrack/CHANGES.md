# PackTrack — Build Log

## 2026-09-21 — visual representation pass (Glen's "spruce up" order)
- **New "Unpack progress by room" bars** on the Dashboard, between the room
  pills and the overall unpack bar: per-room unpacked/total with % and green
  gradient fills matching the existing overall progress style. Live-updates
  through the app's own render path (unpack-mode toggles -> save -> renderAll
  -> renderDashboard). Group-level aria-label summarizes every room.
  Verified headlessly: 3 room bars, correct counts, live update on toggle
  (Kitchen 2/9 = 22%); screenshot inspected.

**App:** PackTrack (Moving Box Inventory Indexer) — free-loop app #2
**Built:** 2026-09-19
**File:** `index.html` (single file, ~36 KB, zero external requests)

## Build notes

- Data model: `state = { boxes: [{number, room, label, color, fragile, packed, items: [{text, unpacked}]}], customRooms, nextNumber }` persisted to localStorage key `packtrack-v1`.
- Box numbers start at 101, auto-increment; user-editable with duplicate guard and 1–9999 validation.
- Rooms: 8 defaults + user-addable custom rooms via the "New room" field (sanitized, deduped, capped at 50).
- Color tag: 6 swatch buttons (none/blue/green/red/yellow/purple), aria-pressed toggle.
- Search: instant (120 ms debounce), case-insensitive partial match across items, rooms, labels; matches highlighted with `<mark>` built via DOM text nodes (no innerHTML).
- Security: every user/imported string enters the DOM via `textContent`/`.value`/text nodes. Import pipeline runs through `sanitizeState`/`sanitizeBox`: finite numbers clamped, strings trimmed + length-capped (room 40, label 40, item 120), color restricted to an allowlist, items capped (300/box), boxes capped (500), duplicate box numbers dropped. Corrupt localStorage falls back to empty state silently.
- Dark mode: `data-theme` on `<html>`, CSS variables, prefers-color-scheme on first load, persisted to `packtrack-theme`, visible toggle in header.
- Print labels: screen-hidden `.print-label` container; print button builds the label DOM and adds `printing-label` to `<body>`; print CSS hides the app, shows one label per page (big number, room, tag, FRAGILE banner, item list, count). "Print all labels" builds one label div per box. Class removed on `afterprint` + 2s fallback.
- Unpack mode: toggle in the Boxes toolbar; in unpack mode each item gets a checkbox; progress bar + % label on dashboard; "Fully unpacked" stat counts packed boxes with all items unpacked.
- Empty states: dashboard zeroes, "No boxes yet" note, search no-hit message, data note about localStorage.
- No emojis anywhere in UI chrome. Footer: "by Glenerds" → https://glenerds.gumroad.com.

## Fixes during build

1. **Print-cleanup race:** `window.print()` returns immediately in headless; class removal via `afterprint` alone can leave the app hidden if the event never fires — added a 2 s `setTimeout` fallback so the app always reappears.
2. **Color-swatch form submission:** swatch buttons sit inside the new-box form — explicitly `type="button"` so they never trigger submit.
3. **"Other" rooms not in defaults:** boxes imported with an unknown room keep the room string and render in the per-room pill list via `allRooms()`-based filtering (pill only shows rooms that have boxes, so no stray select options needed).
4. **Item add focus:** after adding an item with Enter the input keeps focus for fast multi-add.

## QA — Playwright (system Chromium /opt/meta-chromium/chrome, headless, file://) — 2026-09-19

**22/22 checks passed.**

| Check | Result |
|---|---|
| No console errors on load | PASS |
| Box create (auto number, custom room, fragile, color) | PASS |
| Duplicate box number rejected | PASS |
| Item add via Enter + remove | PASS |
| Search finds items, case-insensitive, hand-checked ("hdmi" → Box 101 Kitchen, HDMI highlighted) | PASS |
| Seal/unseal box | PASS |
| Unpack mode checkboxes + progress bar updates ("Unpacked 1 of 2 items (50%)") | PASS |
| Print label view renders (print media emulation: label visible, big "Box 101", FRAGILE, app hidden) | PASS |
| Export JSON (download valid, box 101 present) | PASS |
| Import JSON round-trip (Box 201, items, custom room loaded) | PASS |
| Malformed import rejected gracefully (alert + existing data intact) | PASS |
| Hostile import sanitized (number clamped, strings length-capped, color allowlisted, no script content in DOM, truthy "fragile" not coerced) | PASS |
| Demo data load (2 rooms / 4 boxes / ~20 items) + clear-all | PASS |
| Dark mode toggle persists across reload (dark → dark) | PASS |
| 390px mobile layout, no horizontal overflow | PASS |
| Zero external requests (network log: no file://-external requests) | PASS |

QA notes: two harness-only issues fixed during the run — (1) `ElementHandle.check` race
(checkbox re-renders on change; switched to `dispatch_event("click")`), (2) duplicate
`page.on("dialog")` handlers throwing "already handled"; consolidated to a single
record-and-accept handler. No app code was changed for either.

## 2026-09-19 — outside-AI QA defect fixes (verified headless Chromium)
- Seal/Unseal buttons: removed the misleading `aria-pressed` attribute. The
  button label already flips between "Seal box" and "Unseal", which conveys the
  state; `aria-pressed` implied a toggle-button pattern that didn't fit.
- Export JSON: added a visible confirmation line ("Exported N boxes — download
  started (packtrack-backup.json).") in the Backup & demo section, cleared on
  the next render. The download itself was verified working (real download
  event for packtrack-backup.json); the message makes success observable.
- "Add item inputs don't accept text" report investigated: could not reproduce
  — `fill()`, `keyboard.type()`, and Enter-to-commit all work with demo data
  and with boxes added via the form; the item count updates correctly. The
  builder's own QA table (same file, same flows) also passes. No code change.
- "Export does nothing" report investigated: the download fires correctly
  (verified via Playwright download event); only the confirmation message was
  added. No change to download mechanics.
- "Dark-mode toggle does nothing" report investigated: could not reproduce —
  clicking the toggle sets `data-theme="dark"` on `<html>` and the computed
  body background changes light→dark; the builder's QA also passes this. No
  code change.
- Verified in headless Chromium (Playwright): seal buttons carry no
  aria-pressed and still toggle Sealed/Open; export downloads
  packtrack-backup.json and shows the confirmation; add-item and theme toggle
  regressions pass; zero console/page errors.

## 2026-09-19 — review round-1 defect fixes
- Room select didn't stick after adding a box: submit handler called
  `refreshRoomSelect(room)` then `form.reset()`, so the select snapped back
  to the first room. Reordered — `form.reset()` now runs first, then the
  room is re-applied (the `room` string is a JS variable, unaffected by reset).
  Packing several boxes for one room no longer forces re-selecting the room.
- SEO: description now opens keyword-first ("Free Moving Box Inventory
  Tracker — ...") instead of brand-first; title trimmed to 82 chars.

## 2026-09-19 — review round-2 defect fixes
- Add-item lost keyboard focus after every commit: `commit()` called
  `inp.focus()` on an input that `renderAll()` had just destroyed (no-op).
  Now re-queries the fresh input via its aria-label ("Add item to box N")
  and focuses that. Verified live: focus stays in the input, second item
  typed without clicking goes through, zero page errors.
- Import hardening: `sanitizeState` now derives `nextNumber` from max box
  number + 1 when the imported JSON lacks the field (previously reset to
  101, causing a confusing "Box 101 already exists" error on first add).
  Verified: missing -> 108 for boxes 101/107; present respected; empty -> 101.

## 2026-09-19 — review round-3 defect fix
- Reset button didn't reset the color-swatch state: native reset wipes form
  fields but not module-level `selectedColor` or swatch `aria-pressed`, so a
  box submitted after Reset still got the previously picked color. Added a
  `form.addEventListener("reset", ...)` that clears `selectedColor` and
  re-applies `aria-pressed` (same pattern as the submit handler). Verified
  live: red pressed -> Reset -> red unpressed, "No color" pressed, submitted
  box has color "", zero page errors.
