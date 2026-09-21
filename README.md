# TripBudget — Trip Budget Planner

A fully **offline, single-file** web app for planning a trip budget before you go and tracking expenses while you're there. No account, no subscription, no internet needed — open `index.html` in any browser (works from `file://`) and your data stays on your device.

## Features

- **Multiple trips** — create, rename, delete. Each trip has a destination, start/end dates, a home currency, a trip currency, and your own exchange rate (offline — no live rates; you enter it from your bank or a receipt).
- **Pre-trip budget allocation** — total trip budget plus per-category targets across 8 categories: Flights, Lodging, Food & Drink, Local Transport, Activities & Tours, Shopping, Travel Insurance, Other. Per-day allowance is computed automatically from your trip dates.
- **Savings target** — enter a departure date and a target amount; TripBudget tells you exactly how much to save per month and per week to hit it.
- **In-trip expense log** — date, category, amount in trip currency (auto-converted to home currency at your rate), optional note. Running totals vs. budget per category with progress bars and over-budget warnings.
- **Daily view** — spending per day against your daily allowance, with per-day category breakdowns.
- **Dashboard** — total budget, spent, remaining, % used, days until departure / days remaining, daily allowance.
- **Dark mode** — toggle button, follows your OS preference on first load, remembered afterwards.
- **Export / Import** — full backup as a JSON file; restore on any device.
- **Print** — a "Print trip summary" button produces a clean, printer-friendly budget sheet.
- **Exact money math** — all home-currency amounts are stored as integer cents, so totals are never off by a penny. Conversions round to the nearest cent (e.g. a €85 dinner at a 1.08 rate = $91.80).

## Use

Open `index.html` in Chrome, Edge, Firefox, or Safari — desktop or mobile. Everything runs locally; there are zero network requests.

Typical flow:

1. **+ New trip** — destination, dates, home/trip currency, your exchange rate, total budget.
2. **Planner tab** — split the budget across categories; set a savings target and departure date.
3. **Expenses tab** — log spending in the local currency as you go; watch each category's bar.
4. **Daily view tab** — check each day against your daily allowance.
5. **Dashboard** — the at-a-glance totals. Export JSON before you fly as a backup.

## Files

- `index.html` — the entire app (HTML + CSS + JS, no dependencies)
- `README.md` — this file
- `gumroad-listing.md` — product listing copy
- `gallery/` — screenshots

## Privacy

No analytics, no CDNs, no webfonts, no cookies, no servers. Data lives in your browser's `localStorage` under the key `tripbudget-v1`. Export JSON any time for a portable backup.

## QA

Automated Playwright/Chromium suite (`qa-tripbudget.py`, 40 checks): trip CRUD, allocation math, savings computation, expense logging in trip currency with conversion, export/import round-trip, theme persistence, 360px mobile layout, zero console/page errors, zero external network requests. Plus two rounds of Gemini API code review (logic, security/XSS, edge cases) with all valid findings fixed.

---

by [Glenerds](https://glenerds.gumroad.com)
