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
