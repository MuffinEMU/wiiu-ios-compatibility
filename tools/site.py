#!/usr/bin/env python3
"""Builds the compatibility website into _site/ from data/games.json and site/.

Run: python3 tools/site.py        then open _site/index.html through any static server.

Copyright (c) 2026 MuffinEMU Development Team (Void). SPDX-License-Identifier: GPL-3.0-only
"""
import html, json, os, re, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
SITE = "https://muffinemu.github.io/wiiu-ios-compatibility/"
REPO = "https://github.com/MuffinEMU/wiiu-ios-compatibility"
H = html.escape
RANK = {"runs-well": 0, "playable": 1, "runs-with-issues": 2, "reported-working": 3, "broken": 4}

def load():
    with open(os.path.join(ROOT, "data", "games.json"), encoding="utf-8") as f:
        return json.load(f)

def part(name):
    with open(os.path.join(ROOT, "site", "parts", name), encoding="utf-8") as f:
        return f.read()

def device_key(d):
    s = d.lower()
    if "a12z" in s: return "iPad Pro (A12Z)"
    if "a16" in s: return "iPad (A16)"
    for m in ("iphone 16", "iphone 15 pro", "iphone 14", "iphone 13 pro max", "iphone 13", "iphone 12"):
        if m in s: return m.title().replace("Iphone", "iPhone")
    return None

def best_fps(g):
    """The highest frame rate in a game's reports, for sorting and the card."""
    top = 0
    for r in g["reports"]:
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", r["fps"])]
        if nums and "n/a" not in r["fps"].lower(): top = max(top, max(nums))
    return int(top)

def fps_text(r):
    f = r["fps"].strip()
    if f.lower() in ("", "not stated", "n/a"): return ""
    return f + " fps" if any(c.isdigit() for c in f) else f

def footage_path(u):
    m = re.search(r"/blob/main/(snapshots/.+)$", u)
    return m.group(1) if m else None

def head(title, desc, base, path):
    canon = SITE + path
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- Wii U on iOS compatibility site. Copyright (c) 2026 MuffinEMU Development Team (Void). SPDX-License-Identifier: GPL-3.0-only. Additional terms (GPL-3.0 section 7) apply: see ATTRIBUTION.md. -->
<title>{H(title)}</title>
<meta name="description" content="{H(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Void (MuffinEMU)">
<meta property="og:type" content="website"><meta property="og:site_name" content="Wii U on iOS compatibility">
<meta property="og:title" content="{H(title)}"><meta property="og:description" content="{H(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="https://muffinemu.github.io/MuffinEMU/social-preview.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{base}assets/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{base}assets/icon-180.png">
<meta name="theme-color" content="#05060B" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#F4F5FA" media="(prefers-color-scheme: light)">
<link rel="preload" href="{base}assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/site.css"><link rel="stylesheet" href="{base}assets/compat.css">
<script src="{base}assets/theme.js"></script>
</head>
"""

def header(base, current, data):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{base}{href}"{cur}>{label}</a>'
    nav = "\n      ".join([
        a("index.html", "Home", "home"), a("index.html#games", "Games", "games"), a("devices.html", "Devices", "devices"),
        a("testing.html", "Testing", "testing"), a("contribute.html", "Contribute", "contribute"),
        '<a href="https://muffinemu.github.io/MuffinEMU/">MuffinEMU</a>',
        f'<a href="{REPO}">GitHub</a>'])
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{base}index.html"><img src="{base}assets/icon-64.png" alt="" width="30" height="30"><span>Wii U on iOS</span></a>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      {nav}
      <button class="nav-theme" type="button" data-palette-open="theme "><span class="theme-dot" aria-hidden="true"></span>Theme: <span data-theme-name>Bakery (Original)</span></button>
    </nav>
    <div class="header-tools">
      <button class="icon-btn search-btn" type="button" data-palette-open aria-label="Search and commands"><svg aria-hidden="true"><use href="#i-search"/></svg><span class="label">Search</span><span class="kbd" data-shortcut>⌘K</span></button>
      <button class="icon-btn theme-btn" type="button" data-palette-open="theme "><span class="theme-dot" aria-hidden="true"></span><span class="label" data-theme-name>Bakery (Original)</span></button>
      <button class="icon-btn mode-btn" type="button" data-mode-cycle aria-label="Colour mode"><svg class="auto" aria-hidden="true"><use href="#i-auto"/></svg><svg class="moon" aria-hidden="true"><use href="#i-moon"/></svg><svg class="sun" aria-hidden="true"><use href="#i-sun"/></svg></button>
      <button class="icon-btn nav-toggle" type="button" data-nav-toggle aria-controls="site-nav" aria-expanded="false" aria-label="Menu"><svg aria-hidden="true"><use href="#i-menu"/></svg></button>
    </div>
    <div class="progress" aria-hidden="true"></div>
  </div>
</header>"""

