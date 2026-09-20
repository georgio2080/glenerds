#!/usr/bin/env python3
"""Builds the Glenerds SEO microsite as static HTML. Run: python3 build.py"""
import os, html, re

ROOT = os.path.dirname(os.path.abspath(__file__))
# Canonical deploy URL (GitHub Pages). Used for sitemap, canonical tags, and OG URLs.
SITE_URL = "https://glenerds.github.io/glenerds"
STORE_URL = "https://glenerds.gumroad.com"

# Dark-mode theme pattern (shared by every generated page, matching the hand-written
# tool pages): THEME_PRE runs before the stylesheet to avoid a theme flash;
# THEME_JS wires the visible toggle. Preference persists in localStorage;
# honors prefers-color-scheme on first load.
THEME_PRE = """<script>
(function(){try{var t=localStorage.getItem('glenerds-theme');if(t){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();
</script>"""
THEME_JS = """<script>
(function(){
  var KEY='glenerds-theme',root=document.documentElement,btn=document.getElementById('theme-toggle');
  function sysDark(){return window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;}
  function cur(){try{var s=localStorage.getItem(KEY);if(s==='dark'||s==='light')return s;}catch(e){}return sysDark()?'dark':'light';}
  function paint(){var t=cur();root.setAttribute('data-theme',t);
    if(btn){btn.textContent=(t==='dark'?'\\u2600 Light':'\\u25D0 Dark');btn.setAttribute('aria-pressed',t==='dark'?'true':'false');}}
  if(btn){btn.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';try{localStorage.setItem(KEY,n);}catch(e){}paint();});}
  paint();
})();
</script>"""

CSS = """:root{
  --bg:#ffffff; --fg:#1a1a1a; --muted:#5b5b5b; --card:#f6f6f6;
  --border:#e2e2e2; --accent:#0f6c3f; --accent-fg:#ffffff; --code:#efefef;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#141414; --fg:#eaeaea; --muted:#a8a8a8; --card:#1e1e1e;
    --border:#333333; --accent:#3fae6d; --accent-fg:#0c0c0c; --code:#262626;
  }
}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--fg);line-height:1.65}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem}
header.site{border-bottom:1px solid var(--border);padding:.9rem 0;margin-bottom:2rem}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem}
.brand{font-weight:800;font-size:1.35rem;text-decoration:none;color:var(--fg)}
nav.main a{margin-left:1.1rem;text-decoration:none;color:var(--muted);font-weight:600}
nav.main a:hover{color:var(--fg)}
.hero{padding:2.5rem 0 1.5rem}
.hero h1{font-size:2.1rem;line-height:1.25;margin:.2rem 0 1rem}
.hero p.lead{font-size:1.1rem;color:var(--muted);max-width:46rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.25rem;margin:1.5rem 0 2.5rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;
  padding:1.25rem;display:flex;flex-direction:column}
.card h3{margin:.1rem 0 .5rem;font-size:1.1rem}
.card p{color:var(--muted);font-size:.95rem;flex:1}
.card .price{font-weight:700;margin:.5rem 0}
.card a.btn,.btn{display:inline-block;background:var(--accent);color:var(--accent-fg);
  font-weight:700;text-decoration:none;padding:.65rem 1.15rem;border-radius:8px;margin-top:.6rem}
.btn.ghost{background:transparent;color:var(--accent);border:2px solid var(--accent)}
section.block{margin:2.5rem 0}
h2.sec{font-size:1.5rem;margin-bottom:.5rem;border-bottom:2px solid var(--border);padding-bottom:.4rem}
.breadcrumb{font-size:.85rem;color:var(--muted);margin:0 0 1rem}
.breadcrumb a{color:var(--muted)}
.pricebox{display:inline-block;background:var(--card);border:1px solid var(--border);
  border-radius:10px;padding:.6rem 1rem;font-weight:800;font-size:1.15rem;margin:.8rem .8rem .8rem 0}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;margin:1.25rem 0}
.shots img{width:100%;border:1px solid var(--border);border-radius:10px;display:block}
.shots figcaption{font-size:.85rem;color:var(--muted);margin-top:.35rem}
ul.feat{padding-left:1.25rem}
ul.feat li{margin:.45rem 0}
.faq dt{font-weight:700;margin:1rem 0 .25rem}
.faq dd{margin:0 0 .75rem;color:var(--muted)}
footer.site{border-top:1px solid var(--border);margin-top:3rem;padding:1.5rem 0 2.5rem;
  color:var(--muted);font-size:.9rem}
footer.site a{color:var(--muted)}
.toolbox{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin:1.5rem 0}
.toolbox input[type=text],.toolbox input[type=number],.toolbox input[type=date],
.toolbox select{padding:.5rem .6rem;border:1px solid var(--border);border-radius:6px;
  background:var(--bg);color:var(--fg);font-size:1rem;margin:.25rem .25rem .25rem 0}
.toolbox button{padding:.55rem 1rem;border:none;border-radius:6px;background:var(--accent);
  color:var(--accent-fg);font-weight:700;cursor:pointer;margin:.25rem .25rem .25rem 0}
.toolbox button.plain{background:transparent;color:var(--accent);border:2px solid var(--accent)}
.toolbox table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}
.toolbox th,.toolbox td{border:1px solid var(--border);padding:.45rem .6rem;text-align:left}
.toolbox th{background:var(--code)}
.habit-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.75rem;margin:1rem 0}
.habit{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:.75rem}
.habit .hname{font-weight:700;font-size:.95rem;margin-bottom:.5rem;word-break:break-word}
.dots{display:flex;flex-wrap:wrap;gap:.3rem}
.dot{width:26px;height:26px;border-radius:50%;border:2px solid var(--border);background:transparent;
  cursor:pointer;font-size:.7rem;color:var(--muted);padding:0}
.dot.on{background:var(--accent);border-color:var(--accent);color:var(--accent-fg)}
.prose{max-width:46rem}
.prose p{margin:.9rem 0}
.cta-band{background:var(--card);border:1px solid var(--border);border-radius:12px;
  padding:1.75rem;margin:2.5rem 0;text-align:center}
.cta-band h2{margin-top:0}
.small{font-size:.85rem;color:var(--muted)}
@media (max-width:640px){.hero h1{font-size:1.6rem}nav.main a{margin-left:.7rem}}
"""

def esc(s):
    return html.escape(s, quote=True)

def head(title, desc, path, og_image=None, extra=""):
    canon = SITE_URL + path
    tags = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canon)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Glenerds">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canon)}">"""
    if og_image:
        tags += f'\n<meta property="og:image" content="{esc(SITE_URL + og_image)}">'
    depth = len([s for s in path.strip("/").split("/") if s])
    css_path = "../" * depth + "style.css" if depth else "style.css"
    tags += f"\n{THEME_PRE}\n" + f'<link rel="stylesheet" href="{css_path}">'
    return "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" + tags + extra + "\n</head>"

import json as _json
def json_ld(p):
    price_num = re.sub(r"[^0-9.]", "", p["price"].split()[0])
    data = {
        "@context": "https://schema.org",
        "@type": ["Product", "SoftwareApplication"],
        "name": p["name"],
        "description": p["meta"],
        "url": SITE_URL + "/products/" + p["slug"] + "/",
        "brand": {"@type": "Brand", "name": "Glenerds"},
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any modern web browser",
        "offers": {
            "@type": "Offer",
            "price": price_num,
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": p["url"],
        },
    }
    return '<script type="application/ld+json">\n' + _json.dumps(data, indent=2) + '\n</script>'

def faq_ld(faqs):
    qs = []
    for q, a in faqs:
        qs.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qs}
    return '<script type="application/ld+json">\n' + _json.dumps(data, indent=2) + '\n</script>'

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", html.unescape(re.sub(r"\s+", " ", s))).strip()

def faq_ld_from_html(page_html):
    """Build an FAQPage JSON-LD block from the first <dl class="faq"> in rendered HTML."""
    m = re.search(r'<dl class="faq">(.*?)</dl>', page_html, re.S)
    if not m:
        return ""
    pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", m.group(1), re.S)
    return faq_ld([(strip_tags(q), strip_tags(a)) for q, a in pairs])

def site_header(depth):
    home = "../" * depth if depth else "./"
    return f"""<body>
<header class="site"><div class="wrap">
<a class="brand" href="{home}index.html">Glenerds</a>
<nav class="main">
<a href="{home}index.html">Home</a>
<a href="{home}index.html#free-tools">Free Tools</a>
<a href="{home}index.html#products">Products</a>
<a href="{STORE_URL}">Store</a>
<button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">◐ Dark</button>
</nav></div></header>
<div class="wrap">"""

def site_footer(depth):
    home = "../" * depth if depth else "./"
    return f"""</div>
<footer class="site"><div class="wrap">
<p><strong>Glenerds</strong> makes single-purpose offline micro-tools: habit trackers, savings planners,
inspection checklists, and calculators that run in your browser with no account and no subscription.</p>
<p>More offline micro-tools from Glenerds: <a href="{STORE_URL}">{STORE_URL}</a></p>
<p class="small"><a href="{home}site-map/index.html">Site map</a> &mdash; every free tool, paid product, and guide on this site.</p>
<p class="small">&copy; 2026 Glenerds. All tools on this site run locally in your browser; nothing you enter is sent anywhere.</p>
</div></footer>
{THEME_JS}
</body>
</html>"""

def crumb(depth, items):
    home = "../" * depth if depth else "./"
    parts = [f'<a href="{home}index.html">Home</a>']
    parts += items
    return '<p class="breadcrumb">' + " &rsaquo; ".join(parts) + "</p>"

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path, len(content), "chars")

# ---------------- HOMEPAGE ----------------
def build_home():
    tool_cards = [
        ("tools/habit-tracker/", "Free Offline Habit Tracker",
         "Build daily streaks with a simple printable-style tracker that saves to your browser. No account, no app install."),
        ("tools/savings-challenge/", "Free 52-Week Savings Challenge Calculator",
         "See exactly how much a 52-week money challenge adds up to, customize the weekly amount, and track your progress week by week."),
        ("tools/net-worth-tracker/", "Free Net Worth Tracker",
         "List what you own and what you owe, watch your net worth change over time, all stored privately on your device."),
        ("tools/compound-interest-calculator/", "Free Compound Interest Calculator",
         "Model investing growth with inflation, fees, and tax adjustments \u2014 simple or advanced mode."),
    ]
    product_cards = [
        ("products/online-fitness-coach-check-in-tracker/", "Online Fitness Coach Check-In Tracker",
         "Log client check-ins, compare weeks side by side, and draft feedback in one click.", "$29 one-time"),
        ("products/cremacheck/", "Used Commercial Espresso Machine Inspection Checklist",
         "Brand-specific checklists with a risk score and repair-cost estimate before you buy used.", "$29 one-time"),
        ("products/moving-company-quote-comparison-scam-checker/", "Moving Company Scam Checker",
         "Score movers on 35 red-flag signals and compare up to 4 quotes side by side.", "$9 one-time"),
        ("products/flipbid-reconciler/", "Contractor Bid Comparison Tool for House Flippers",
         "Normalize up to 3 bids into one scope matrix and flag price gaps and scope holes.", "$29 one-time"),
        ("products/hoa-resale-package-reserve-study-risk-analyzer/", "HOA Financial Health & Reserve Study Analyzer",
         "Score HOA finances from resale-package figures and flag special-assessment risk.", "$9 one-time"),
        ("products/hullcheck/", "Used Boat Pre-Purchase Inspection Checklist",
         "Boat-type-specific checklists with weighted risk scoring and repair estimates.", "$29 one-time"),
        ("products/depositdocket/", "Security Deposit Deduction Statement Generator",
         "Itemize deposit deductions and print professional tenant statements for small landlords.", "$14 one-time"),
        ("products/pitprofit/", "Competition BBQ Expense & Payout Tracker",
         "Log every contest and see your true season P&amp;L, best and worst contests.", "$29 one-time"),
        ("products/handmade-pricing-calculator-etsy-craft-sellers/", "Handmade Pricing Calculator for Etsy &amp; Craft Sellers",
         "Turn supplies, labor, and fees into suggested prices for every sales channel.", "$14 one-time"),
        ("products/css-element-inspector-chrome/", "CSS Element Inspector for Chrome",
         "Hover any element to inspect it, click to lock, copy CSS, selectors, and Tailwind classes.", "$9 one-time"),
    ]
    body = site_header(0) + """
