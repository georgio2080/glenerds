# MoveInProof — build log

## 2026-09-21 — Retroactive sweep baseline (Glenerds sweep, build phase)
- Standardized the header cluster: `.g-header-actions` wrapper with More Apps pill first, icon-only dark-mode button (44x44px, moon/sun icon, no text label, dynamic aria-label/title), new icon-only sound toggle (44x44px, 🔊/🔇) at the far right.
- Added the standard WebAudio sound engine (oscillator-only, no audio files, offline): click/select/success/error/toggleTheme, on by default, persisted at `moveinproof.sound`, wired into theme toggle, add room (with validation error), delete room, demo load, clear, export/import, and print.
- Made the report's condition-overview bars interactive: each row (room ratings, defect severities) is a keyboard-accessible button — activating it spotlights the row and shows which rooms or defects it counts in a detail line; activating again restores.

## 2026-09-21 — visual representation pass (Glen's "spruce up" order)
1. **New "Condition overview" in the Move-In Condition Report**: Room ratings
   distribution (Excellent/Good/Fair/Poor/Not rated) and Defects-by-severity
   (Minor/Moderate/Major) bar groups at the top of the report, theme-aware
   colors (--good/--accent1/--warn/--bad), counts in a right column, aria-labels
   per group, print-color-adjust so bars survive printing. Only renders when
   rooms exist. Verified headlessly with demo data (1 Good, 1 Fair; 1 minor,
   2 moderate); screenshot inspected.

