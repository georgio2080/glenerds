# HabitTrack — Changes

## 2026-09-20 — Data-hardening + visual pass (verification round)
- Fixed: malformed stored habits (weekdays as string, missing `created`, null entries)
  could throw on load and brick the habit list. Storage is now sanitized on load:
  unrecoverable entries are dropped, trivially repairable fields (bad weekdays,
  invalid `created` date, bad color/icon) are repaired to safe defaults.
- Hardened JSON import: invalid entries are skipped (count reported), impossible
  calendar dates (e.g. 2026-02-30) rejected, notes truncated to 500 chars, import
  rejected when no valid habits remain — state untouched on failure.
- Hardened CSV import: strict calendar-date validation, 500-char note truncation,
  skipped rows reported.
- Added "Last 7 days" activity bar chart (done/partial stacked bars, pure CSS —
  still fully offline, no dependencies).
- New covers: professional 1280×720 cover and redesigned 1200×1200 square cover
  (real populated UI in a browser frame).

## 2026-09-20 — Bench adjudication fixes (Grok + Gemini functional re-review)
- Fixed HIGH: stored XSS via crafted habit id in JSON imports (id interpolated raw
  into innerHTML). Habit ids are now charset-locked (`[A-Za-z0-9_-]`, 1–64 chars)
  with `__proto__`/`constructor`/`prototype` blocklisted; bad ids regenerate via
  `uid()`. Self-healing on next load. Also closes the JSON proto-pollution vector.
- Fixed: "longest streak" header showed the max *current* streak; now shows the
  true best (`st.best`).
- Fixed: "Last 7 days" chart counted phantom misses before a habit's created date.
- Fixed: completion % counted an unlogged today as a miss; now uses the same
  open-day rule as the streak logic.
- Fixed: tapping an active status to clear it wiped the note; the note is kept.
- Fixed: JSON import now runs the full `sanitizeLog` (was a weaker inline check).
- Fixed: detail "Check-ins" ignored the created date; now consistent.
- Fixed: CSV export/import round-trips note-only entries (blank status).
- Dismissed as false positives: DST infinite-loop claim (Y/M/D constructor is
  DST-safe, node-verified across 2026 transitions) and the streak-algorithm claim.
- Fixed (copy/SEO bench, Gemini leg): page title trimmed to 51 chars so it
  survives SERP truncation; added canonical, Open Graph and Twitter card tags
  (og:image = square cover).