<main>
<div class="hero">
<h1>Free Offline Micro-Tools &amp; Calculators</h1>
<p class="lead">Glenerds builds tiny, single-purpose tools that run entirely in your browser.
No accounts, no subscriptions, no uploads &mdash; your data never leaves your device.
Start with a free tool below, or browse the paid toolkits when you need the full power version.</p>
</div>

<section class="block" id="free-tools">
<h2 class="sec">Free Tools &mdash; Use Them Right Now</h2>
<div class="grid">
"""
    for slug, name, pitch in tool_cards:
        body += f"""<div class="card"><h3>{name}</h3><p>{pitch}</p>
<a class="btn" href="{slug}index.html">Open the free tool</a></div>
"""
    body += """</div>
<p class="small">More free tools: <a href="tools/moving-cost-calculator/index.html">moving cost calculator</a>
&middot; <a href="tools/craft-pricing-calculator/index.html">craft pricing calculator</a>
&middot; <a href="tools/contractor-bid-comparison/index.html">contractor bid comparison worksheet</a>
&middot; <a href="tools/security-deposit-deduction-calculator/index.html">deposit deduction calculator</a>
&middot; <a href="tools/hoa-special-assessment-calculator/index.html">HOA assessment calculator</a>
&middot; <a href="tools/css-specificity-calculator/index.html">CSS specificity calculator</a>
&middot; <a href="tools/index.html">all 14 free tools</a></p>
</section>

<section class="block prose">
<h2 class="sec">Why offline tools?</h2>
<p>Most web apps make you create an account before you can do anything, then charge you every month
for the privilege. Every Glenerds tool takes the opposite approach: it is a single file that runs
in any modern browser, works with no internet connection, and stores everything in your browser's
local storage. There is nothing to sign up for, nothing to sync, and nothing that can leak your
financial or personal data &mdash; because the data never goes anywhere.</p>
<p>The free tools on this page are fully working, not demos. The habit tracker, the 52-week savings
challenge calculator, and the net worth tracker each do their job completely, for free, forever.
They are also a good preview of how Glenerds builds software: fast, private, and focused on exactly
one task. If you like the approach, the paid toolkits below apply the same philosophy to bigger
jobs &mdash; vetting a moving company, inspecting a used boat, comparing contractor bids, or pricing
handmade products &mdash; as a one-time purchase with no subscription attached.</p>
<p>New to the idea of offline-first software? Pick any free tool above and try it. Everything happens
on your device, so there is zero risk in experimenting: close the tab and nothing of yours was ever
uploaded anywhere.</p>
</section>

<section class="block" id="products">
<h2 class="sec">Paid Toolkits &mdash; One-Time Purchase, Yours Forever</h2>
<div class="grid">
"""
    for slug, name, pitch, price in product_cards:
        body += f"""<div class="card"><h3>{name}</h3><p>{pitch}</p>
<span class="price">{price}</span>
<a class="btn" href="{slug}index.html">Learn more</a></div>
"""
    body += """</div>
<p class="small">Comparison guides: <a href="alternatives/craftybase-alternative/index.html">Craftybase alternative for makers</a>
&middot; <a href="alternatives/moving-quote-websites-alternative/index.html">moving quote website alternative</a>
&middot; <a href="alternatives/servicetitan-alternative/index.html">ServiceTitan alternative for flippers</a>
&middot; <a href="alternatives/hoa-management-software-alternative/index.html">HOA software alternative for buyers</a>
&middot; <a href="alternatives/trainerize-truecoach-alternative/index.html">Trainerize / TrueCoach alternative</a></p>
<p class="small">Every paid toolkit is sold through Gumroad as a one-time purchase.
No subscription, no account required to use the tool itself &mdash; download it and it runs offline in your browser.</p>
</section>
</main>
"""
    page = head(
        "Free Offline Micro-Tools & Calculators | Glenerds",
        "Free offline micro-tools and calculators from Glenerds: habit tracker, 52-week savings challenge, net worth tracker, plus paid one-time toolkits. No account, no subscription.",
        "/") + body + site_footer(0)
    write("index.html", page)

HABIT_JS = """
<script>
(function(){
  var KEY='glenerds-habit-v1';
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||{habits:[]}}catch(e){return{habits:[]}}}
  function save(d){localStorage.setItem(KEY,JSON.stringify(d))}
  var data=load();
  function uid(){return 'h'+Date.now().toString(36)+Math.floor(Math.random()*999)}
  function todayStr(){var d=new Date();return d.toISOString().slice(0,10)}
  function last14(){var out=[],d=new Date();for(var i=13;i>=0;i--){var t=new Date(d);t.setDate(d.getDate()-i);out.push(t.toISOString().slice(0,10))}return out}
  function render(){
    var wrap=document.getElementById('habit-list');wrap.innerHTML='';
    var days=last14(),today=todayStr();
    if(!data.habits.length){wrap.innerHTML='<p class="small">No habits yet. Add your first one above.</p>'}
    data.habits.forEach(function(h){
      var div=document.createElement('div');div.className='habit';
      var head=document.createElement('div');head.className='hname';head.textContent=h.name;
      var del=document.createElement('button');del.className='plain';del.textContent='Delete';del.style.marginLeft='0.5rem';
      del.onclick=function(){data.habits=data.habits.filter(function(x){return x.id!==h.id});save(data);render()};
      head.appendChild(del);div.appendChild(head);
      var dots=document.createElement('div');dots.className='dots';
      days.forEach(function(day){
        var b=document.createElement('button');b.className='dot'+(h.days[day]?' on':'');
        b.title=day;b.textContent=new Date(day+'T12:00:00').getDate();
        b.setAttribute('aria-label',(h.days[day]?'Done ':'Not done ')+h.name+' on '+day);
        b.onclick=function(){h.days[day]=!h.days[day];save(data);render()};
        dots.appendChild(b);
      });
      div.appendChild(dots);
      var streak=0,d=new Date();
      while(true){var s=d.toISOString().slice(0,10);if(h.days[s]){streak++;d.setDate(d.getDate()-1)}else break}
      var meta=document.createElement('p');meta.className='small';
      meta.textContent='Current streak: '+streak+' day'+(streak===1?'':'s')+'  |  Total check-ins: '+Object.keys(h.days).filter(function(k){return h.days[k]}).length;
      div.appendChild(meta);wrap.appendChild(div);
    });
  }
  document.getElementById('habit-add').onclick=function(){
    var inp=document.getElementById('habit-name');var v=inp.value.trim();if(!v)return;
    data.habits.push({id:uid(),name:v,days:{}});inp.value='';save(data);render();
  };
  document.getElementById('habit-export').onclick=function(){
    var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='habit-tracker-backup.json';a.click();
  };
  render();
})();
</script>"""

def build_habit():
    body = site_header(2) + crumb(2, ["Free Tools", "Habit Tracker"]) + """
<main>
<div class="hero">
<h1>Free Offline Habit Tracker &mdash; Build Streaks Without an Account</h1>
<p class="lead">Need a habit tracker that works offline with no account? Add your habits, tap the dots each day,
and watch your streaks grow &mdash; every check-in stored in your browser, nothing uploaded anywhere.
No sign-up, no app install, no subscription. Open the page and start.</p>
</div>

<div class="toolbox" role="region" aria-label="Habit tracker">
<input type="text" id="habit-name" placeholder="New habit, e.g. Read 20 pages" aria-label="New habit name">
<button id="habit-add">Add habit</button>
<button id="habit-export" class="plain">Export backup</button>
<div class="habit-grid" id="habit-list"></div>
<p class="small">Tip: click a date circle to toggle it. Your habits are saved automatically in this browser.</p>
</div>
""" + HABIT_JS + """
<div class="toolbox">
<h3 style="margin-top:0">Free forever &mdash; no paid version</h3>
<p>This habit tracker is complete as-is: unlimited habits, streak counts, totals, and JSON export &mdash; free for personal use, forever.</p>
<p><strong>Coaching clients instead of yourself?</strong> <a href="../../products/online-fitness-coach-check-in-tracker/index.html"><strong>FitnessCheckIn &mdash; $29 one-time</strong></a> is the coaching version: a full client roster with weekly check-in histories, photo protocols, measurements, and one-click feedback drafts. No subscription. No account.</p>
</div>

<section class="block prose">
<h2 class="sec">How to use the habit tracker</h2>
<p>Add each habit you want to build &mdash; exercise, reading, meditation, saving money, anything with
a daily repetition. Each habit gets a row of the last 14 days. Click a date to mark it done; click
again to undo. Your current streak counts backward from today, so a missed day simply resets the
counter without erasing your history. Use the export button any time to download a JSON backup of
all your habits, which you can keep with your other files or move to another browser.</p>
<h2 class="sec">Why streaks work</h2>
<p>Habit research consistently finds that visible progress is one of the strongest motivators for
keeping a new behavior going. A streak turns an abstract goal ("exercise more") into a concrete
daily question ("did I keep the chain alive today?"). The tracker above is deliberately minimal:
no gamified coins, no social feed, no reminders begging for attention &mdash; just your habits and
your history. That simplicity is also why it works offline: there is no server to sync with, so
the whole tool is a single page that loads instantly and works on a plane, in a basement, or
anywhere else with no signal.</p>
<h2 class="sec">Worked example</h2>
<p>Add a habit called "Read 20 pages". Tap today's dot, then the 13 dots before it. The tracker reads
<strong>Current streak: 14 days</strong> with 14 total check-ins. Miss tomorrow and the streak resets to
zero &mdash; but your history stays, so those 14 days still count in your totals. That's the whole game:
the streak is the motivator, the history is the record.</p>
<h2 class="sec">Frequently asked questions</h2>
<dl class="faq">
<dt>Is this habit tracker really free?</dt>
<dd>Yes. Every feature on this page &mdash; unlimited habits, streak counts, totals, and JSON export
&mdash; is free and always will be. There is no premium tier and no account wall.</dd>
<dt>Where is my data stored?</dt>
<dd>In your browser's local storage, on your device only. Glenerds never sees it, and nothing is
uploaded anywhere. Clearing your browser data will erase your habits, so use the export button for
backups you care about.</dd>
<dt>Does it work on my phone?</dt>
<dd>Yes. The page is responsive and works in any modern mobile browser. Add it to your home screen
for app-like access; it still runs fully offline after the first load.</dd>
<dt>Can I track weekly instead of daily habits?</dt>
<dd>The tracker is built around daily check-ins, which is where streaks are most motivating. For a
weekly habit, many people check in on the day they do it and simply let the other days stay empty
&mdash; the total check-in count still tells the real story.</dd>
<dt>What if I want more than a habit tracker?</dt>
<dd>If you coach clients or run a fitness business, the free tracker above covers personal habits.
For managing other people's check-ins &mdash; weekly logs, photo protocols, measurements, and
client feedback drafts &mdash; take a look at the paid toolkit below.</dd>
</dl>
</section>

