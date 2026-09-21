# GradePlan — Free Final Grade Calculator & GPA Calculator

## What it is
A free, fully offline single-file web app with three tools:

1. **Final Exam Solver** — "What do I need on the final?" Enter current grade, desired grade, and
   final weight. Returns the exact required score, an honest "not possible" verdict with your real
   ceiling (score with a perfect 100% on the final), or an "already guaranteed" verdict with your floor.
2. **Weighted Course Grade** — grading categories with weights and scores. Auto-scales when weights
   don't total 100%.
3. **GPA Calculator** — courses with credits and letter grades on a 4.0 scale, with a weighted toggle
   (+1.0 for Honors/AP courses).

Every result shows the formula with your numbers substituted (show-your-work).

## How to use
Double-click `index.html` — it opens in any browser. No install, no internet, no account.
Works from `file://`. Your inputs are saved privately in your browser (localStorage).

## Key formulas
- Required final score: `required = (desired − (1 − w) × current) ÷ w`
- Course grade: `Σ(weight × score) ÷ Σ(weight)`
- GPA: `Σ(grade points × credits) ÷ Σ(credits)`
- Grade points: A+/A 4.0, A− 3.7, B+ 3.3, B 3.0, B− 2.7, C+ 2.3, C 2.0, C− 1.7, D+ 1.3, D 1.0, D− 0.7, F 0.0

## Privacy
Zero external requests. No trackers, no analytics. Data never leaves the device.

## Files
- `index.html` — the app (single file)
- `gallery/` — 8 screenshot walkthrough images
- `GUMROAD-LISTING.md` — SEO-first Gumroad draft copy ($0, unpublished)
- `CHANGES.md` — changelog
- `gradeplan-bundle.zip` — everything zipped for the Gumroad product file
