# Home Inventory for Insurance Claims — Room-by-Room Belongings Tracker

If fire, flood, or theft hit tomorrow, could you list everything you own for
your insurance claim — with purchase values, serial numbers, and photos? Most
people can't, and that gap costs them thousands at claim time. HomeInventory
fixes it: catalog your belongings room by room, then print a claim-ready
insurance report in minutes.

An offline, single-file web app. No account, no subscription, no internet
needed — open `index.html` in any browser (even from `file://`) and it just
works. Your data never leaves this device.

## What it does

- **Rooms** — add, rename, and delete rooms. Each room shows its item count and
  total documented value. Rooms with items can't be deleted until emptied.
- **Item catalog** — name, category, purchase value, serial number, purchase
  date, receipt/note, and a photo (stored on this device, automatically
  downscaled to keep storage small).
- **Per-room and grand totals** — every total is computed live and shown in
  dollars, so you always know your total documented value.
- **Claim-ready report** — room-by-room table with item, category, serial #,
  purchase date, and value, plus a grand total. Print / Save as PDF prints
  only the report — hand it straight to your adjuster.
- **Search and room filter** — find items by name, serial, note, category, or
  room in seconds.
- **Dark mode** — visible toggle, follows your system preference on first load,
  remembered across visits.
- **Your data stays yours** — everything is saved in the browser's
  localStorage on your device. Export a JSON backup any time; import it to
  restore or move devices.

## Why it's different

- **100% offline** — works with no internet, from a single HTML file.
- **No account, no subscription** — one-time purchase, yours forever.
- **Private by design** — no analytics, no network requests, no cookies.

## Files

- `index.html` — the whole app (single file, zero external requests)
- `gallery/` — screenshots for the listing

## Privacy

No analytics, no network requests, no cookies. The only link in the app is the
discreet "by Glenerds" attribution in the footer.

## By Glenerds

Made by [Glenerds](https://glenerds.github.io/glenerds/) — practical offline
tools that respect your privacy. Related tools: [RenoTrack](https://glenerds.github.io/glenerds/)
(home renovation budget tracker) and the [Rent Receipt Generator](https://glenerds.github.io/glenerds/)
(printable landlord receipts).

---

© Glenerds. Sold as a one-time purchase — yours forever, no subscription.