<section class="block">
<h2 class="sec">Related tools</h2>
<div class="grid">
<div class="card"><h3>Free Fitness Client Check-In Tracker</h3><p>Log one client's weekly check-ins &mdash; weight, measurements, adherence &mdash; and compare weeks.</p><a class="btn" href="../fitness-client-check-in/index.html">Open the free tool</a></div>
<div class="card"><h3>Free 52-Week Savings Challenge Calculator</h3><p>Build the saving habit with the weekly math done for you.</p><a class="btn" href="../savings-challenge/index.html">Open the free tool</a></div>
</div>
</section>

<div class="cta-band">
<h2>Coaching clients, not just yourself?</h2>
<p>FitnessCheckIn is the offline client check-in tracker for online coaches: log weekly check-ins,
compare weeks side by side, and generate client feedback in one click. One-time purchase, no subscription.</p>
<a class="btn" href="../../products/online-fitness-coach-check-in-tracker/index.html">See FitnessCheckIn &mdash; $29 one-time</a>
<p class="small">Prefer to browse everything? <a href="https://glenerds.gumroad.com">More offline micro-tools from Glenerds</a></p>
</div>
</main>
"""
    page = head("Free Offline Habit Tracker — Build Daily Streaks | Glenerds",
        "Free offline habit tracker that runs in your browser. Build streaks, track daily habits, export backups. No account, no subscription, your data stays on your device.",
        "/tools/habit-tracker/", extra=faq_ld_from_html(body)) + body + site_footer(2)
    write("tools/habit-tracker/index.html", page)

SAVE_JS = """
<script>
(function(){
  var KEY='glenerds-save52-v1';
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||{done:{},weekly:1,start:1}}catch(e){return{done:{},weekly:1,start:1}}}
  function save(d){localStorage.setItem(KEY,JSON.stringify(d))}
  var data=load();
  function render(){
    var w=parseFloat(document.getElementById('sv-weekly').value)||data.weekly;
    var s=parseFloat(document.getElementById('sv-start').value)||data.start;
    data.weekly=w;data.start=s;
    var total=0,rows='',doneCount=0;
    for(var i=1;i<=52;i++){
      var amt=s+(i-1)*w;total+=amt;
      var done=!!data.done[i];if(done)doneCount++;
      rows+='<tr><td>Week '+i+'</td><td>$'+amt.toFixed(2)+'</td><td>$'+total.toFixed(2)+'</td>'
        +'<td><input type="checkbox" data-w="'+i+'"'+(done?' checked':'')+' aria-label="Mark week '+i+' done"></td></tr>';
    }
    document.getElementById('sv-rows').innerHTML=rows;
    var saved=0;for(var j=1;j<=52;j++){if(data.done[j])saved+=s+(j-1)*w}
    document.getElementById('sv-total').textContent='Challenge total: $'+total.toFixed(2);
    document.getElementById('sv-progress').textContent='Saved so far: $'+saved.toFixed(2)+' ('+doneCount+'/52 weeks)';
    var boxes=document.querySelectorAll('#sv-rows input[type=checkbox]');
    boxes.forEach(function(b){b.onchange=function(){var wk=parseInt(b.getAttribute('data-w'),10);data.done[wk]=b.checked;save(data);render()}});
    save(data);
  }
  document.getElementById('sv-weekly').value=data.weekly;
  document.getElementById('sv-start').value=data.start;
  document.getElementById('sv-weekly').oninput=render;
  document.getElementById('sv-start').oninput=render;
  document.getElementById('sv-reset').onclick=function(){if(confirm('Reset all 52 weeks?')){data={done:{},weekly:parseFloat(document.getElementById('sv-weekly').value)||1,start:parseFloat(document.getElementById('sv-start').value)||1};save(data);render()}};
  render();
})();
</script>"""

def build_savings():
    body = site_header(2) + crumb(2, ["Free Tools", "52-Week Savings Challenge"]) + """
<main>
<div class="hero">
<h1>Free 52-Week Savings Challenge Calculator &amp; Tracker</h1>
<p class="lead">How much does the 52-week money challenge actually save? $1,378 with the classic $1-a-week rules
&mdash; and this free calculator works out any variation. Set your own starting amount and weekly increase,
check off each week as the money moves into savings, and watch the running total grow. Two strategies beat
the hard back half: run the challenge in reverse (big weeks first, while motivation is high) or split each
week into daily transfers. Offline, no account; your savings data never leaves your browser.</p>
</div>

<div class="toolbox" role="region" aria-label="52-week savings challenge calculator">
<label>Start week 1 at: $<input type="number" id="sv-start" min="0.5" step="0.5" style="width:5rem" aria-label="Starting amount"></label>
<label>Increase each week by: $<input type="number" id="sv-weekly" min="0.5" step="0.5" style="width:5rem" aria-label="Weekly increase"></label>
<button id="sv-reset" class="plain">Reset</button>
<p><strong id="sv-total"></strong><br><span id="sv-progress" class="small"></span></p>
<table><thead><tr><th>Week</th><th>Save</th><th>Running total</th><th>Done</th></tr></thead>
<tbody id="sv-rows"></tbody></table>
<p class="small">Check a week when the money is actually saved. Everything is stored in your browser only.</p>
</div>
""" + SAVE_JS + """
<div class="toolbox">
<h3 style="margin-top:0">Free forever &mdash; no paid version</h3>
<p>This savings challenge tracker is complete as-is: any start amount, any weekly increase, all 52 weeks with a running total &mdash; free forever.</p>
<p><strong>Sell handmade goods?</strong> <a href="../../products/handmade-pricing-calculator-etsy-craft-sellers/index.html"><strong>CraftCost &mdash; $14 one-time</strong></a> applies the same offline philosophy to the other half of the equation: turning supplies, labor, and fees into prices that actually leave a margin. No subscription. No account.</p>
</div>

<section class="block prose">
<h2 class="sec">How the 52-week savings challenge works</h2>
<p>The standard challenge starts by saving $1 in week one, $2 in week two, $3 in week three, and so
on, increasing by one dollar each week until week 52. Done straight through, that adds up to
<strong>$1,378</strong>. The calculator above starts with those classic settings, but the real power
is customization: set the starting amount and weekly increase to match your budget. Starting at $5
and increasing by $5 each week, for example, finishes at $6,890 &mdash; a serious emergency fund built
one painless increment at a time.</p>
<p>The hardest part of any savings challenge is the back half, when weekly amounts get large. Two
strategies help: run the challenge in reverse (start with week 52's big amount while motivation is
highest), or split the weekly amount into a daily transfer so it never feels like a lump sum. Use
the checkboxes above honestly &mdash; only check a week when the money has actually moved into savings
&mdash; and the "saved so far" counter keeps you accountable without any judgment.</p>
<h2 class="sec">Making the challenge fit a tight budget</h2>
<p>If the classic $1,378 version feels out of reach, shrink it. A $0.50 start with $0.50 weekly
increases totals $689 &mdash; still a meaningful cushion. The point is the habit of moving money
consistently, not the headline number. Many people run two challenges at once: a small one for
guilt-free spending money and a larger one for the emergency fund. Because this tracker lives in
your browser with no account, there is nothing stopping you from opening it in two tabs with
different settings.</p>
<h2 class="sec">Worked example</h2>
<p>Classic rules: start at $1, increase by $1 each week. Week 1 saves $1, week 52 saves $52, and the total
is the sum of 1 through 52 &mdash; <strong>$1,378</strong>, which the calculator shows the moment the page
loads. Change the start to $5 with $5 weekly increases and the total becomes <strong>$6,890</strong>; drop
to $0.50 and $0.50 and it's <strong>$689</strong>. The running-total column shows exactly where you stand at
any week, checked or not.</p>
<h2 class="sec">Frequently asked questions</h2>
<dl class="faq">
<dt>How much does the classic 52-week challenge save?</dt>
<dd>$1,378. Week <em>n</em> saves <em>n</em> dollars, so the total is the sum of 1 through 52.
Customize the start amount and weekly increase above to see any variation instantly.</dd>
<dt>Do I have to follow the weeks in order?</dt>
<dd>No. Check off whichever weeks you complete. Many savers do the expensive weeks first (reverse
challenge) while motivation is high, then coast through the cheap weeks at the end.</dd>
<dt>Is my savings data private?</dt>
<dd>Completely. The tracker stores your progress in your browser's local storage and never sends it
anywhere. There is no account, no analytics, and no server.</dd>
<dt>What if I miss a week?</dt>
<dd>Just leave it unchecked and keep going. You can double up later or extend the challenge past
week 52 &mdash; the running total column shows exactly where you stand either way.</dd>
<dt>Can this help my small business finances too?</dt>
<dd>Saving consistently is half the equation; the other half is pricing your work so there is
something left to save. If you sell handmade goods, the paid calculator below turns your supply
costs, labor, and fees into prices that actually leave a margin.</dd>
</dl>
</section>

<section class="block">
<h2 class="sec">Related tools</h2>
<div class="grid">
<div class="card"><h3>Free Net Worth Tracker</h3><p>What you own minus what you owe, updated live and kept private.</p><a class="btn" href="../net-worth-tracker/index.html">Open the free tool</a></div>
<div class="card"><h3>Free Offline Habit Tracker</h3><p>Saving is a habit &mdash; build the daily streak behind it.</p><a class="btn" href="../habit-tracker/index.html">Open the free tool</a></div>
</div>
</section>