def footer(base):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{base}index.html" style="margin-bottom:12px"><img src="{base}assets/icon-64.png" alt="" width="30" height="30"><span>Wii U on iOS</span></a>
        <p style="margin:0">A community list of Wii U games run on iPhone and iPad.</p>
        <p style="margin:10px 0 0">Website designed and built by <strong>Void</strong>, creator of <a href="https://muffinemu.github.io/MuffinEMU/">MuffinEMU</a>, a Wii U emulator for iOS.</p>
      </div>
      <nav aria-label="Footer">
        <a href="{base}index.html#games">Games</a><a href="{base}devices.html">Devices</a><a href="{base}testing.html">Testing</a><a href="{base}contribute.html">Contribute</a>
        <a href="{REPO}">GitHub</a><a href="https://muffinemu.github.io/MuffinEMU/discord">Discord</a>
      </nav>
    </div>
    <p class="fineprint">Site code is GPL-3.0; the data is CC BY 4.0 (credit "Wii U on iOS compatibility list (MuffinEMU)"). Wii U and the game titles belong to Nintendo and their owners. This list is not affiliated with Nintendo and contains no games, keys or firmware.</p>
    <div class="footer-mark" aria-hidden="true">Wii U on iOS</div>
  </div>
</footer>"""

def page(title, desc, base, path, current, body, extra_script=""):
    return (head(title, desc, base, path) + f'<body data-base="{base}">\n' + part("sprite.html") +
            '\n<a class="skip-link" href="#main">Skip to content</a>\n<div class="backdrop" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grid-lines"></div><div class="grain"></div></div>\n' +
            header(base, current, None) + "\n" + body + "\n" + footer(base) + "\n" + part("palette.html") +
            f'\n<script src="{base}assets/app.js"></script>\n<script src="{base}assets/compat.js"></script>\n{extra_script}</body>\n</html>\n')

def status_badge(data, s):
    return f'<span class="st st-{s}">{H(data["statuses"][s])}</span>'

# ------------------------------------------------------------------ pages
def home(data):
    games = data["games"]
    runs = sum(1 for g in games if g["status"] == "runs-well")
    devs = {device_key(r["device"]) for g in games for r in g["reports"]} - {None}
    clips = sum(len(g["footage"]) for g in games)
    cards = []
    for g in sorted(games, key=lambda g: (RANK[g["status"]], g["name"].lower())):
        fps = best_fps(g); nd = len({device_key(r["device"]) or r["device"] for r in g["reports"] if r["device"].lower() != "not stated"})
        meta = []
        if fps: meta.append(f'<span class="fps">{fps} fps best</span>')
        meta.append(f'<span>{nd} device{"s" if nd != 1 else ""}</span>' if nd else "<span>No device details yet</span>")
        meta.append("<span>Footage</span>" if g["footage"] else "<span>Footage wanted</span>")
        search = " ".join([g["name"], data["statuses"][g["status"]]] + [r["device"] + " " + r["note"] for r in g["reports"]]).lower()
        cards.append(f'<a class="card gcard" href="games/{g["slug"]}.html" data-status="{g["status"]}" data-name="{H(g["name"].lower())}" data-fps="{fps}" data-rank="{RANK[g["status"]]}" data-search="{H(search)}" data-reveal><div>{status_badge(data, g["status"])}</div><h3>{H(g["name"])}</h3><div class="meta">{"".join(meta)}</div></a>')
    chips = "".join(f'<button type="button" class="fbtn" data-status="{k}" aria-pressed="false">{H(v)}</button>' for k, v in data["statuses"].items())
    body = f"""<main id="main" tabindex="-1">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="pill"><span class="pulse" aria-hidden="true"></span>Community list · Wii U on iPhone &amp; iPad</span>
      <h1 class="wordmark">Wii U on <span class="accent">iOS</span></h1>
      <p class="lede">Which Wii U games actually run on iPhone and iPad? Real devices, real frame rates and real gameplay footage, gathered by players and kept in the open.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="#games"><svg aria-hidden="true"><use href="#i-gamepad"/></svg>Browse the games</a>
        <a class="btn btn-outline" href="contribute.html"><svg aria-hidden="true"><use href="#i-github"/></svg>Report a game</a>
      </div>
      <p class="hero-note">Results come from MuffinEMU and from other Wii U emulators on iOS. <a href="testing.html">What we are testing next →</a></p>
    </div>
    <div class="hero-visual" aria-hidden="true" data-anim>
      <div class="orb"></div><div class="ring"></div><div class="ring r2"></div><div class="ring r3"></div>
      <div class="hero-icon"><div class="hero-face"><img class="hero-img" data-theme-icon src="{base_icons()}bakery.svg" alt="" width="192" height="192" fetchpriority="high"></div></div>
      <script>MuffinThemes.paintIcons()</script>
      <span class="chip c1"><i></i>{len(games)} games</span><span class="chip c2"><i></i>{len(devs)} devices</span><span class="chip c3"><i></i>{clips} clip{"s" if clips != 1 else ""}</span>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true">Scroll<span></span></div>
