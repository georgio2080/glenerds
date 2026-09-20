# GardenCal — Vegetable Garden Planting Calendar by Zone

An offline, single-file web app that tells you exactly when to start seeds indoors,
transplant, direct sow, and plant for fall — based on your USDA hardiness zone. No account,
no subscription, no internet needed. Open `index.html` in any browser (even from `file://`).

## What it does

- **Zone-based schedules** — pick USDA zone 3–10; the app computes dates from average last
  spring / first fall frost dates for your zone.
- **Your exact frost dates** — optionally override with your town's real dates (MM/DD) for
  precision without any lookup or account.
- **36 vegetables & herbs** — tomatoes to garlic, each with indoor-start, transplant,
  direct-sow, harvest-estimate, and fall-sow dates, plus growing notes.
- **Month-by-month view** — a 12-month action calendar with a "Right now" card highlighting
  what to do this month.
- **Crop schedule table** — every date per crop in one printable table.
- **Choose your crops** — check only what you actually grow; the calendar adapts.
- **Fall & succession planting** — fall sow dates computed back from your first fall frost;
  garlic handled as a proper fall-planted crop.
- **Dark mode** — visible toggle, follows your system preference on first load, remembered.
- **Your data stays yours** — zone, custom dates, and crop picks saved in localStorage.
  JSON export/import for backup.
- **Print / PDF** — clean print stylesheet for a one-page seasonal plan.

## Frost-date honesty

Zone frost dates are long-term averages. The app says so on screen and invites you to enter
your local dates for exactness. For the most accurate dates for your town, check your local
cooperative extension.

## Files

- `index.html` — the whole app (single file, zero external requests)
- `gallery/` — screenshots for the listing

## Privacy

No analytics, no network requests, no cookies. The only link in the app is the discreet
"by Glenerds" attribution in the footer.

---

© Glenerds. Sold as a one-time purchase — yours forever, no subscription.
