# HenTrack — Backyard Chicken Flock & Egg Tracker

Daily egg counts, feed costs, flock records & egg sales for backyard chicken keepers. 100% offline single-file web app.

## Features
- **Dashboard** — laying-hen count, 30-day egg totals, lay rate %, cost per dozen (trailing 30 days), spend/revenue stats, 14-day egg bar chart
- **Egg Log** — one entry per day (re-logging updates), damaged-egg count, notes (double yolks, first eggs…)
- **Flock** — hen names, breeds, hatch dates, status (laying / pullet / molting / broody / retired / lost); lay rate only counts laying hens
- **Feed & Costs** — categorized expenses (feed, bedding, supplements, vet, equipment, chicks), monthly/all-time totals
- **Egg Sales** — dozens sold + price per dozen, revenue totals, all-time profit vs spend
- Dark mode (toggle, system preference on first load, persisted), localStorage persistence, JSON export/import, print summary, mobile responsive, zero external requests

## Files
- `index.html` — the app (open directly, works from `file://`)
- `gallery/` — screenshots (light/dark/mobile)
- `gumroad-listing.md` — SEO-first listing draft
- `hentrack-1.0.0.zip` — distributable bundle

## QA
Playwright/Chromium checks + Gemini API code review (2 rounds), zero console errors.