</section>

<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <div class="stats" data-stagger>
      <div class="card stat" data-reveal><b>{len(games)}</b><span>games listed</span></div>
      <div class="card stat" data-reveal style="--i:1"><b>{runs}</b><span>run well</span></div>
      <div class="card stat" data-reveal style="--i:2"><b>{len(devs)}</b><span>devices reporting</span></div>
      <div class="card stat" data-reveal style="--i:3"><b>{clips}</b><span>footage clip{"s" if clips != 1 else ""}</span></div>
    </div>
  </div>
</section>

<section class="section" id="games">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <span class="eyebrow">Games</span>
      <h2>Every game we have a report for</h2>
      <p>Search, filter by how well it runs, or sort by frame rate. Open a game for the devices, notes and footage.</p>
    </div>
    <div class="tools" data-reveal>
      <input id="gsearch" class="search" type="search" placeholder="Search games, devices, notes" aria-label="Search games" autocomplete="off">
      <select id="gsort" class="sortsel" aria-label="Sort games"><option value="status">Best status first</option><option value="fps">Highest frame rate</option><option value="name">Name A to Z</option></select>
      <button type="button" class="fbtn" id="gsurprise">Surprise me</button>
    </div>
    <div class="filters" role="group" aria-label="Filter by status" style="margin-bottom:22px"><button type="button" class="fbtn" data-status="all" aria-pressed="true">All</button>{chips}</div>
    <p class="crumbs" id="gcount" aria-live="polite"></p>
    <div class="gcards" id="gcards" data-stagger>{"".join(cards)}</div>
    <p class="empty" id="gempty" hidden>No game matches that. <a href="contribute.html">Report it</a> and it will be added.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">How it works</span><h2>Built by players, in the open</h2></div>
    <div class="grid grid-3" data-stagger>
      <div class="card pillar" data-reveal><span class="card-icon"><svg aria-hidden="true"><use href="#i-gamepad"/></svg></span><h3>Play and report</h3><p>Run a game on your own dump, then fill in a short form: the game, your device, the app version and the frame rate.</p></div>
      <div class="card pillar" data-reveal><span class="card-icon"><svg aria-hidden="true"><use href="#i-display"/></svg></span><h3>Add footage</h3><p>A 30 to 60 second clip with the frame counter on shows how it really ran. Clips live in the repository, next to the data.</p></div>
      <div class="card pillar" data-reveal><span class="card-icon"><svg aria-hidden="true"><use href="#i-open"/></svg></span><h3>Open data</h3><p>Everything is in one file on GitHub. Reuse it freely under CC BY 4.0, and fix anything you spot.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="card" data-reveal style="text-align:center">
      <h2 style="margin-top:0">Testing progress</h2>
      <p>We are working through a checklist of games on a handful of devices: <strong id="homeprog">…</strong> done so far.</p>
      <a class="btn btn-outline" href="testing.html">See the checklist</a>
    </div>
  </div>