<div class="cta-band">
<h2>Sell handmade goods? Price them to actually profit.</h2>
<p>CraftCost is the offline pricing calculator for Etsy and craft sellers: enter supplies, build a
recipe per product, and get a suggested price for every sales channel &mdash; with a Healthy / Thin /
Underwater verdict on your current prices. One-time purchase, no subscription.</p>
<a class="btn" href="../../products/handmade-pricing-calculator-etsy-craft-sellers/index.html">See CraftCost &mdash; $14 one-time</a>
<p class="small">Prefer to browse everything? <a href="https://glenerds.gumroad.com">More offline micro-tools from Glenerds</a></p>
</div>
</main>
"""
    page = head("Free 52-Week Savings Challenge Calculator & Tracker | Glenerds",
        "Free 52-week savings challenge calculator: customize weekly amounts, track progress week by week, see your running total. Offline, no account, no subscription.",
        "/tools/savings-challenge/", extra=faq_ld_from_html(body)) + body + site_footer(2)
    write("tools/savings-challenge/index.html", page)

NW_JS = """
<script>
(function(){
  var KEY='glenerds-networth-v1';
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||{assets:[],debts:[]}}catch(e){return{assets:[],debts:[]}}}
  function save(d){localStorage.setItem(KEY,JSON.stringify(d))}
  var data=load();
  function uid(){return 'n'+Date.now().toString(36)+Math.floor(Math.random()*999)}
  function money(v){return '$'+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}
  function render(){
    function rows(list,el,btnId){
      var t=document.getElementById(el);t.innerHTML='';
      var sum=0;
      list.forEach(function(it){
        sum+=parseFloat(it.value)||0;
        var tr=document.createElement('tr');
        var td1=document.createElement('td');td1.textContent=it.name;
        var td2=document.createElement('td');td2.textContent=money(it.value);
        var td3=document.createElement('td');
        var b=document.createElement('button');b.textContent='Remove';b.className='plain';
        b.onclick=function(){var i=list.indexOf(it);list.splice(i,1);save(data);render()};
        td3.appendChild(b);tr.appendChild(td1);tr.appendChild(td2);tr.appendChild(td3);t.appendChild(tr);
      });
      return sum;
    }
    var aSum=rows(data.assets,'nw-assets');
    var dSum=rows(data.debts,'nw-debts');
    var nw=aSum-dSum;
    var el=document.getElementById('nw-result');
    el.innerHTML='Assets: '+money(aSum)+' &nbsp;|&nbsp; Debts: '+money(dSum)
      +'<br><strong>Net worth: '+money(nw)+'</strong>';
    el.style.color=nw>=0?'':'#c0392b';
  }
  document.getElementById('nw-add-asset').onclick=function(){
    var n=document.getElementById('nw-aname').value.trim(),v=parseFloat(document.getElementById('nw-avalue').value);
    if(!n||isNaN(v))return;data.assets.push({id:uid(),name:n,value:v});save(data);render();
    document.getElementById('nw-aname').value='';document.getElementById('nw-avalue').value='';
  };
  document.getElementById('nw-add-debt').onclick=function(){
    var n=document.getElementById('nw-dname').value.trim(),v=parseFloat(document.getElementById('nw-dvalue').value);
    if(!n||isNaN(v))return;data.debts.push({id:uid(),name:n,value:v});save(data);render();
    document.getElementById('nw-dname').value='';document.getElementById('nw-dvalue').value='';
  };
  document.getElementById('nw-export').onclick=function(){
    var blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    var aEl=document.createElement('a');aEl.href=URL.createObjectURL(blob);aEl.download='net-worth-backup.json';aEl.click();
  };
  render();
})();
</script>"""

def build_networth():
    body = site_header(2) + crumb(2, ["Free Tools", "Net Worth Tracker"]) + """
<main>
<div class="hero">
<h1>Free Net Worth Tracker &mdash; What You Own Minus What You Owe</h1>
<p class="lead">What's your net worth right now &mdash; really? List what you own (bank accounts, investments, home,
car) and what you owe (credit cards, loans, mortgage), and this free tracker subtracts one from the other
live as you type. No bank connections, no account, no sign-up: everything stays in your browser, nothing is
uploaded. Update it monthly and watch the number move.</p>
</div>

<div class="toolbox" role="region" aria-label="Net worth tracker">
<h3>Assets (what you own)</h3>
<input type="text" id="nw-aname" placeholder="e.g. Checking account" aria-label="Asset name">
<input type="number" id="nw-avalue" placeholder="0.00" step="0.01" aria-label="Asset value">
<button id="nw-add-asset">Add asset</button>
<table><thead><tr><th>Asset</th><th>Value</th><th></th></tr></thead><tbody id="nw-assets"></tbody></table>
<h3>Debts (what you owe)</h3>
<input type="text" id="nw-dname" placeholder="e.g. Credit card" aria-label="Debt name">
<input type="number" id="nw-dvalue" placeholder="0.00" step="0.01" aria-label="Debt value">
<button id="nw-add-debt">Add debt</button>
<table><thead><tr><th>Debt</th><th>Balance</th><th></th></tr></thead><tbody id="nw-debts"></tbody></table>
<p id="nw-result" style="font-size:1.15rem"></p>
<button id="nw-export" class="plain">Export backup</button>
<p class="small">Use round numbers or exact figures &mdash; whatever you are comfortable typing. It never leaves this device.</p>
</div>
""" + NW_JS + """
<div class="toolbox">
<h3 style="margin-top:0">Free forever &mdash; no paid version</h3>
<p>This net worth tracker is complete as-is: unlimited assets and debts, live totals, JSON export &mdash; free forever.</p>
<p><strong>Buying a condo?</strong> Your home may be your biggest asset &mdash; <a href="../../products/hoa-resale-package-reserve-study-risk-analyzer/index.html"><strong>HOA ReserveCheck &mdash; $9 one-time</strong></a> scores the HOA's finances from the resale-package figures and flags special-assessment risk before you buy. No subscription. No account.</p>
</div>

<section class="block prose">
<h2 class="sec">How to calculate your net worth</h2>
<p>Net worth is simply everything you own minus everything you owe. List bank balances, investment
accounts, your home's estimated value, vehicles, and anything else of meaningful value under assets.
List credit card balances, student loans, auto loans, mortgages, and any other debts under debts.
The tracker does the subtraction and shows the result live as you add items. Most people are
surprised the first time &mdash; in either direction &mdash; which is exactly why the number is worth
knowing: you cannot improve what you do not measure.</p>
<h2 class="sec">What to include (and what to skip)</h2>
<p>Include anything with real monetary value: cash, savings, brokerage and retirement accounts, home
equity (market value minus mortgage), cars at realistic resale value. Skip small household items;
tracking every coffee mug adds noise without insight. Update the numbers monthly or quarterly &mdash;
more often than that and you are mostly watching market noise. The trend over six to twelve months
is what matters: is the number climbing, flat, or sliding? A climbing number means your financial
system is working, whatever the starting point.</p>
<h2 class="sec">Why track it offline</h2>
<p>Net worth is the single most sensitive number in personal finance, and account-aggregator apps ask
you to hand it &mdash; along with your bank logins &mdash; to a third party. This tracker inverts that:
the math happens on your device, the data lives in your browser, and there is no company on the
other end. You give up automatic syncing; you keep complete privacy. For a number you check a few
times a year, that is a trade worth making.</p>
<h2 class="sec">Worked example</h2>
<p>Assets: $8,000 in savings and a $12,000 car &mdash; $20,000 total. Debts: a $3,500 credit card balance and
an $18,000 student loan &mdash; $21,500 total. Net worth: <strong>&minus;$1,500</strong>, shown in red. It
stings, but now it's a number instead of a feeling: pay $1,500 off the card and the tracker crosses into
positive territory the moment you update it.</p>
<h2 class="sec">Frequently asked questions</h2>
<dl class="faq">
<dt>Should my home count in net worth?</dt>
<dd>Yes, at a realistic market value, minus the remaining mortgage. Just remember that home equity
is illiquid &mdash; it counts, but you cannot spend it without selling or borrowing.</dd>
<dt>What about my car?</dt>
<dd>Include it at private-sale value, not what you paid. Cars depreciate, so revisit the number
yearly rather than letting an old figure flatter the total.</dd>
<dt>Is a negative net worth bad?</dt>
<dd>It is common, especially early in a career with student loans. What matters is the direction:
steady upward movement means the plan is working.</dd>
<dt>Where does my data go?</dt>
<dd>Nowhere. It is stored in your browser's local storage on your device. Export a JSON backup
before clearing browser data or switching devices.</dd>
<dt>My biggest asset is my home &mdash; how do I protect that investment?</dt>
<dd>Before buying a condo or townhome, the HOA's finances matter as much as the unit itself. The
paid analyzer below scores HOA financial health from resale-package figures and flags
special-assessment risk.</dd>
</dl>
</section>

<section class="block">
<h2 class="sec">Related tools</h2>
<div class="grid">
<div class="card"><h3>Free 52-Week Savings Challenge Calculator</h3><p>Grow the asset side with weekly savings math done for you.</p><a class="btn" href="../savings-challenge/index.html">Open the free tool</a></div>
<div class="card"><h3>Free Offline Habit Tracker</h3><p>The daily habits that move the number, tracked free.</p><a class="btn" href="../habit-tracker/index.html">Open the free tool</a></div>
</div>
</section>

