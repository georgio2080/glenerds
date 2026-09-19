# Compound-Interest Calculator — Change Log

## 2026-09-19 — Review-fix pass (3-AI bench adjudication)

Backup: `index.html.bak-20260919-122416` (pre-fix, same directory).
Adjudication: `~/workspace/compound-interest-calculator-review/ADJUDICATION.md`.

### Fixed (genuine defects)
1. **JS input clamping** (`readOpts`): `ret`, `inc`, `fee`, `tax`, `infl` now clamped
   `≥ 0` in JavaScript. Previously only HTML `min` attributes guarded them, so typed
   negative values (e.g. −5% inflation) were silently ignored by `defl()`.
2. **Milestone label** (`milestones`): month 12 now reads "year 1, month 12"
   (was "year 0, month 12"); month 1 reads "year 1, month 1". Via `y=ceil(mo/12)`.
3. **Reverse solver vs today's-dollars** (`renderReverse`): with "show in today's
   dollars" on, the solver now targets `target×(1+infl)^years` and labels the
   answer "(in today's dollars)". Lump-sum figure unchanged (money today is
   already today's dollars). Static note extended to document this.
4. **Scenario vs real-dollar display** (`renderScenarios`, scenario save): each
   scenario now stores `{years, real, infl}`; values render inflation-adjusted
   when saved in real mode; "best" highlight compares displayed values; footnote
   added when any scenario is real-mode. Old scenarios (no fields) render nominal.
5. **Tab keyboard semantics**: roving tabindex, ArrowLeft/Right/Up/Down + Home/End
   per APG, `aria-controls` on tabs, `role="tabpanel"` + `aria-labelledby` on the
   two advanced sections.
6. **Live regions**: `aria-live="polite" aria-atomic="true"` on `#ci-final`,
   `aria-live="polite"` on `#ci-milestones`.
7. **JSON round-trip** (export/import/localStorage): now carries
   `ui:{adv, revToggle, revTarget, revYears, wdToggle, wdAmt, scenarios}`.
   Import replaces in-memory scenarios with the file's (no silent mixing);
   old bare-opts files still import. Page reload now also restores scenarios
   and toggle states.
8. **Attribution** (standing rule): "Free tool by Glenerds" now links to
   `https://glenerds.gumroad.com` (was `../../index.html`).
9. **Reverse lump-sum vs initial balance** (`lumpFor`): the lump figure now
   subtracts the future value of the current initial balance + one-time
   deposits before discounting (previously it always priced from $0, so with
   the default $10,000 initial it overstated by exactly the grown initial —
   showed $136,237 instead of $126,237 — while the monthly figure next to it
   correctly accounted for the initial). Floored at 0. Spec values unchanged
   (no-initial case: $136,236.52 nominal, $285,249.01 real).

### Verified unchanged (correct per spec — not "fixed")
- Nominal-APR model `r_m=(1+r_eff/p)^(p/12)−1`, `r_eff=max(0,ret−fee−tax)`;
  month-end contributions; deposits at start of year; withdrawals at start of month;
  60-iteration bisection. All 16 Node math checks pass (see QA notes).
- Withdrawal ordering, real-dollar milestone thresholds, reverse-solver bisection
  bounds: intentional, confirmed.

### QA (2026-09-19)
- Node: 16/16 pure-function checks pass (headline $854,537.02; 0% $190,000;
  annual/quarterly/daily; drag floor; yr-5 deposit $79,494.07; reverse
  $1,051.50/mo & $136,236.52 lump; worked-example copy numbers verified).
- Static: zero external network URLs; JSON-LD valid; `node --check` clean.
- Gemini API re-review of the full fixed file: zero genuine new issues
  (4 suggestions adjudicated and rejected with rationale in ADJUDICATION.md).
- Round 2 (lumpFor fix): Playwright headless 64/64 pass (desktop 1440×900 +
  mobile 390×844, system Chromium); Gemini re-review of the changed function:
  zero genuine new issues (ADJUDICATION.md I10).
- Playwright headless (desktop 1440×900 + mobile 390×844): see QA script
  `/tmp/ciqa/qa.py` — console errors, network, interactions, JSON round-trip,
  dark-mode persistence, keyboard, links, screenshots.

## 2026-09-19 13:05 UTC — ChatGPT + Claude full-file review round (adjudicated)
Backup: index.html.bak-20260919-130500
- #10 One-time deposit dated beyond the time horizon is now omitted from the projection (was silently clamped into the final year); the entered year is preserved so extending the horizon later picks it up. UI note updated to say out-of-horizon deposits are ignored. (Both AIs flagged; genuine.)
- #11 addDepRow() rebuilt with DOM APIs + .value assignment instead of innerHTML string concat — closes stored-XSS path via malicious imported JSON deposit values. (Both AIs flagged; genuine.)
- #12 Added aria-live="polite" aria-atomic="true" to #ci-rev-out and #ci-wd-out so screen readers announce reverse-solver/withdrawal updates. (ChatGPT; genuine.)
- #13 "Best final value is highlighted" → "Highest final value is highlighted" (terminology accuracy).
- #14 Withdrawal note now states the 60-year projection limit.
- #15 scope="col" added to generated table headers (year-by-year + scenarios).
Rejected after verification: esc()/scenario-name XSS (false alarm from transcription error in review brief — actual /[&<>"]/g regex correct, retracted by ChatGPT, confirmed by Claude); tabKey() "dead code" (false — listeners attached at lines 549-550); Home/End tab mapping (already correct on disk — Home→Simple; the review brief carried a transcription error); year-end deflation of annual table components (reasonable documented approximation); unbounded monetary inputs / inconsistent clamping / solver failure state (graceful degradation via money()→"—", accepted behavior).

## 2026-09-19 13:20 UTC — Glen's live bug report (screenshot: $347,328,336,210,122,240,000)
Backup: index.html.bak-20260919-132000
Root cause: one-time deposit rows (and all other Advanced inputs) live inside the hidden Advanced panels, but readOpts()/readDeposits() applied them in Simple mode too. A huge deposit row Glen had set earlier was invisible in Simple mode yet inflated the result to $3.47e20 — reproduced exactly by planting the same hidden deposit.
- #16 Simple mode now uses only the four visible inputs (monthly compounding, no increase/fees/tax, nominal dollars, no deposits). Advanced values are preserved and re-apply when switching back; localStorage/JSON export still save the full state.
- #17 New note in Simple mode when advanced extras are set but not applied: "Simple mode uses just your four numbers above. Advanced extras currently set (...) apply in Advanced mode only."
- #18 "You put in" now includes the initial investment (was contributions-only: showed $72,000 for $180k initial + $72k monthly). put-in + growth = final invariant restored. Chart's contribution curve now starts at the initial investment to match.
Verified: Node math spec all pass; Playwright 11/11 behaviors (simple ignores hidden deposit, note shows/hides, deposit preserved across mode switches, advanced value stable $934,031 = 854,537 + 79,494).