</section>
</main>"""
    return page("Wii U on iOS: game compatibility", "A community list of Wii U games run on iPhone and iPad, with devices, frame rates, problems and gameplay footage.", "", "index.html", "home", body, '<script>fetch("https://api.github.com/repos/MuffinEMU/wiiu-ios-compatibility/issues/1").then(function(r){return r.json()}).then(function(i){var b=String(i.body||"").split(/\\r?\\n/),d=0,t=0;b.forEach(function(l){var m=l.match(/^\\s*- \\[( |x|X)\\]/);if(m){t++;if(m[1]!==" ")d++}});var e=document.getElementById("homeprog");if(e&&t)e.textContent=d+" of "+t}).catch(function(){var e=document.getElementById("homeprog");if(e)e.textContent="some"})</script>\n')

def base_icons():
    return "https://muffinemu.github.io/MuffinEMU/assets/icons/"

def game_page(data, g, i):
    games = data["games"]
    side = "".join(f'<a href="{x["slug"]}.html"' + (' aria-current="page"' if x["slug"] == g["slug"] else "") + f'><span class="dot st-{x["status"]}"></span><span class="n">{H(x["name"])}</span></a>' for x in sorted(games, key=lambda x: x["name"].lower()))
    rows = ""
    for r in g["reports"]:
        rows += f'<tr><td>{H(r["device"])}</td><td><strong>{H(fps_text(r)) or "&mdash;"}</strong></td><td>{H(r["note"]) or "&mdash;"}</td><td>{H(r["source"])}</td></tr>'
    reports = (f'<div class="reports-wrap"><table class="reports"><thead><tr><th scope="col">Device</th><th scope="col">Frame rate</th><th scope="col">Notes</th><th scope="col">Source</th></tr></thead><tbody>{rows}</tbody></table></div>'
               if rows else '<p>No device details yet. <a href="../contribute.html">Report how it runs</a>.</p>')
    clips = ""
    for n, u in enumerate(g["footage"], 1):
        p = footage_path(u)
        src = ("../" + p) if p else u
        name = os.path.basename(p or u)
        clips += f'<figure class="clip"><video controls preload="metadata" playsinline src="{H(src)}"></video><figcaption>Clip {n}: {H(name)} · <a href="{H(u)}">open on GitHub</a></figcaption></figure>' if p else f'<p><a href="{H(u)}">Footage {n}</a></p>'
    if not clips: clips = '<p>No footage yet. <a href="../contribute.html">Add a clip</a> and it will show up here.</p>'
    prev = sorted(games, key=lambda x: x["name"].lower()); idx = [x["slug"] for x in prev].index(g["slug"])
    nav = ""
    if idx > 0: nav += f'<a href="{prev[idx-1]["slug"]}.html"><span class="dir">Previous</span>&larr; {H(prev[idx-1]["name"])}</a>'
    else: nav += "<span></span>"
    nav += f'<a href="{prev[(idx+1)%len(prev)]["slug"]}.html" style="text-align:right"><span class="dir">Next</span>{H(prev[(idx+1)%len(prev)]["name"])} &rarr;</a>'
    body = f"""<div class="docs-shell">
  <aside class="docs-sidebar"><p class="sidebar-title">Games</p><nav class="sidegames" aria-label="Games">{side}</nav></aside>
  <main class="docs-content" id="main" tabindex="-1">
    <nav class="docs-breadcrumb" aria-label="Breadcrumb"><ol><li><a href="../index.html">Home</a></li><li><a href="../index.html#games">Games</a></li><li aria-current="page">{H(g["name"])}</li></ol></nav>
    <h1>{H(g["name"])}</h1>
    <p class="subtitle">{status_badge(data, g["status"])} &nbsp;{H(MEAN(data, g["status"]))}</p>
    <section class="symptom"><h2>Reports</h2>{reports}</section>
    <section class="symptom"><h2>Footage</h2>{clips}</section>
    <section class="symptom"><h2>Ran it? Tell us.</h2><p class="symptom-answer">One report per game and device is perfect.</p><p><a class="btn btn-primary" href="{REPO}/issues/new?template=report-a-game.yml">Report this game</a></p></section>
    <nav class="doc-next" aria-label="Previous and next game">{nav}</nav>
  </main>