<div class="cta-band">
<h2>Buying a condo? Check the HOA's finances first.</h2>
<p>HOA ReserveCheck is the offline risk analyzer for condo and townhome buyers: key in the figures
from the HOA documents and get a weighted financial-risk score, a special-assessment likelihood
gauge, and a printable due-diligence report. One-time purchase, no subscription.</p>
<a class="btn" href="../../products/hoa-resale-package-reserve-study-risk-analyzer/index.html">See HOA ReserveCheck &mdash; $9 one-time</a>
<p class="small">Prefer to browse everything? <a href="https://glenerds.gumroad.com">More offline micro-tools from Glenerds</a></p>
</div>
</main>
"""
    page = head("Free Net Worth Tracker — Calculate Your Net Worth Offline | Glenerds",
        "Free net worth tracker: list assets and debts, see your net worth instantly, track it over time. Runs offline in your browser; your financial data never leaves your device.",
        "/tools/net-worth-tracker/", extra=faq_ld_from_html(body)) + body + site_footer(2)
    write("tools/net-worth-tracker/index.html", page)

build_home()
build_habit()
build_savings()
build_networth()

# ---------------- PRODUCT PAGES ----------------
PRODUCTS = [
 dict(slug="online-fitness-coach-check-in-tracker", name="FitnessCheckIn",
  h1="Online Fitness Coach Check-In Tracker — Client Check-Ins, Comparisons & Feedback Drafts",
  meta="Offline client check-in tracker for online fitness coaches: log weekly check-ins, compare weeks side by side, generate client feedback in one click. $29 one-time, no subscription.",
  price="$29 one-time",
  url="https://glenerds.gumroad.com/l/online-fitness-coach-check-in-tracker",
  pitch="Online coaches lose hours every week to messy check-ins scattered across DMs, spreadsheets, and screenshots. This tracker gives you one offline home for your whole roster: log each client's weekly check-in, compare any two weeks side by side, and turn the numbers into a feedback message draft with a single click.",
  features=[
   "Client roster with per-client weekly check-in history, stored locally on your device",
   "Photo protocol checklists so clients submit the right shots every week",
   "Weight, measurements, macros vs. actuals, and 1–10 adherence scores per check-in",
   "Side-by-side week comparison to spot trends at a glance",
   "One-click client feedback message draft built from the week's data",
   "Runs offline in any modern browser — no account, no subscription, no uploads",
  ],
  uses=[
   "Physique and prep coaches managing weekly client check-ins",
   "Online coaches who want macros-vs-actuals tracking without a spreadsheet",
   "Coaches tired of digging through chat history for last week's numbers",
  ],
  faqs=[
   ("Do my clients need accounts too?","No. This is your coaching dashboard — clients send check-ins however they already do, and you log them here. Nothing for them to install or sign up for."),
   ("Where is client data stored?","On your device, in your browser. No cloud sync means no data-processing worries and no monthly fee — but keep your own backups."),
   ("Does it replace my coaching app?","It replaces the check-in spreadsheet and the DM archaeology. Programming, billing, and messaging stay wherever they already live."),
   ("Is it really a one-time purchase?","Yes. Pay once, download the file, use it forever. No subscription, no per-client pricing."),
  ]),
 dict(slug="cremacheck", name="CremaCheck",
  h1="Used Commercial Espresso Machine Inspection Checklist — Risk Score & Repair Estimates",
  meta="Offline inspection tool for used commercial espresso machine buyers: brand-specific checklists, scored risk verdict, repair-cost estimate, printable report. $29 one-time.",
  price="$29 one-time",
  url="https://glenerds.gumroad.com/l/cremacheck",
  pitch="A used commercial espresso machine can be the deal of the decade or a five-figure mistake. This inspection tool walks you through brand-specific checklists for La Marzocco, Synesso, Nuova Simonelli, and Victoria Arduino, then turns your findings into a scored low/medium/high risk verdict with a repair-cost estimate — before money changes hands.",
  features=[
   "Brand-specific inspection checklists for four major commercial manufacturers",
   "Weighted scoring that produces a clear low / medium / high risk verdict",
   "Repair-cost estimate based on the issues you flag during inspection",
   "Printable inspection report to support your negotiation",
   "Designed for dockside-style use: works offline on a phone or laptop",
   "One-time purchase — no account, no subscription",
  ],
  uses=[
   "Café owners buying a second machine on the used market",
   "Home baristas stepping up to a commercial machine",
   "Equipment flippers who need a fast, consistent inspection routine",
  ],
  faqs=[
   ("Does this replace a technician's pre-purchase inspection?","No — and it doesn't claim to. It helps you screen machines so you only pay a technician for the ones worth a closer look."),
   ("Which brands are covered?","La Marzocco, Synesso, Nuova Simonelli, and Victoria Arduino, each with its own checklist tuned to that brand's known weak points."),
   ("Can I use it at the seller's location?","Yes. It runs offline in any modern browser, so a phone or laptop works fine with no signal."),
   ("What do I get for the price?","The full inspection tool as a single offline file, yours forever after a one-time purchase."),
  ]),
 dict(slug="moving-company-quote-comparison-scam-checker", name="MoveAudit",
  h1="Moving Company Scam Checker — Compare Quotes & Spot Red Flags",
  meta="Offline moving-company vetting tool: score movers on 35 red-flag signals, compare up to 4 quotes side by side, verify USDOT credentials. $9 one-time, no subscription.",
  price="$9 one-time",
  url="https://glenerds.gumroad.com/l/moving-company-quote-comparison-scam-checker",
  image="/assets/moveaudit.png",
  pitch="Moving scams follow patterns: the too-low estimate, the demand for a big deposit, the name that doesn't match the USDOT record. This vetting tool scores every mover you consider against 35 red-flag signals, compares up to four quotes side by side ranked by risk, and checks estimates against the federal 110% rule — so the cheapest quote can't quietly become the most expensive move.",
  features=[
   "35-signal red-flag checklist covering the most common moving scam patterns",
   "Weighted scam-risk score per company, ranked for easy comparison",
   "Side-by-side comparison of up to 4 quotes in one view",
   "Estimate analyzer that enforces the federal 110% rule",
   "USDOT credential verification guidance built into the workflow",
   "Printable vetting report to keep with your moving paperwork",
  ],
  uses=[
   "Anyone comparing interstate movers and worried about rogue operators",
   "First-time movers who don't know what a legitimate estimate looks like",
   "People who received a suspiciously cheap quote and want a second opinion",
  ],
  faqs=[
   ("What is the federal 110% rule?","On interstate moves with a non-binding estimate, the mover generally can't demand more than 110% of the estimate at delivery. The tool's analyzer checks your quotes against it."),
   ("How do I verify a USDOT number?","The tool walks you through checking the mover's USDOT credentials against the federal database and flags mismatches like a name that doesn't match the record."),
   ("Does it work for local moves?","The red-flag signals and quote comparison apply to any move; the 110% rule specifically covers federally regulated interstate moves."),
   ("Why a one-time $9 tool instead of a free article?","Articles tell you what to watch for; this scores your actual movers and your actual quotes, then hands you a printable report."),
  ]),
 dict(slug="flipbid-reconciler", name="FlipBid Reconciler",
  h1="Contractor Bid Comparison Tool for House Flippers — Normalize Bids & Find Scope Gaps",
  meta="Offline bid-comparison tool for house flippers: normalize up to 3 contractor bids into one scope-of-work matrix, flag price gaps and missing items. $29 one-time.",
  price="$29 one-time",
  url="https://glenerds.gumroad.com/l/flipbid-reconciler",
  pitch="Three contractor bids, three different formats, three different scopes — comparing them is guesswork. This tool normalizes up to three bids into a single scope-of-work matrix, flags line items where one contractor's price diverges materially from the others, and calls out work a contractor didn't bid at all. The report tab turns it into a negotiation-ready variance report with talking points and projected profit vs. ARV.",
  features=[
   "Enter up to 3 contractor bids as line items in one normalized matrix",
   "Automatic flags for prices that diverge materially from competing bids",
   "Scope-hole detection: items a contractor didn't bid on at all",
   "Negotiation-ready variance report with per-contractor totals",
   "Projected profit vs. ARV so every bid is judged against the deal",
   "Offline single file — no account, no subscription, your numbers stay private",
  ],
  uses=[
   "House flippers comparing GC bids on a rehab",
   "Investors who need to defend their numbers to a contractor",
   "Landlords bidding out turnovers across multiple properties",
  ],
  faqs=[
   ("How many bids can I compare?","Up to three per project, which covers the standard get-three-bids workflow most investors use."),
   ("What counts as a material price difference?","The tool flags line items where one bid diverges meaningfully from the others, so you know exactly which numbers to question."),
   ("Can I print the report?","Yes — the report tab is built to be printed or saved, with talking points for the negotiation call."),
   ("Does it estimate ARV for me?","You enter your ARV; the tool projects profit against it so each bid is judged in the context of the deal."),
  ]),
 dict(slug="hoa-resale-package-reserve-study-risk-analyzer", name="HOA ReserveCheck",
  h1="HOA Financial Health Checker — Reserve Study & Special Assessment Risk Analyzer",
  meta="Offline risk analyzer for condo and townhome buyers: score HOA financial health from resale-package figures, flag special-assessment risk. $9 one-time, no subscription.",
  price="$9 one-time",
  url="https://glenerds.gumroad.com/l/hoa-resale-package-reserve-study-risk-analyzer",
  pitch="The condo looks perfect; the HOA's finances are the part that can blindside you. This analyzer takes the figures straight from the resale package and reserve study and produces a weighted financial-risk score, a special-assessment likelihood gauge, and Fannie Mae warrantability warning flags — plus a 12-item document-request checklist and a printable due-diligence report for your file.",
  features=[
   "Weighted HOA financial-risk score from resale-package figures you key in",
   "Special-assessment likelihood gauge based on reserve funding levels",
   "Fannie Mae warrantability warning flags that can affect your mortgage",
   "12-item document-request checklist so nothing is missing from the package",
   "Printable due-diligence report for your records or your agent",
   "Guidance only — not professional financial or legal advice",
  ],
  uses=[
   "First-time condo and townhome buyers in their due-diligence window",
   "Buyers comparing two HOAs and wanting an apples-to-apples risk read",
   "Anyone who has heard a special-assessment horror story and wants to avoid one",
  ],
  faqs=[
   ("What documents do I need?","The HOA resale package and reserve study — the 12-item checklist tells you exactly what to request if anything is missing."),
   ("What is a special assessment?","A one-time charge HOA members pay when reserves can't cover a major repair. The gauge estimates how likely one is based on funding levels."),
   ("Why do Fannie Mae flags matter?","If a condo project isn't warrantable, conventional financing gets harder. The tool flags the warning signs early."),
   ("Is this legal or financial advice?","No. It's a record-keeping and analysis tool that organizes the documents' figures into a clear risk picture — your agent, lender, or attorney makes the call."),
  ]),
 dict(slug="hullcheck", name="HullCheck",
  h1="Used Boat Pre-Purchase Inspection Checklist — Risk Score & Repair Cost Estimate",
  meta="Offline inspection tool for used-boat buyers: boat-type-specific checklists, weighted risk scoring, repair-cost estimates, printable report. $29 one-time.",
  price="$29 one-time",
  url="https://glenerds.gumroad.com/l/hullcheck",
  pitch="A used boat hides its problems well — until you're paying for them. Pick your boat type (outboard powerboat, sterndrive/inboard, sailboat, or pontoon), work the matching checklist dockside, and get a scored low/medium/high risk level, a repair-cost estimate, the effective total next to the asking price, and a printable inspection report to take into negotiation.",
  features=[
   "Four boat-type-specific checklists: outboard, sterndrive/inboard, sailboat, pontoon",
   "Weighted scoring with a clear low / medium / high risk verdict",
   "Repair-cost estimate for every issue you flag",
   "Effective total shown next to the asking price — the real cost of the boat",
   "Printable inspection report for your file or the negotiation table",
   "Works offline dockside on a phone or laptop — no account, no subscription",
  ],
  uses=[
   "First-time boat buyers doing their own pre-screening",
   "Buyers comparing several used boats on the same weekend",
   "Anyone deciding whether a cheap boat is a deal or a project",
  ],
  faqs=[
   ("Does this replace a marine surveyor?","No. It screens boats so you hire a surveyor only for the ones that pass — saving you the survey fee on the duds."),
   ("Which boat types are covered?","Outboard powerboats, sterndrive/inboard boats, sailboats, and pontoons, each with its own checklist."),
   ("What is the 'effective total'?","Asking price plus the estimated repair costs you flagged — the number that tells you what the boat really costs."),
   ("Can I really use it at the dock?","Yes. It's a single offline file; open it on your phone, no signal needed."),
  ]),
 dict(slug="depositdocket", name="Landlord Ledger",
  h1="Security Deposit Deduction Statement Generator for Landlords",
  meta="Offline record-keeping tool for landlords with 1-10 units: itemize security-deposit deductions, track return deadlines, print tenant statements. $14 one-time.",
  price="$14 one-time",
  url="https://glenerds.gumroad.com/l/depositdocket",
  pitch="Security deposit disputes are won on paperwork. This record-keeping tool is built for landlords with 1–10 units: record each tenancy, itemize every deposit deduction, watch the return-deadline countdown, and print a professional itemized statement for the tenant — the kind of documentation that ends arguments before they start.",
  features=[
   "Per-tenancy records with full deposit deduction itemization",
   "Return-deadline countdown so you never miss the statutory window",
   "Professional printable itemized statements for tenants",
   "Built for the 1–10 unit landlord — no enterprise bloat",
   "Offline single file: tenant data never leaves your device",
   "One-time purchase — a record-keeping tool, not legal advice",
  ],
  uses=[
   "Small landlords handling their own move-outs",
   "Accidental landlords renting out a former residence",
   "Property managers who want cleaner deposit documentation",
  ],
  faqs=[
   ("How many units does it support?","It's designed around the 1–10 unit landlord — simple enough to actually use, structured enough to hold up."),
   ("Does it handle my state's deadline?","It tracks the return deadline per tenancy; you enter your state's window. It's a tracker, not a legal reference — confirm your local rules."),
   ("Can I print the statement?","Yes — the itemized tenant statement is built to print cleanly and look professional."),
   ("Is tenant data private?","Completely. Everything is stored locally in your browser; nothing is uploaded anywhere."),
  ]),
 dict(slug="pitprofit", name="PitProfit",
  h1="Competition BBQ Expense & Payout Tracker — Season P&L for Pitmasters",
  meta="Offline season expense and payout tracker for competition BBQ teams: log every contest, see true season P&L, best/worst contests, cost per call. $29 one-time.",
  price="$29 one-time",
  url="https://glenerds.gumroad.com/l/pitprofit",
  pitch="Entry fees, meat, fuel, lodging, rubs, payouts, placements — a competition season's real numbers live in a shoebox. This tracker logs every contest in one place and answers the questions that matter: your true season P&L, your best and worst contests, and what every call (stage walk) actually cost you. Multi-season support, CSV export, and JSON backup included.",
  features=[
   "Per-contest logging: entry fees, meat, fuel, lodging, rubs, payouts, placements",
   "Instant season P&L — the true cost of competing",
   "Best and worst contest rankings by profitability",
   "Cost-per-call calculation for every stage walk",
   "Multi-season support with CSV export and JSON backup",
   "Single offline file — no account, no subscription",
  ],
  uses=[
   "KCBS and other sanctioning-body competition teams",
   "Pitmasters deciding which contests are worth entering next year",
   "Teams splitting costs who need clean, shareable numbers",
  ],
  faqs=[
   ("What is 'cost per call'?","Your total season spend divided by your calls (stage walks) — the real price of each moment in the spotlight."),
   ("Can I track multiple seasons?","Yes — multi-season support keeps each year's contests separate while letting you compare across years."),
   ("Can I get my data out?","CSV export for spreadsheets and JSON backup for safekeeping. Your data is yours."),
   ("Does it need internet at a contest?","No. It runs offline in the browser, so the fairground's dead zone is no problem."),
  ]),
 dict(slug="handmade-pricing-calculator-etsy-craft-sellers", name="CraftCost",
  h1="Handmade Pricing Calculator for Etsy & Craft Sellers — Supplies, Labor & Fees",
  meta="Offline pricing calculator for handmade sellers: turn supplies, labor, and marketplace fees into suggested prices per sales channel. $14 one-time, no subscription.",
  price="$14 one-time",
  url="https://glenerds.gumroad.com/l/handmade-pricing-calculator-etsy-craft-sellers",
  image="/assets/craftcost.png",
  pitch="Most handmade sellers underprice — not from generosity, but because the real cost was never added up. Enter your supplies, build a recipe per product, and get a suggested price for every sales channel, each with a Healthy / Thin / Underwater verdict on your current price. A built-in batch labor timer feeds your real minutes into each recipe's cost, so labor stops being a guess.",
  features=[
   "Per-product recipes: supplies, quantities, and costs in one place",
   "Batch labor timer so real minutes flow into each recipe's cost",
   "Suggested prices for every sales channel you sell on",
   "Healthy / Thin / Underwater verdict on your current pricing",
   "Built for candles, soap, jewelry, pottery, sewn goods, baked goods, and more",
   "Offline single file — pricing and record-keeping only, not tax or accounting advice",
  ],
  uses=[
   "Etsy sellers wondering if their prices actually cover costs",
   "Craft fair vendors setting prices across retail and wholesale",
   "Makers adding a new product line and needing a sane starting price",
  ],
  faqs=[
   ("What does the Healthy / Thin / Underwater verdict mean?","It rates your current price against your true cost: Healthy leaves real margin, Thin barely covers costs, Underwater loses money on every sale."),
   ("How does the labor timer work?","Time a production batch and the tool spreads those minutes across each unit's recipe cost — no more guessing your labor rate per item."),
   ("Does it handle marketplace fees?","Yes — fees per sales channel factor into the suggested price, so Etsy, craft fair, and wholesale prices each stand on their own."),
   ("Is this accounting software?","No. It's a pricing and record-keeping tool, not tax or accounting advice — but it gives your accountant much better numbers to work with."),
  ]),
 dict(slug="css-element-inspector-chrome", name="CSSHover",
  h1="CSS Element Inspector for Chrome — Copy CSS, Selectors & Tailwind in One Click",
  meta="Chrome extension for web designers and developers: hover any element to inspect it, click to lock, copy CSS, selectors, Tailwind classes, fonts. $9 one-time.",
  price="$9 one-time",
  url="https://glenerds.gumroad.com/l/css-element-inspector-chrome",
  pitch="See a design detail on any website and wonder how it's built? Hover any element on any page to inspect it, click to lock it, and instantly grab its unique CSS selector, all 47 computed style properties, the same styles converted to Tailwind utility classes, and the detected font — ready to paste into your own project.",
  features=[
   "Hover-to-inspect on any element of any web page",
   "Click-to-lock so you can examine tricky hover states",
   "Unique CSS selector generation for the locked element",
   "All 47 computed style properties, copy-ready",
   "One-click conversion to Tailwind utility classes",
   "Font detection for the inspected element",
  ],
  uses=[
   "Web designers reverse-engineering a layout detail they admire",
   "Developers grabbing exact styles instead of eyeballing them",
   "Tailwind users converting traditional CSS on the fly",
  ],
  faqs=[
   ("Which browser does it work in?","Chrome — it's built as a Chrome extension."),
   ("Does it send browsing data anywhere?","No. Everything runs locally in your browser: no accounts, no tracking, no network requests."),
   ("What is click-to-lock?","Hover highlights elements live; clicking locks the current one so you can inspect elements that only appear on hover."),
   ("Is it a one-time purchase?","Yes. Pay once, use it in your workflow indefinitely."),
  ]),
]

# ---------------- PRODUCT LIVE DEMOS (Phase 2) ----------------
# Compact interactive samples rendered above the main CTA on three product pages.
# Lightweight, client-side only, zero external requests. Each links the matching free tool.

DEMO_CSS = """<section class="block">
<h2 class="sec">Try it: specificity in 10 seconds</h2>
<div class="toolbox" role="region" aria-label="Specificity mini demo">
<p class="small">CSSHover copies a unique selector for any element you lock. Paste a selector below to see
how its specificity score breaks down &mdash; the same (a, b, c) math the extension exposes.</p>
<label>CSS selector: <input type="text" id="dcs-in" value="#nav .menu li.active a" style="width:65%" aria-label="CSS selector"></label>
<button id="dcs-go">Score it</button>
<div id="dcs-out" style="margin-top:1rem"></div>
<p class="small"><a href="../../tools/css-specificity-calculator/index.html">Open the full free CSS specificity calculator</a>
for detailed breakdowns, bar charts, and <code>:not()</code> / <code>:is()</code> / <code>:where()</code> handling.</p>
</div>
</section>
<script>
(function(){
  function specOf(sel){
    var a=0,b=0,c=0,s=String(sel);
    var ids=s.match(/#[A-Za-z0-9_-]+/g);if(ids)a+=ids.length;
    var cls=s.match(/\\.[A-Za-z0-9_-]+/g);if(cls)b+=cls.length;
    var attrs=s.match(/\\[[^\\]]+\\]/g);if(attrs)b+=attrs.length;
    var pseudoC=s.match(/:(?!:)[A-Za-z-]+(\\([^)]*\\))?/g);if(pseudoC)b+=pseudoC.length;
    var pseudoE=s.match(/::[A-Za-z-]+/g);if(pseudoE)c+=pseudoE.length;
    var els=s.replace(/#[A-Za-z0-9_-]+/g,' ').replace(/\\.[A-Za-z0-9_-]+/g,' ')
      .replace(/\\[[^\\]]+\\]/g,' ').replace(/::?[A-Za-z-]+(\\([^)]*\\))?/g,' ')
      .replace(/[\\s>+~]+/g,' ').trim().split(' ').filter(function(x){return x&&x!=='*';});
    c+=els.length;
    return [a,b,c];
  }
  function calc(){
    var sel=document.getElementById('dcs-in').value.trim();
    var out=document.getElementById('dcs-out');
    if(!sel){out.innerHTML='<p class="small">Enter a selector above.</p>';return;}
    var sp=specOf(sel);
    out.innerHTML='<p style="font-size:1.3rem"><strong>Specificity: '+sp[0]+','+sp[1]+','+sp[2]+'</strong></p>'
      +'<table><tbody>'
      +'<tr><td>ID selectors <code>#id</code></td><td>'+sp[0]+'</td></tr>'
      +'<tr><td>Classes, attributes, pseudo-classes</td><td>'+sp[1]+'</td></tr>'
      +'<tr><td>Elements, pseudo-elements</td><td>'+sp[2]+'</td></tr>'
      +'</tbody></table>'
      +'<p class="small">Higher columns win: any ID beats any number of classes; any class beats any number of elements.</p>';
  }
  document.getElementById('dcs-go').onclick=calc;
  document.getElementById('dcs-in').addEventListener('input',calc);
  calc();
})();
</script>"""

DEMO_DEPOSIT = """<section class="block">
<h2 class="sec">See it in action: a sample deposit statement</h2>
<div class="toolbox" role="region" aria-label="Deposit statement sample">
<p class="small">A sample move-out below &mdash; edit the numbers and watch the refund update. This is the
same itemized math DepositDocket (Landlord Ledger) tracks per tenancy, with return-deadline countdowns
and printable tenant statements in the full tool.</p>
<label>Deposit held: $<input type="number" id="dd-dep" value="1500" min="0" step="1" style="width:7rem" aria-label="Deposit held"></label>
<table><thead><tr><th>Deduction</th><th>Amount</th></tr></thead><tbody>
<tr><td>Carpet cleaning</td><td>$<input type="number" class="dd-amt" value="120" min="0" step="1" style="width:6rem" aria-label="Carpet cleaning amount"></td></tr>
<tr><td>Bedroom wall repaint</td><td>$<input type="number" class="dd-amt" value="180" min="0" step="1" style="width:6rem" aria-label="Wall repaint amount"></td></tr>
<tr><td>Unpaid water bill</td><td>$<input type="number" class="dd-amt" value="65" min="0" step="1" style="width:6rem" aria-label="Unpaid water bill amount"></td></tr>
</tbody></table>
<p id="dd-out" style="font-size:1.15rem"></p>
<p class="small">A record-keeping sample, not legal advice. <a href="../../tools/security-deposit-deduction-calculator/index.html">Try your own numbers in the free deposit deduction calculator</a>.</p>
</div>
</section>
<script>
(function(){
  function money(n){return '$'+n.toFixed(2);}
  function calc(){
    var dep=parseFloat(document.getElementById('dd-dep').value)||0;
    var tot=0,amts=document.querySelectorAll('.dd-amt');
    for(var i=0;i<amts.length;i++){tot+=parseFloat(amts[i].value)||0;}
    var refund=Math.max(0,dep-tot);
    document.getElementById('dd-out').innerHTML='<strong>Refund to tenant: '+money(refund)+'</strong>'
      +'<br><span class="small">Total deductions: '+money(tot)+' of '+money(dep)+' held.</span>';
  }
  document.getElementById('dd-dep').addEventListener('input',calc);
  var amts=document.querySelectorAll('.dd-amt');
  for(var i=0;i<amts.length;i++){amts[i].addEventListener('input',calc);}
  calc();
})();
</script>"""

DEMO_FLIPBID = """<section class="block">
<h2 class="sec">See it in action: two bids, one flip</h2>
<div class="toolbox" role="region" aria-label="Bid comparison sample">
<p class="small">Sample bids on a kitchen refresh &mdash; edit any price and the gaps recompute. Any line item
diverging more than 15% gets flagged: that is the number to question on the call. A zero in one column
means that contractor did not bid that scope at all &mdash; the classic scope hole.</p>
<table><thead><tr><th>Scope item</th><th>Bid A</th><th>Bid B</th><th>Gap</th></tr></thead><tbody id="fb-rows"></tbody></table>
<p class="small">FlipBid Reconciler does this across up to 3 bids, then builds a negotiation-ready variance
report with profit vs. ARV. <a href="../../tools/contractor-bid-comparison/index.html">Try the free two-bid comparison worksheet</a>.</p>
</div>
</section>
<script>
(function(){
  var items=[
    {d:'Cabinet refacing',a:3200,b:3850},
    {d:'Quartz counters',a:2400,b:2500},
    {d:'Tile backsplash',a:950,b:1450},
    {d:'Permit & disposal',a:400,b:0}
  ];
  function gapText(a,b){
    if(a&&b){var p=Math.abs(a-b)/Math.max(a,b)*100;return p.toFixed(0)+'%'+(p>15?' \\u26a0':'');}
    if(a||b)return 'only one bid';
    return '\\u2014';
  }
  function update(){
    items.forEach(function(it,idx){
      document.getElementById('fb-gap-'+idx).textContent=gapText(it.a,it.b);
    });
  }
  function build(){
    var tb=document.getElementById('fb-rows');
    items.forEach(function(it,idx){
      var tr=document.createElement('tr');
      var td0=document.createElement('td');td0.textContent=it.d;tr.appendChild(td0);
      ['a','b'].forEach(function(k){
        var td=document.createElement('td');
        var inp=document.createElement('input');
        inp.type='number';inp.min='0';inp.step='1';inp.style.width='6.5rem';inp.value=it[k];
        inp.setAttribute('aria-label',it.d+' \\u2014 bid '+(k==='a'?'A':'B'));
        inp.addEventListener('input',function(){it[k]=parseFloat(inp.value)||0;update();});
        td.appendChild(inp);tr.appendChild(td);
      });
      var tdg=document.createElement('td');tdg.id='fb-gap-'+idx;tr.appendChild(tdg);
      tb.appendChild(tr);
    });
    update();
  }
  build();
})();
</script>"""

DEMOS = {
    "css-element-inspector-chrome": DEMO_CSS,
    "depositdocket": DEMO_DEPOSIT,
    "flipbid-reconciler": DEMO_FLIPBID,
}


# Cross-link graph for product pages: companion free tool, related free tools,
# relevant alternative guide, and honest "not for" list. Paths are site-root-relative.
PRODUCT_XREF = {
 "online-fitness-coach-check-in-tracker": dict(
  free=("tools/fitness-client-check-in/", "Free Fitness Client Check-In Tracker",
        "Log one client's weekly check-ins \u2014 weight, measurements, adherence \u2014 free forever."),
  related=[("tools/habit-tracker/", "Free Offline Habit Tracker",
            "Daily adherence habits are what move client check-ins; track them free.")],
  alt=("alternatives/trainerize-truecoach-alternative/", "Trainerize / TrueCoach Alternative"),
  not_for=["You need client data synced automatically across your phone and laptop",
           "Multiple coaches share one client roster",
           "You want programming, billing, or messaging built into the same app"]),
 "cremacheck": dict(
  free=("tools/espresso-machine-inspection-checklist/", "Free Espresso Machine Inspection Checklist",
        "The generic inspection checklist with an issue tally and rough repair-cost estimate."),
  related=[("tools/used-boat-inspection-checklist/", "Free Used Boat Inspection Checklist",
            "The same pass/flag/fail inspection method, tuned for boats.")],
  alt=None,
  not_for=["You need a certified technician's report for insurance or financing",
           "You're buying new from a dealer with a warranty",
           "You manage a fleet of machines across locations"]),
 "moving-company-quote-comparison-scam-checker": dict(
  free=("tools/moving-cost-calculator/", "Free Moving Cost Calculator",
        "Estimate DIY, container, and full-service move costs to sanity-check the quotes you're comparing."),
  related=[("tools/security-deposit-deduction-calculator/", "Free Security Deposit Deduction Calculator",
            "Closing out the old place? Itemize deductions and compute the refund."),
           ("tools/contractor-bid-comparison/", "Free Contractor Bid Comparison Worksheet",
            "Settling in? Compare two contractor bids line by line.")],
  alt=("alternatives/moving-quote-websites-alternative/", "Moving Quote Website Alternative"),
  not_for=["You're moving fully DIY with no movers involved",
           "You want someone to book and manage the mover for you",
           "You need international shipping and customs brokerage"]),
 "flipbid-reconciler": dict(
  free=("tools/contractor-bid-comparison/", "Free Contractor Bid Comparison Worksheet",
        "Line up two bids item by item; gaps over 15% get flagged automatically."),
  related=[("tools/hoa-special-assessment-calculator/", "Free HOA Special Assessment Calculator",
            "Rehabbing a condo? Estimate what a special assessment would cost you.")],
  alt=("alternatives/servicetitan-alternative/", "ServiceTitan Alternative"),
  not_for=["You need to compare more than three bids on one project",
           "You want scheduling, dispatch, and crew management too",
           "You need automated contractor outreach and follow-up"]),
 "hoa-resale-package-reserve-study-risk-analyzer": dict(
  free=("tools/hoa-special-assessment-calculator/", "Free HOA Special Assessment Calculator",
        "Estimate your personal share of a special assessment from project cost, units, and reserves."),
  related=[("tools/security-deposit-deduction-calculator/", "Free Security Deposit Deduction Calculator",
            "Renting while you house-hunt? Keep the deposit math clean.")],
  alt=("alternatives/hoa-management-software-alternative/", "HOA Management Software Alternative"),
  not_for=["You're an HOA board member who needs management software",
           "You want professional financial or legal advice about a purchase",
           "You're analyzing a commercial or mixed-use association"]),
 "hullcheck": dict(
  free=("tools/used-boat-inspection-checklist/", "Free Used Boat Inspection Checklist",
        "The generic dockside checklist: hull, engine, trailer, electrics with a repair tally."),
  related=[("tools/espresso-machine-inspection-checklist/", "Free Espresso Machine Inspection Checklist",
            "The same inspection discipline, tuned for espresso machines.")],
  alt=None,
  not_for=["You need a certified marine survey for insurance or a loan",
           "You're buying new with a dealer warranty",
           "You manage a charter fleet and need maintenance tracking"]),
 "depositdocket": dict(
  free=("tools/security-deposit-deduction-calculator/", "Free Security Deposit Deduction Calculator",
        "Itemize deductions and compute the tenant refund \u2014 the core math, free."),
  related=[("tools/moving-cost-calculator/", "Free Moving Cost Calculator",
            "Between tenants? Budget the turnover move.")],
  alt=None,
  not_for=["You manage 50+ units and need full property management software",
           "You need trust accounting across multiple entities",
           "You want automatic bank reconciliation"]),
 "pitprofit": dict(
  free=("tools/bbq-contest-cost-tracker/", "Free BBQ Contest Cost Tracker",
        "Log one contest's real costs and payouts to see if the weekend made money."),
  related=[("tools/craft-pricing-calculator/", "Free Craft Pricing Calculator",
            "Sell rubs or sauces on the side? Price them to actually profit.")],
  alt=None,
  not_for=["You need full restaurant accounting and payroll",
           "You want tax filing or bookkeeping features",
           "Your whole team needs shared cloud books"]),
 "handmade-pricing-calculator-etsy-craft-sellers": dict(
  free=("tools/craft-pricing-calculator/", "Free Craft Pricing Calculator",
        "The same true-cost formula \u2014 materials, labor, fees, margin \u2014 with the Healthy / Thin / Underwater verdict."),
  related=[("tools/bbq-contest-cost-tracker/", "Free BBQ Contest Cost Tracker",
            "Sell at events too? Track whether a show weekend actually paid.")],
  alt=("alternatives/craftybase-alternative/", "Craftybase Alternative"),
  not_for=["You need inventory management across many SKUs",
           "You want stock levels synced across sales channels",
           "You need accounting or payroll features"]),
 "css-element-inspector-chrome": dict(
  free=("tools/css-specificity-calculator/", "Free CSS Specificity Calculator",
        "Paste any selector and see its specificity score counted and explained."),
  related=[],
  alt=None,
  not_for=["You want a full IDE debugging suite",
           "You need team design-system governance",
           "You don't work in Chrome"]),
}

def build_products():
    for p in PRODUCTS:
        shots = ""
        if p.get("image"):
            shots = f"""<h2 class="sec">Screenshots</h2>
