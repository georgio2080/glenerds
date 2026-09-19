# QuoteCraft — Local Service Quote & Proposal Builder

Stop quoting jobs on scraps of paper or in a spreadsheet you'll never open again.
QuoteCraft builds clean, professional service quotes in seconds: add line items
with quantities and prices, apply a discount, add tax, and hand the customer a
printed quote with your business name on it.

## What's inside
- `index.html` — the complete app. Single file, works offline.
  Open it in any modern browser (double-click, or File → Open). No install,
  no account, no internet needed.
- `gallery/` — 9 images (cover + 8 screenshots showing the app in action).

## Features
- Quotes list with auto-incrementing numbers (Q-0001, Q-0002…) that never reuse
  a number — delete Q-0002 and the next quote is still Q-0003
- Full quote editor: customer info, quote date, valid-until, status
  (Draft / Sent / Accepted / Declined)
- Line items with description, quantity, unit price, and per-item taxable flag
- Discounts: none, percentage, or flat amount
- Tax applied to taxable lines AFTER the discount, pro-rated across
  taxable/non-taxable lines (explained in the app's totals footnote)
- Integer-cent math throughout — totals match to the penny every time
- Live totals panel with screen-reader announcements
- Clean printable customer quote: your business header, line items, totals,
  and signature lines — the Glenerds footer is hidden from the printed page
- Business profile (name, tagline, phone, email) printed on every quote
- JSON backup export/import with full sanitization of imported data
- One-click demo data and confirm-gated clear-all
- Dark mode (follows your system, remembers your choice)
- Everything stays in your browser — your data never leaves your device

## Support
Questions or issues: reply to your Gumroad receipt email.