</div>"""
    desc = f'{g["name"]} on iPhone and iPad: {data["statuses"][g["status"]].lower()}. Devices, frame rates, notes and footage from players.'
    return page(f'{g["name"]} on iOS: compatibility', desc, "../", f'games/{g["slug"]}.html', "games", body)

def MEAN(data, s):
    return {"runs-well": "Reported at a steady 60 fps or close to it on at least one device.",
            "playable": "Reported playable; the frame rate or small problems vary.",
            "runs-with-issues": "Starts and plays, with a clear problem such as audio or graphics.",
            "broken": "Reported not working.",
            "reported-working": "Reported working on at least one device, without more detail yet."}[s]

def devices(data):
    games = sorted(data["games"], key=lambda g: g["name"].lower())
    cols = []
    for g in games:
        for r in g["reports"]:
            k = device_key(r["device"])
            if k and k not in cols: cols.append(k)
    order = lambda k: (0 if "iPad" in k else 1, k)
    cols.sort(key=order)
    head_ = "".join(f"<th scope='col'>{H(c)}</th>" for c in cols)
    rows = ""
    for g in games:
        cells = ""
        for c in cols:
            rep = [r for r in g["reports"] if device_key(r["device"]) == c]
            if rep:
                t = " / ".join(fps_text(r) or "reported" for r in rep)
                cells += f'<td class="cell c-{g["status"] if g["status"] != "reported-working" else "playable"}">{H(t)}</td>'
            else:
                cells += '<td class="none">&mdash;</td>'
        rows += f'<tr><th scope="row"><a href="games/{g["slug"]}.html">{H(g["name"])}</a></th>{cells}</tr>'
    body = f"""<main class="section" id="main" tabindex="-1" style="padding-top:clamp(110px,16vh,170px)">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Devices</span><h1 style="font-size:clamp(2rem,5vw,3.4rem);margin:.2em 0">Which device runs what</h1><p>Every frame rate we have, by device. A dash means nobody has reported that game on that device yet, which is where you can help.</p></div>
    <div class="mx-wrap"><table class="mx"><thead><tr><th scope="col">Game</th>{head_}</tr></thead><tbody>{rows}</tbody></table></div>
    <div class="legend"><span class="st st-runs-well">Runs well</span><span class="st st-playable">Playable</span><span class="st st-runs-with-issues">Runs with issues</span><span class="st st-broken">Doesn't work yet</span></div>
  </div>
</main>"""
    return page("Which device runs what: Wii U on iOS compatibility", "A device by game table of Wii U frame rates on iPhone and iPad.", "", "devices.html", "devices", body)

def testing(data):
    body = """<main class="section" id="main" tabindex="-1" style="padding-top:clamp(110px,16vh,170px)">
  <div class="wrap" style="max-width:860px">
    <div class="section-head"><span class="eyebrow">Testing</span><h1 style="font-size:clamp(2rem,5vw,3.4rem);margin:.2em 0">What we are testing next</h1><p>This is the live checklist from GitHub. It updates by itself as boxes are ticked.</p></div>
    <div class="card"><div class="bar"><i id="pbar"></i></div><p class="pcount"><span id="pnum">Loading…</span><span id="ppct"></span></p></div>
    <div id="checklist" aria-live="polite"><p class="empty">Loading the checklist…</p></div>
    <p style="margin-top:28px"><a class="btn btn-outline" href="https://github.com/MuffinEMU/wiiu-ios-compatibility/issues/1">Open the checklist on GitHub</a></p>
  </div>