<figure class="shots"><div>
<img src="../..{p['image']}" alt="{esc(p['name'])} product page showing the tool interface" loading="lazy">
<figcaption>{esc(p['name'])} — live product page</figcaption></div></figure>"""
        feat = "\n".join(f"<li>{esc(f)}</li>" for f in p["features"])
        uses = "\n".join(f"<li>{esc(u)}</li>" for u in p["uses"])
        faqs = "\n".join(f"<dt>{esc(q)}</dt>\n<dd>{esc(a)}</dd>" for q, a in p["faqs"])
        notfor = "\n".join(f"<li>{esc(n)}</li>" for n in PRODUCT_XREF[p["slug"]]["not_for"])
        x = PRODUCT_XREF[p["slug"]]
        fb = x["free"]
        freebox = f"""<div class="toolbox">
<h3 style="margin-top:0">Try the free companion tool first</h3>
<p><a href="../../{fb[0]}index.html"><strong>{esc(fb[1])}</strong></a> &mdash; {esc(fb[2])}</p>
<p class="small">Free forever, runs offline in your browser. {esc(p["name"])} is the full version for when you need more.</p>
</div>"""
        rel_cards = []
        for rpath, rname, rblurb in x["related"]:
            rel_cards.append(
                f'<div class="card"><h3>{esc(rname)}</h3><p>{esc(rblurb)}</p>'
                f'<a class="btn" href="../../{rpath}index.html">Open the free tool</a></div>')
        if x["alt"]:
            apath, aname = x["alt"]
            rel_cards.append(
                f'<div class="card"><h3>{esc(aname)}</h3>'
                f'<p>An honest comparison: when the one-time offline tool wins, and when the subscription alternative is the better call.</p>'
                f'<a class="btn" href="../../{apath}index.html">Read the comparison</a></div>')
        relfree = ""
        if rel_cards:
            relfree = ('<section class="block">\n<h2 class="sec">Related free tools</h2>\n<div class="grid">\n'
                       + "\n".join(rel_cards) + '\n</div>\n</section>')
        demo = DEMOS.get(p["slug"], "")
        body = site_header(2) + crumb(2, ["Products", esc(p["name"])]) + f"""
