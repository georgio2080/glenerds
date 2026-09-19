# MacroTrack — CHANGES.md

## 2026-09-19 — v1.0 (initial build)
- Built free TDEE & macro calculator as a single offline HTML file.
- Inputs: age, sex, height/weight (imperial + metric), optional body fat %,
  5 activity levels, goal presets (cut −20% / maintain / lean bulk +10%) with
  fine-tune slider (−30% to +20%), 3 BMR formulas, 3 macro split presets.
- Outputs: BMR, TDEE, target calories, protein/carbs/fat grams, weekly pace
  estimate, full show-your-work math steps, printable results.
- Dark mode: toggle, honors prefers-color-scheme, persisted in localStorage.
- Inputs persist in localStorage; stored state strictly validated on load.
- Discreet "by Glenerds" attribution link to the Gumroad store.
- QA: zero console/page errors in system Chromium (light + dark + mobile);
  all computed values verified against hand calculations (Mifflin-St Jeor,
  Harris-Benedict female, Katch-McArdle, metric/imperial, validation errors).
- Outside-AI review round 1: 4 minor findings — 2 verified non-issues
  (init overwrites inputs from defaults; canonical metric storage already in
  place), 2 fixed: localStorage state validation hardening, aria-live scoped
  to the big-numbers output only.
- Outside-AI review round 2: ZERO ISSUES.
- Gallery: 8 real screenshots (cover, inputs, results, show-your-work,
  dark mode, mobile, metric, Katch-McArdle).