## 2026-09-19 — Initial build (spec v1)
- Single-file offline app at `staging/moveinproof/index.html` (~39 KB, zero external requests, works from file://).
- Property header (address, landlord/manager, tenant names, lease start, move-in date defaulting to today), saved to localStorage on change.
- Rooms: 6 seeded defaults (Living Room, Kitchen, Bedroom, Bathroom, Hallway, Exterior/Balcony); add/delete custom rooms; per-room condition rating (Excellent/Good/Fair/Poor radios), notes, room-level photos.
- Defects per room: item/area, type (scuff/stain/crack/dent/missing/broken/dirty/other), severity (minor/moderate/major), description, auto timestamp; add/edit/delete.
- Photo attach (per room and per defect): `<input type="file" accept="image/*">` multiple; canvas downscale to max 1200px longest edge, JPEG q0.7; thumbnail grid with per-photo delete; storage-quota failure shows a message naming the largest photo's location and size.
- Printable handover report: property header, per-room ratings/notes, defects with severity + thumbnails, tenant/landlord signature blocks (printed name, signature, date); print stylesheet hides app chrome and forces light colors.
- JSON export (download) / import (file picker) with aggressive sanitization: photos allowlisted to `data:image/jpeg`/`data:image/png` only, strings length-capped, enums allowlisted, unknown keys dropped.
- Demo data (2 rooms, 3 defects, no photos) + clear-all (confirm dialog).
- Dark mode standard: visible toggle, `prefers-color-scheme` default, localStorage persistence, CSS variables, pre-DOMContentLoaded set to avoid flash.
- Discreet footer: "by Glenerds" → https://glenerds.gumroad.com. No emojis in UI chrome.
- Accessibility: labeled inputs, keyboard-operable controls (file inputs stay focusable via visually-hidden class), `aria-live="polite"` on the report section and status message, 44px minimum tap targets, mobile-first layout.

### Security notes (implemented)
- Zero `innerHTML`/`outerHTML`/`document.write` in the file (verified by grep; only prose comments mention it).
- Photos render only via `img.src = dataURL`; `isPhotoURL()` allowlist enforced on attach (post-downscale), on every stored photo at load/import, and SVG dataURLs are always dropped.
- All other user/imported strings rendered via `textContent` or DOM text nodes.

### QA results (Playwright, real system Chromium /opt/meta-chromium/chrome, headless) — 13/13 pass
- property header save: PASS (values persisted across reload via localStorage)
- room add/rating/notes: PASS (Garage, rating Poor, notes persisted)
- defect add/edit/delete: PASS (fields + auto timestamp on add; edit saves; delete removes)
- photo attach downscales: PASS (3000x2000 PIL test JPEG → stored dataURL starts `data:image/jpeg`, 15,415 chars vs 176,724 original — ~11x smaller)
- photo delete: PASS
- hostile import neutralized: PASS (svg dataURLs dropped from room + defect photos; `<script>`/`<img onerror>` strings rendered as inert literal text; only the app's own 2 script tags in DOM; print-emulation screenshot confirms inert rendering)
- print report renders: PASS (print media: report visible, app chrome hidden, signature blocks with 6+ sig lines)
- export/import round-trip: PASS (1 room exported → clear → import → 1 room back)
- demo + clear-all: PASS (demo = 2 rooms / 3 defects / 0 photos; clear-all empties rooms + header)
- dark mode persists: PASS (dark survives reload; toggled back to light after)
- 390px mobile: PASS (no horizontal overflow; all visible buttons/file-labels ≥40px tall)
- zero external requests: PASS (no http/https requests during full run)
- no console errors: PASS (no console errors, no pageerrors across the whole run)

### QA fixes applied
- None needed — all checks passed on the first run. No defects found.

## 2026-09-19 — outside-AI QA defect fix (verified headless Chromium)
- Prefilled property address now appears in the handover report on load.
  Root cause: the report rendered only from `state.header`, which updated
  solely on input `change` events — and `bindHeader()` unconditionally
  overwrote the address input with the (empty) stored value, destroying any
  prefilled/autofilled value. Fix: `bindHeader()` no longer clobbers a
  non-empty input, and a new `syncHeaderInputsToState()` (called on init
  before the first report render) pulls visible prefilled values into state
  and saves them.
- Verified in headless Chromium (Playwright): prefilled "999 Prefill Ave"
  survives load, renders in the report, and persists to localStorage; saved
  state still populates input + report; demo address renders; typing + change
  still updates the report; zero console/page errors.

## 2026-09-19 — review round 1 (outside-AI; coordinator report truncated mid-delivery, recovered from transcript + Gemini pass files)
- Review round 1 ran against 39,497 bytes (sha256 6f4802f8…): two Gemini API passes (security + functional), full-source read, headless Chromium live render + 8-image gallery pixel comparison.
- Coordinator verified gallery: all 8 images accurate; live render zero console/page errors; all 8 functional areas verified clean.
- Dropped (false/fabricated): pass-1 claim that loadDemo() "bypasses sanitizeState()" is a defect — demo values are hardcoded safe literals, sanitizeState is for untrusted input; not a real issue.
- 1 verified should-fix: **Gumroad description opened brand-first** ("📸 MoveInProof — Free Apartment Move-In Damage Logger"), violating the SEO-first keyword-first rule.
- Same rule applied to the app's own HTML: <title> and meta description were also brand-first.
- Fixes applied (2026-09-19): listing description first line → "📸 Free Apartment Move-In Checklist & Damage Logger — MoveInProof"; <title> → "Free Apartment Move-In Checklist & Damage Logger (MoveInProof)"; meta description → "Free apartment move-in checklist and damage logger: document your rental's condition room by room with photos, print a timestamped handover report. Offline, single-file tool (MoveInProof)."
- Verified headless Chromium: new title renders, header + report load, demo renders report, zero console/page errors.
- New bytes: 39,558; sha256 b9b5ec4e6a6dbc6911e428e29e855628be0b6c70c54483b2d050b26344badf08.

## 2026-09-19 — review round 2: ZERO ISSUES, signed off
- Round 2 ran against the exact updated bytes (39,558; sha256 b9b5ec4e…badf08): two Gemini API passes on full source bytes (security + functional/SEO), independent source verification, headless Chromium live render + 8-image gallery comparison, listing SEO recheck.
- Verified clean: no XSS surface (no executable innerHTML/outerHTML/document.write; photo dataURLs allowlisted at 4 enforcement sites; user strings via textContent at 8 sites), import sanitization path, localStorage quota/error handling, report completeness, edge cases, no dead controls, dark mode persistence, keyword-first title/meta/slug/tags, gallery accurate, zero console/page errors.
- Should-fix: none. Should-improve: none. Nits: none. No false claims to drop.
- Parent verified final bytes independently (title + meta + hash match).
- Signed off 2026-09-19 12:30 EDT. Staging row marked Passed locally. Deploy queued for when Netlify credits reset (full-site ZIP rebuilt same turn).
