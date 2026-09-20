# RecipeCost — Recipe Cost Calculator for Home Bakers

An offline, single-file web app that tells home bakers and cottage-food sellers exactly what
each recipe costs and what to charge for it. No account, no subscription, no internet needed —
open `index.html` in any browser (even from `file://`) and it just works.

## What it does

- **Ingredient library** — store every ingredient with its package size, package price, and unit
  (g, kg, oz, lb, ml, l, tsp, tbsp, cup, each). The app computes the true cost per gram / ml / piece.
- **Smart unit conversion** — use flour by the cup in a recipe even though you buy it by the
  kilogram. Optional grams-per-cup handles cup↔gram; optional grams-per-piece handles count
  items used by weight (e.g. eggs).
- **Full recipe costing** — ingredients + your labor hours × hourly rate + packaging per piece +
  overhead % = true batch cost.
- **Pricing for profit** — set a target profit margin and get a suggested selling price per
  piece, profit per piece, profit per batch, and food-cost %.
- **Multiple recipes** — build, switch between, and delete as many recipes as you like.
- **Dark mode** — visible toggle, follows your system preference on first load, remembered.
- **Your data stays yours** — everything is saved in the browser's localStorage on your device.
  Export a JSON backup any time; import it on another device.
- **Print / PDF** — a clean print stylesheet gives you a one-page cost sheet per recipe.

## Files

- `index.html` — the whole app (single file, zero external requests)
- `gallery/` — screenshots for the listing

## Privacy

No analytics, no network requests, no cookies. The only link in the app is the discreet
"by Glenerds" attribution in the footer.

---

© Glenerds. Sold as a one-time purchase — yours forever, no subscription.