</main>"""
    return page("Test checklist: Wii U on iOS compatibility", "The live checklist of Wii U games and devices we are testing.", "", "testing.html", "testing", body)

def contribute(data):
    body = f"""<main class="section" id="main" tabindex="-1" style="padding-top:clamp(110px,16vh,170px)">
  <div class="wrap" style="max-width:860px">
    <div class="section-head"><span class="eyebrow">Contribute</span><h1 style="font-size:clamp(2rem,5vw,3.4rem);margin:.2em 0">Add your results</h1><p>You need your own legally dumped games. Never share games, keys or firmware, or links to them.</p></div>
    <ol class="steps">
      <li><h3 style="margin:0">Play the game</h3><p>Turn on the performance overlay so the frame rate is on screen. Note your device, iOS version, the app and its version, and whether JIT was on.</p></li>
      <li><h3 style="margin:0">Record 30 to 60 seconds</h3><p>Show actual gameplay, not a menu. Turn on Do Not Disturb first so no notifications, names or Apple ID show up. Name the file with the game, device and app version.</p></li>
      <li><h3 style="margin:0">Send it in</h3><p>Open the report form and attach the clip, or add it to <code>snapshots/&lt;game&gt;/</code> in a pull request.</p><p><a class="btn btn-primary" href="{REPO}/issues/new?template=report-a-game.yml">Open the report form</a></p></li>
    </ol>
    <div class="grid grid-2" style="margin-top:36px">
      <div class="card"><h3 style="margin-top:0">Fix the data</h3><p>The list is one file, <code>data/games.json</code>. Edit it, run <code>python3 tools/build.py</code>, and open a pull request.</p><a href="{REPO}/blob/main/CONTRIBUTING.md">Read the full guide</a></div>
      <div class="card"><h3 style="margin-top:0">Join the chat</h3><p>Ask questions, share results and find people with the same device.</p><a href="https://muffinemu.github.io/MuffinEMU/discord">MuffinEMU Discord</a></div>
    </div>
  </div>
</main>"""
    return page("Add your results: Wii U on iOS compatibility", "How to report a Wii U game and add gameplay footage to the compatibility list.", "", "contribute.html", "contribute", body)

def not_found():
    body = """<main class="section" id="main" tabindex="-1" style="padding-top:clamp(120px,20vh,200px);text-align:center"><div class="wrap"><h1>That page isn't here</h1><p>Try the <a href="/wiiu-ios-compatibility/index.html">game list</a>.</p></div></main>"""
    return page("Page not found", "Page not found.", "/wiiu-ios-compatibility/", "404.html", "", body)

def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f: f.write(text)

def main():
    data = load()
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "site", "assets"), os.path.join(OUT, "assets"))
    snaps = os.path.join(ROOT, "snapshots")
    if os.path.isdir(snaps):
        for dp, dn, fn in os.walk(snaps):
            for f in fn:
                if f == ".gitkeep": continue
                s = os.path.join(dp, f); d = os.path.join(OUT, os.path.relpath(s, ROOT))
                os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy(s, d)
    write("index.html", home(data)); write("devices.html", devices(data)); write("testing.html", testing(data)); write("contribute.html", contribute(data)); write("404.html", not_found())
    for i, g in enumerate(data["games"]): write(f"games/{g['slug']}.html", game_page(data, g, i))
    today = datetime.date.today().isoformat()
    urls = ["index.html", "devices.html", "testing.html", "contribute.html"] + [f"games/{g['slug']}.html" for g in data["games"]]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write(".nojekyll", "")
    print(f"built {len(urls)+1} pages into _site/")

if __name__ == "__main__":
    main()