<main>
<div class="hero">
<h1>{esc(p["h1"])}</h1>
<p class="lead">{esc(p["pitch"])}</p>
<span class="pricebox">{esc(p["price"])}</span>
<a class="btn" href="{esc(p["url"])}">Get it on Gumroad</a>
<p class="small">One-time purchase. The tool runs offline in your browser — no account, no subscription.</p>
</div>
{shots}
{freebox}
<section class="block prose">
<h2 class="sec">What it does</h2>
<ul class="feat">
{feat}
</ul>
<h2 class="sec">Who this is for</h2>
<ul class="feat">
{uses}
</ul>
<h2 class="sec">Who this isn't for</h2>
<ul class="feat">
{notfor}
</ul>
<p>The honest filter: if you want a simple offline tool you pay for once and own forever, this fits.
If you need cloud sync, team seats, or integrations with other platforms, you'll be happier with a
subscription product &mdash; and that's fine. This tool is deliberately not that.</p>
<h2 class="sec">Frequently asked questions</h2>
<dl class="faq">
{faqs}
</dl>
</section>
{demo}
{relfree}
<div class="cta-band">
<h2>Get {esc(p["name"])} today</h2>
<p>{esc(p["price"])} — one-time purchase, yours forever. No subscription.</p>
<a class="btn" href="{esc(p["url"])}">Get it on Gumroad</a>
<p class="small">Prefer to browse everything? <a href="{STORE_URL}">More offline micro-tools from Glenerds</a></p>
</div>
</main>
"""
        page = head(p["h1"] + " | Glenerds", p["meta"], f"/products/{p['slug']}/",
                    og_image=p.get("image"), extra=json_ld(p) + "\n" + faq_ld(p["faqs"])) + body + site_footer(2)
        write(f"products/{p['slug']}/index.html", page)

def build_sitemap_page():
    free_tools = [
        ("tools/habit-tracker/", "Free Offline Habit Tracker", "Daily streaks with no account, stored in your browser."),
        ("tools/savings-challenge/", "Free 52-Week Savings Challenge Calculator", "Weekly savings math with a running total, all 52 weeks."),
        ("tools/net-worth-tracker/", "Free Net Worth Tracker", "Assets minus debts, updated live, private by design."),
        ("tools/moving-cost-calculator/", "Free Moving Cost Calculator", "DIY, container, and full-service move estimates by home size and distance."),
        ("tools/craft-pricing-calculator/", "Free Craft Pricing Calculator", "True-cost pricing for handmade goods with a profit verdict."),
        ("tools/fitness-client-check-in/", "Free Fitness Client Check-In Tracker", "Weekly client check-in log for online coaches."),
        ("tools/espresso-machine-inspection-checklist/", "Free Espresso Machine Inspection Checklist", "Point-by-point used-machine inspection with repair-cost estimate."),
        ("tools/contractor-bid-comparison/", "Free Contractor Bid Comparison Worksheet", "Line up two bids item by item; gaps over 15% flagged."),
        ("tools/hoa-special-assessment-calculator/", "Free HOA Special Assessment Calculator", "Your share of a special assessment, in dollars and months of dues."),
        ("tools/security-deposit-deduction-calculator/", "Free Security Deposit Deduction Calculator", "Itemize deductions, compute the tenant refund, print a statement."),
        ("tools/bbq-contest-cost-tracker/", "Free BBQ Contest Cost Tracker", "One contest weekend's real P&amp;L."),
        ("tools/css-specificity-calculator/", "Free CSS Specificity Calculator", "Specificity scores for any selector, counted and explained."),
        ("tools/used-boat-inspection-checklist/", "Free Used Boat Inspection Checklist", "Dockside pre-purchase inspection with repair tally."),
        ("tools/compound-interest-calculator/", "Free Compound Interest Calculator", "Growth projections with inflation, fees, and tax adjustments."),
    ]
    guides = [
        ("alternatives/servicetitan-alternative/", "ServiceTitan Alternative", "FlipBid Reconciler vs. contractor management suites."),
        ("alternatives/craftybase-alternative/", "Craftybase Alternative", "CraftCost vs. inventory + pricing SaaS for makers."),
        ("alternatives/moving-quote-websites-alternative/", "Moving Quote Website Alternative", "MoveAudit vs. lead-gen moving quote sites."),
        ("alternatives/hoa-management-software-alternative/", "HOA Management Software Alternative", "HOA ReserveCheck vs. management software, for buyers."),
        ("alternatives/trainerize-truecoach-alternative/", "Trainerize / TrueCoach Alternative", "FitnessCheckIn vs. coaching platforms."),
    ]
    embeds = [
        ("embed/moving-cost-calculator/", "Moving Cost Calculator"),
        ("embed/craft-pricing-calculator/", "Craft Pricing Calculator"),
        ("embed/css-specificity-calculator/", "CSS Specificity Calculator"),
        ("embed/security-deposit-deduction-calculator/", "Security Deposit Deduction Calculator"),
        ("embed/hoa-special-assessment-calculator/", "HOA Special Assessment Calculator"),
    ]
    def cards(items):
        return "\n".join(
            f'<div class="card"><h3>{n}</h3><p>{d}</p><a class="btn" href="../{s}index.html">Open</a></div>'
            for s, n, d in items)
    def plain(items):
        return "\n".join(
            f'<div class="card"><h3>{n}</h3><p>{d}</p><a class="btn" href="../{s}index.html">Open</a></div>'
            for s, n, d in items)
    body = site_header(1) + crumb(1, ["Site Map"]) + """
