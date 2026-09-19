# Glenerds Design System — Integration Guide

For app builders. Three files live in `~/workspace/glenerds-microsite/assets/`:

| File | What it is |
|---|---|
| `glenerds-design-system.css` | The stylesheet. **Inline it** into each app's `<style>` block. |
| `glenerds-icons.svg` | The 30-icon `<symbol>` sprite. **Inline it** right after `<body>`. |
| `design-system-demo.html` | Visual demo of every component, both themes. Review target. |

Nothing is adopted into an app until the parent visually approves the demo.

## 1. Drop-in (5 lines)

In `<head>`, paste the entire CSS file inside your existing `<style>` block:

```html
<style>
/* ... your app's own styles ... */

/* ===== GLENERDS DESIGN SYSTEM v1.0 (pasted verbatim) ===== */
...entire glenerds-design-system.css...
</style>
```

Right after `<body ...>`, paste the entire sprite:

```html
<body class="g-app">
<svg ...>...entire glenerds-icons.svg...</svg>
<div class="g-wrap">
  ...
```

Then put the theme-init script **in `<head>`, after the style block** (runs before
paint, avoids a light/dark flash):

```html
<script>
(function(){var t=null;try{t=localStorage.getItem('glenerds-theme')}catch(e){}
if(t!=='dark'&&t!=='light'){t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}
document.documentElement.setAttribute('data-theme',t);})();
function gToggleTheme(){var h=document.documentElement;
var n=h.getAttribute('data-theme')==='dark'?'light':'dark';
h.setAttribute('data-theme',n);try{localStorage.setItem('glenerds-theme',n)}catch(e){}}
</script>
```

Body must carry `class="g-app"` and content should sit in `<div class="g-wrap">`.

## 2. Theme toggle button

```html
<button class="g-theme-toggle" onclick="gToggleTheme()" aria-label="Toggle dark mode">
  <svg class="g-icon g-icon-sm" aria-hidden="true"><use href="#g-i-moon"/></svg><span>Dark</span>
</button>
```

## 3. Component cheat-sheet

```html
<!-- Header -->
<header class="g-header">
  <div class="g-brand">
    <span class="g-appicon g-appicon-sm" style="--g-ai1:#fb7185;--g-ai2:#f59e0b">
      <svg class="g-icon" aria-hidden="true"><use href="#g-i-flame"/></svg>
    </span>
    <h1 class="g-brand-name">HabitTrack</h1>
  </div>
  <button class="g-theme-toggle" ...>…</button>
</header>
<p class="g-tagline">One-line pitch of what the app does.</p>

<!-- Tabs -->
<div class="g-tabs" role="tablist">
  <button class="g-tab" role="tab" aria-selected="true">…</button>
  <button class="g-tab" role="tab" aria-selected="false">…</button>
</div>

<!-- Card + form -->
<div class="g-card">
  <p class="g-title">Section title</p>
  <p class="g-desc">Muted description.</p>
  <div class="g-field">
    <label class="g-label" for="x">Label</label>
    <input class="g-input" id="x" type="number">
    <p class="g-hint">Hint text.</p>
    <p class="g-error" id="x-err">Error text (add .show to reveal, .is-invalid on input).</p>
  </div>
  <div class="g-btn-row">
    <button class="g-btn g-btn-primary">Calculate</button>
    <button class="g-btn g-btn-secondary">Reset</button>
  </div>
</div>

<!-- Result -->
<div class="g-result">
  <p class="g-big-number">94.67%</p>
  <p class="g-verdict g-verdict-good">On track</p>
  <p class="g-result-note">Explanation line.</p>
  <div class="g-math">show-your-work lines</div>
</div>

<!-- Stats / table / badges / empty / footer -->
<div class="g-stats">
  <div class="g-stat"><span class="g-stat-label">Label</span><span class="g-stat-value good">Value</span></div>
</div>
<table class="g-table">…</table>            <!-- wrap in .g-table-wrap -->
<span class="g-badge g-badge-accent">New</span>
<div class="g-empty">…icon + .g-title + text + button…</div>
<footer class="g-footer">Made by <a href="https://glenerds.gumroad.com">Glenerds</a> · free tools, no tracking, works offline</footer>
```

Class variants: buttons `g-btn-primary|secondary|danger|ghost`, `g-btn-sm`, `g-btn-block`;
verdicts `g-verdict-good|bad|warn`; badges `g-badge-accent|good|bad|warn|neutral` (+`g-badge-dot`);
grids `g-grid-2|g-grid-3`; type `g-display|g-title|g-body|g-caption|g-mono`.

## 4. Icons

Clean line variant (inherits text color):

```html
<svg class="g-icon" aria-hidden="true"><use href="#g-i-flame"/></svg>
```

Flash variant (brand indigo gradient stroke):

```html
<svg class="g-icon g-icon-flash" aria-hidden="true"><use href="#g-i-flame"/></svg>
```

Sizes: `g-icon-sm` (18px), default 24px, `g-icon-lg` (32px).

Available ids (`g-i-` prefix): `calc chart cal check flame star moon sun plus
trash download upload gear heart clock target trophy tag search edit share lock
sparkles home back x info wallet list bell` — 30 total, full gallery in the demo.

Icons inside buttons/tabs size automatically. Always `aria-hidden="true"` on
decorative icons.

## 5. App icons

Each app gets a distinctive gradient tile + one white glyph. Pick two gradient
stops that fit the app (reuse the sprite's `g-grad-*` stops or choose your own):

```html
<span class="g-appicon" style="--g-ai1:#fb7185;--g-ai2:#f59e0b">
  <svg class="g-icon" aria-hidden="true"><use href="#g-i-flame"/></svg>
</span>
```

`g-appicon-sm` for the header (44px). Full size (60px) for cover images.
Claimed so far: HabitTrack = flame/sunset, GradePlan = calc/royal,
MacroTrack = chart/ocean — new apps pick an unused glyph + gradient.

## 6. Rules

- **Zero external requests.** No webfonts, no CDNs, no images. The select chevron
  and checkbox check are inline `data:` URIs (not network).
- **Never restyle `g-` classes per-app.** If a component is missing, propose it
  for the design system instead of forking a one-off.
- **Dark mode is mandatory** and must look designed: use the tokens, never hardcode
  colors, test both themes + 360px width before signoff.
- **Accessibility:** keep `aria-selected` on tabs, `aria-hidden` on decorative
  icons, visible labels on all inputs, and don't remove focus styles.
- `prefers-reduced-motion` is already handled in the CSS.
