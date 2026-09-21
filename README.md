# RenoTrack — Home Renovation Budget Tracker

A single-file, fully offline web app for tracking home renovation budgets:
per-category budgets vs. actuals, an expense log, contractor quote comparison
(up to 4 bids per job), a change-order log, and a contingency guard that warns
you before surprise costs eat your buffer.

## Run it

No install, no server, no internet needed.

1. Download or copy `index.html` anywhere (desktop, phone, USB stick).
2. Double-click it — it opens in any modern browser from `file://`.
3. Your data is saved automatically in the browser's localStorage on that
   device. Nothing is ever sent anywhere.

## Features

- **Multiple projects** — create, rename, delete (e.g. "Kitchen remodel", "Bath flip").
- **13 preset budget categories** (Demolition, Structural, Plumbing, Electrical,
  Kitchen, Bathrooms, Flooring, Paint & Drywall, Fixtures & Finishes, Appliances,
  Permits & Fees, Labor, Contingency) — rename them, add your own, delete ones
  you don't need. Edit any budget inline; totals update instantly.
- **Expense log** — date, category, vendor/payee, amount, note. Per-category
  progress bars with over-budget highlighting.
- **Contractor quotes** — up to 4 bids per job with side-by-side comparison,
  price range, and one-click "accepted" marking. Accepted bids count as
  committed spend on the dashboard.
- **Change-order log** — description, cost impact (+/-), category, and
  proposed / approved / rejected status. Approved change orders roll into that
  category's actuals automatically.
- **Contingency guard** — set contingency as a % of your base budget. The
  dashboard shows contingency remaining and warns you when approved change
  orders eat into it (amber at 75% used, red when exceeded).
- **Dashboard** — total budget, actual spent, committed, remaining, % used,
  per-category bars, recent expenses.
- **Exact money math** — all amounts are stored and computed as integer cents;
  no floating-point rounding drift.
- **Export / Import** — one-click JSON backup download and restore (validated
  and sanitized on import).
- **Dark mode** — toggle in the header; honors your OS preference on first
  load; remembered afterwards.
- **Print stylesheet** — `Ctrl/Cmd+P` prints a clean budget summary.
- **Mobile friendly** — usable at 360px wide; works on-site with no signal.

## Data & privacy

- Storage key: `renotrack-v1` in localStorage. Use Export regularly for backups.
- 100% offline: zero external requests (no CDNs, fonts, analytics, or images).
  Verified with network blocking in automated QA.

## QA

`qa/test_qa.py` — 29 Playwright checks (Chromium): project CRUD, budgets,
expenses, quotes (4-bid cap, accept toggle), change orders, hand-verified
dashboard math, export/import round-trip, invalid-import rejection, theme
persistence, mobile 360px overflow on all four tabs, zero console errors with
all network traffic blocked. Plus `toCents`/currency edge cases and a
malicious-import sanitization probe. Two rounds of Gemini code review;
all findings fixed.

---
by [Glenerds](https://glenerds.gumroad.com)