<main>
<div class="hero">
<h1>Site Map &mdash; Everything on Glenerds</h1>
<p class="lead">Every free tool, paid product, comparison guide, and embeddable widget on this site, in one place.</p>
</div>
<section class="block">
<h2 class="sec">Free tools</h2>
<div class="grid">
""" + cards(free_tools) + """
</div></section>
<section class="block">
<h2 class="sec">Paid products &mdash; one-time purchase</h2>
<div class="grid">
""" + "\n".join(
        f'<div class="card"><h3>{esc(p["name"])}</h3><p>{esc(p["meta"].split(".")[0])}.</p>'
        f'<span class="price">{esc(p["price"])}</span>'
        f'<a class="btn" href="../products/{p["slug"]}/index.html">Learn more</a></div>'
        for p in PRODUCTS) + """
</div></section>
<section class="block">
<h2 class="sec">Alternative guides</h2>
<div class="grid">
""" + plain([(s, n, d) for s, n, d in guides]) + """
</div></section>
<section class="block">
<h2 class="sec">Embeddable tools</h2>
<div class="grid">
""" + "\n".join(
        f'<div class="card"><h3>{n}</h3><p>Embed this free calculator on your own site with a copy-paste snippet.</p>'
        f'<a class="btn" href="../{s}index.html">Get the embed code</a></div>'
        for s, n in embeds) + """
</div></section>
<section class="block">
<h2 class="sec">More from Glenerds</h2>
<ul class="feat">
<li><a href="../affiliates/index.html">Glenerds affiliate program</a> &mdash; earn 30% promoting the paid tools.</li>
<li><a href="../tools/index.html">All 14 free tools</a> &mdash; the complete free-tool index.</li>
<li><a href="https://glenerds.gumroad.com">Glenerds store on Gumroad</a> &mdash; every paid product in one place.</li>
</ul>
</section>
</main>
"""
    page = head("Site Map \u2014 Every Free Tool, Product & Guide | Glenerds",
                "Complete site map for Glenerds: all 14 free offline tools, 10 paid one-time products, 5 alternative guides, and embeddable calculators.",
                "/site-map/") + body + site_footer(1)
    write("site-map/index.html", page)

def build_aux():
    pages = ["", "tools/", "tools/habit-tracker/", "tools/savings-challenge/", "tools/net-worth-tracker/",
             "tools/moving-cost-calculator/", "tools/craft-pricing-calculator/", "tools/fitness-client-check-in/",
             "tools/espresso-machine-inspection-checklist/", "tools/contractor-bid-comparison/",
             "tools/hoa-special-assessment-calculator/", "tools/security-deposit-deduction-calculator/",
             "tools/bbq-contest-cost-tracker/", "tools/css-specificity-calculator/",
             "tools/used-boat-inspection-checklist/", "tools/compound-interest-calculator/"]
    pages += [f"products/{p['slug']}/" for p in PRODUCTS]
    # Phase 2 pages (hand-written; build.py only registers them in the sitemap)
    pages += ["alternatives/servicetitan-alternative/",
              "alternatives/craftybase-alternative/",
              "alternatives/moving-quote-websites-alternative/",
              "alternatives/hoa-management-software-alternative/",
              "alternatives/trainerize-truecoach-alternative/",
              "embed/",
              "embed/moving-cost-calculator/",
              "embed/craft-pricing-calculator/",
              "embed/css-specificity-calculator/",
              "embed/security-deposit-deduction-calculator/",
              "embed/hoa-special-assessment-calculator/",
              "affiliates/",
              "site-map/"]
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /staging/\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("wrote robots.txt")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pg in pages:
        sm.append(f"  <url><loc>{SITE_URL}/{pg}</loc><lastmod>2026-09-19</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if pg=='' else '0.8'}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    print("wrote sitemap.xml", len(pages), "urls")

build_sitemap_page()
build_products()
build_aux()
print("BUILD COMPLETE")
