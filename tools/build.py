"""Build the portfolio from data/site.json: / (Spanish), /en/ (English), 404, sitemap, robots.

Run: python3 tools/build.py   — never hand-edit the generated .html files.
Inline links in the data: [label](target), where target is a URL or a key of S["links"].
"""
import json
import os
import re
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(ROOT, "data/site.json"), encoding="utf-8"))
SITE = S["siteUrl"]
V = {"css": 9, "js": 6}
LANGS = S["langs"]
ICONS = json.load(open(os.path.join(ROOT, "data/tech-icons.json"), encoding="utf-8"))  # Simple Icons, CC0


def svg(paths):
    return (f'<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>')


I_PAD = '<svg class="pad" viewBox="0 0 16 10" shape-rendering="crispEdges" aria-hidden="true" focusable="false"><rect x="2" y="0" width="1" height="1" fill="currentColor"/><rect x="3" y="0" width="1" height="1" fill="currentColor"/><rect x="4" y="0" width="1" height="1" fill="currentColor"/><rect x="5" y="0" width="1" height="1" fill="currentColor"/><rect x="6" y="0" width="1" height="1" fill="currentColor"/><rect x="7" y="0" width="1" height="1" fill="currentColor"/><rect x="8" y="0" width="1" height="1" fill="currentColor"/><rect x="9" y="0" width="1" height="1" fill="currentColor"/><rect x="10" y="0" width="1" height="1" fill="currentColor"/><rect x="11" y="0" width="1" height="1" fill="currentColor"/><rect x="12" y="0" width="1" height="1" fill="currentColor"/><rect x="13" y="0" width="1" height="1" fill="currentColor"/><rect x="1" y="1" width="1" height="1" fill="currentColor"/><rect x="2" y="1" width="1" height="1" fill="currentColor"/><rect x="3" y="1" width="1" height="1" fill="currentColor"/><rect x="4" y="1" width="1" height="1" fill="currentColor"/><rect x="5" y="1" width="1" height="1" fill="currentColor"/><rect x="6" y="1" width="1" height="1" fill="currentColor"/><rect x="7" y="1" width="1" height="1" fill="currentColor"/><rect x="8" y="1" width="1" height="1" fill="currentColor"/><rect x="9" y="1" width="1" height="1" fill="currentColor"/><rect x="10" y="1" width="1" height="1" fill="currentColor"/><rect x="11" y="1" width="1" height="1" fill="currentColor"/><rect x="12" y="1" width="1" height="1" fill="currentColor"/><rect x="13" y="1" width="1" height="1" fill="currentColor"/><rect x="14" y="1" width="1" height="1" fill="currentColor"/><rect x="0" y="2" width="1" height="1" fill="currentColor"/><rect x="1" y="2" width="1" height="1" fill="currentColor"/><rect x="2" y="2" width="1" height="1" fill="currentColor"/><rect x="3" y="2" width="1" height="1" fill="var(--bg)"/><rect x="4" y="2" width="1" height="1" fill="currentColor"/><rect x="5" y="2" width="1" height="1" fill="currentColor"/><rect x="6" y="2" width="1" height="1" fill="currentColor"/><rect x="7" y="2" width="1" height="1" fill="currentColor"/><rect x="8" y="2" width="1" height="1" fill="currentColor"/><rect x="9" y="2" width="1" height="1" fill="currentColor"/><rect x="10" y="2" width="1" height="1" fill="currentColor"/><rect x="11" y="2" width="1" height="1" fill="currentColor"/><rect x="12" y="2" width="1" height="1" fill="currentColor"/><rect x="13" y="2" width="1" height="1" fill="currentColor"/><rect x="14" y="2" width="1" height="1" fill="currentColor"/><rect x="15" y="2" width="1" height="1" fill="currentColor"/><rect x="0" y="3" width="1" height="1" fill="currentColor"/><rect x="1" y="3" width="1" height="1" fill="currentColor"/><rect x="2" y="3" width="1" height="1" fill="var(--bg)"/><rect x="3" y="3" width="1" height="1" fill="var(--bg)"/><rect x="4" y="3" width="1" height="1" fill="var(--bg)"/><rect x="5" y="3" width="1" height="1" fill="currentColor"/><rect x="6" y="3" width="1" height="1" fill="currentColor"/><rect x="7" y="3" width="1" height="1" fill="currentColor"/><rect x="8" y="3" width="1" height="1" fill="currentColor"/><rect x="9" y="3" width="1" height="1" fill="currentColor"/><rect x="10" y="3" width="1" height="1" fill="currentColor"/><rect x="11" y="3" width="1" height="1" fill="var(--accent)"/><rect x="12" y="3" width="1" height="1" fill="currentColor"/><rect x="13" y="3" width="1" height="1" fill="currentColor"/><rect x="14" y="3" width="1" height="1" fill="currentColor"/><rect x="15" y="3" width="1" height="1" fill="currentColor"/><rect x="0" y="4" width="1" height="1" fill="currentColor"/><rect x="1" y="4" width="1" height="1" fill="currentColor"/><rect x="2" y="4" width="1" height="1" fill="currentColor"/><rect x="3" y="4" width="1" height="1" fill="var(--bg)"/><rect x="4" y="4" width="1" height="1" fill="currentColor"/><rect x="5" y="4" width="1" height="1" fill="currentColor"/><rect x="6" y="4" width="1" height="1" fill="currentColor"/><rect x="7" y="4" width="1" height="1" fill="currentColor"/><rect x="8" y="4" width="1" height="1" fill="currentColor"/><rect x="9" y="4" width="1" height="1" fill="currentColor"/><rect x="10" y="4" width="1" height="1" fill="var(--accent)"/><rect x="11" y="4" width="1" height="1" fill="currentColor"/><rect x="12" y="4" width="1" height="1" fill="var(--accent)"/><rect x="13" y="4" width="1" height="1" fill="currentColor"/><rect x="14" y="4" width="1" height="1" fill="currentColor"/><rect x="15" y="4" width="1" height="1" fill="currentColor"/><rect x="0" y="5" width="1" height="1" fill="currentColor"/><rect x="1" y="5" width="1" height="1" fill="currentColor"/><rect x="2" y="5" width="1" height="1" fill="currentColor"/><rect x="3" y="5" width="1" height="1" fill="currentColor"/><rect x="4" y="5" width="1" height="1" fill="currentColor"/><rect x="5" y="5" width="1" height="1" fill="currentColor"/><rect x="6" y="5" width="1" height="1" fill="var(--bg)"/><rect x="7" y="5" width="1" height="1" fill="var(--bg)"/><rect x="8" y="5" width="1" height="1" fill="currentColor"/><rect x="9" y="5" width="1" height="1" fill="currentColor"/><rect x="10" y="5" width="1" height="1" fill="currentColor"/><rect x="11" y="5" width="1" height="1" fill="var(--accent)"/><rect x="12" y="5" width="1" height="1" fill="currentColor"/><rect x="13" y="5" width="1" height="1" fill="currentColor"/><rect x="14" y="5" width="1" height="1" fill="currentColor"/><rect x="15" y="5" width="1" height="1" fill="currentColor"/><rect x="0" y="6" width="1" height="1" fill="currentColor"/><rect x="1" y="6" width="1" height="1" fill="currentColor"/><rect x="2" y="6" width="1" height="1" fill="currentColor"/><rect x="3" y="6" width="1" height="1" fill="currentColor"/><rect x="4" y="6" width="1" height="1" fill="currentColor"/><rect x="5" y="6" width="1" height="1" fill="currentColor"/><rect x="6" y="6" width="1" height="1" fill="currentColor"/><rect x="7" y="6" width="1" height="1" fill="currentColor"/><rect x="8" y="6" width="1" height="1" fill="currentColor"/><rect x="9" y="6" width="1" height="1" fill="currentColor"/><rect x="10" y="6" width="1" height="1" fill="currentColor"/><rect x="11" y="6" width="1" height="1" fill="currentColor"/><rect x="12" y="6" width="1" height="1" fill="currentColor"/><rect x="13" y="6" width="1" height="1" fill="currentColor"/><rect x="14" y="6" width="1" height="1" fill="currentColor"/><rect x="15" y="6" width="1" height="1" fill="currentColor"/><rect x="0" y="7" width="1" height="1" fill="currentColor"/><rect x="1" y="7" width="1" height="1" fill="currentColor"/><rect x="2" y="7" width="1" height="1" fill="currentColor"/><rect x="3" y="7" width="1" height="1" fill="currentColor"/><rect x="4" y="7" width="1" height="1" fill="currentColor"/><rect x="11" y="7" width="1" height="1" fill="currentColor"/><rect x="12" y="7" width="1" height="1" fill="currentColor"/><rect x="13" y="7" width="1" height="1" fill="currentColor"/><rect x="14" y="7" width="1" height="1" fill="currentColor"/><rect x="15" y="7" width="1" height="1" fill="currentColor"/><rect x="1" y="8" width="1" height="1" fill="currentColor"/><rect x="2" y="8" width="1" height="1" fill="currentColor"/><rect x="3" y="8" width="1" height="1" fill="currentColor"/><rect x="12" y="8" width="1" height="1" fill="currentColor"/><rect x="13" y="8" width="1" height="1" fill="currentColor"/><rect x="14" y="8" width="1" height="1" fill="currentColor"/></svg>'
I_IN = svg('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>')
I_GH = svg('<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.1-1.3-.3-2.5-1-3.5.3-1.2.3-2.4 0-3.5 0 0-1 0-3 1.5a10.4 10.4 0 0 0-5.5 0C6.5 2 5.5 2 5.5 2c-.3 1.1-.3 2.3 0 3.5A5.4 5.4 0 0 0 4.5 9c0 3.5 3 5.5 6 5.5-.4.5-.8 1-1 1.6-.2.6-.3 1.2-.2 1.9v4"/><path d="M9 18c-4.5 2-5-2-7-2"/>')


def tech_tiles():
    out = []
    for t in ICONS:
        fill = "currentColor" if t["hex"] in ("#000000", "#FFFFFF") else t["hex"]
        out.append(f'<li class="tech"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="{fill}" d="{t["path"]}"/></svg>'
                   f'<span>{e(t["label"])}</span></li>')
    return "".join(out)


def links(text, ui):
    """Escape text, then turn [label](target) into links; off-site links open in a new tab."""
    def repl(m):
        label, target = m.group(1), m.group(2)
        href = S["links"].get(target, target)
        return (f'<a href="{e(href)}" target="_blank" rel="noopener">{label}'
                f'<span class="sr-only"> {e(ui["newTab"])}</span></a>')
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, e(text, quote=False))
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def head(L, title, desc, canonical, alternates, pre, noindex=False):
    alt = "".join(f'<link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternates)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="{L['htmlLang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canonical}">{alt}
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{L['locale']}">
<meta property="og:image" content="{SITE}assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<script>try{{var t=localStorage.getItem("theme");if(t==="dark"||t==="light"||t==="8bit")document.documentElement.dataset.theme=t}}catch(_){{}}</script>
<link rel="stylesheet" href="{pre}assets/css/site.css?v={V['css']}">
<script src="{pre}assets/js/site.js?v={V['js']}" defer></script>
</head>"""


IDS = {"es": ["sobre-mi", "experiencia", "proyectos", "formacion"], "en": ["about", "experience", "projects", "education"]}


def tools_row(L, key, other_href):
    ui = L["ui"]
    other = "en" if key == "es" else "es"
    seg = "".join(f'<button type="button" data-theme-set="{v}" aria-pressed="false">{e(t)}</button>'
                  for v, t in zip(["light", "dark", "auto"], ui["themes"]))
    return (f'<div class="tools"><div class="seg" role="group" aria-label="{e(ui["theme"])}" hidden>{seg}</div>'
            f'<a class="lang" href="{other_href}" hreflang="{other}" lang="{other}">{e(ui["otherLang"])}</a></div>')


def side(L, key, other_href, home="./"):
    """Left column: who I am, where I am on the page, how to reach me. Sticky on wide screens."""
    ui, it = L["ui"], L["intro"]
    nav = "".join(f'<li><a href="{home}#{i}">{e(n)}</a></li>' for i, n in zip(IDS[key], ui["nav"]))
    ext = lambda href, icon, label: (f'<a class="btn" href="{href}" target="_blank" rel="noopener">{icon}{label}'
                                    f'<span class="sr-only"> {e(ui["newTab"])}</span></a>')
    return f"""<header class="side">
{tools_row(L, key, other_href)}
<h1 id="t-intro"><a href="{home}">{e(it['greeting'])}</a></h1>
<p class="lead">{e(it['lead'])}</p>
<nav aria-label="{e(ui['navLabel'])}"><ul class="toc">{nav}</ul></nav>
<p class="social">{ext(S['links']['linkedin'], I_IN, 'LinkedIn')}{ext(S['links']['github'], I_GH, 'GitHub')}</p>
</header>"""


def footer(L):
    return f"""<footer class="foot">
<p>{links(L['footer'], L['ui'])}</p>
<p class="konami" hidden>{e(L['ui']['konami'])}</p>
</footer>
</body>
</html>
"""


def page(key):
    L = LANGS[key]
    ui = L["ui"]
    canonical = SITE + L["path"]
    pre = "" if key == "es" else "../"
    other_href = "en/" if key == "es" else "../"
    alternates = [("es", SITE), ("en", SITE + "en/"), ("x-default", SITE)]
    it, w, c, pl, ed, lg = L["intro"], L["work"], L["case"], L["play"], L["education"], L["languages"]
    P = lambda t: links(t, ui)

    intro = "".join(f"<p>{P(t)}</p>" for t in it["paras"])

    jobs = []
    for j in w["jobs"]:
        body = "".join(f"<p>{P(t)}</p>" for t in j["body"])
        stack = f'<p class="stack">{e(j["stack"])}</p>' if j.get("stack") else ""
        jobs.append(f'<li class="row"><p class="when">{e(j["years"])}</p><div class="what">'
                    f'<h3>{e(j["company"])}</h3><p class="role">{e(j["role"])}</p>{body}{stack}</div></li>')

    case_body = "".join(f"<p>{P(t)}</p>" for t in c["body"])

    def proj_row(img, w_, h_, alt, name, meta, body):
        return (f'<li class="proj"><figure class="screen"><img src="{pre}assets/img/{img}" width="{w_}" height="{h_}" '
                f'alt="{e(alt)}" loading="lazy" decoding="async"></figure>'
                f'<div><h3>{e(name)}</h3><p class="role">{e(meta)}</p>{body}</div></li>')

    plays = []
    for p in pl["items"]:
        plays.append(proj_row(p["img"], 1200, 675, p["alt"], p["name"], p["meta"], f'<p>{P(p["body"])}</p>'))
    also = "".join(f"<li>{P(t)}</li>" for t in pl["also"])

    edu = "".join(f'<li class="row"><p class="when">{e(x["years"])}</p><p class="what">{e(x["text"])}</p></li>'
                  for x in ed["items"])

    ld = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "inLanguage": L["htmlLang"],
        "url": canonical,
        "mainEntity": {
            "@type": "Person",
            "name": S["fullName"],
            "jobTitle": "Frontend developer",
            "worksFor": {"@type": "Organization", "name": "ifeel"},
            "address": {"@type": "PostalAddress", "addressLocality": "Torrox", "addressRegion": "Málaga", "addressCountry": "ES"},
            "knowsLanguage": ["es", "en", "de"],
            "sameAs": [S["links"]["linkedin"], S["links"]["github"]],
            "url": SITE,
        },
    }

    ids = IDS[key]
    ph = S.get("photo")
    photo = (f'<figure class="me-photo"><img src="{pre}assets/img/{ph["file"]}" width="{ph["w"]}" height="{ph["h"]}" '
             f'alt="{e(ui["photoAlt"])}" fetchpriority="high"></figure>') if ph else ""
    html = head(L, L["title"], L["description"], canonical, alternates, pre) + f"""
<body>
<a class="skip" href="#main">{e(ui['skip'])}</a>
<div class="layout">
{side(L, key, other_href)}
<main id="main">
<section id="{ids[0]}" class="sec" aria-labelledby="t-about">
<h2 id="t-about">{e(L['about']['title'])}</h2>
{photo}
<div class="story">{intro}</div>
<h3 class="sub">{e(L['tech']['title'])}</h3>
<p>{P(L['tech']['body'])}</p>
<ul class="techs">{tech_tiles()}</ul>
</section>

<section id="{ids[1]}" class="sec" aria-labelledby="t-work">
<h2 id="t-work">{e(w['title'])}</h2>
<ol class="rows">{''.join(jobs)}</ol>
</section>

<section id="{ids[2]}" class="sec" aria-labelledby="t-proj">
<h2 id="t-proj">{e(L['projects']['title'])}</h2>
<ul class="projs">{proj_row(c['img'], c['w'], c['h'], c['alt'], c['name'], L['projects']['caseMeta'], case_body)}</ul>
<h3 class="sub">{e(pl['title'])}</h3>
<p>{e(pl['intro'])}</p>
<p><button class="play8" type="button" aria-pressed="false" hidden>{I_PAD}{e(ui['play8'])}</button></p>
<ul class="projs">{''.join(plays)}</ul>
<h3 class="sub">{e(pl['alsoTitle'])}</h3>
<ul class="also">{also}</ul>
</section>

<section id="{ids[3]}" class="sec" aria-labelledby="t-edu">
<h2 id="t-edu">{e(ed['title'])}</h2>
<ol class="rows rows-tight">{edu}</ol>
<h3 class="sub">{e(lg['title'])}</h3>
<p>{e(lg['text'])}</p>
</section>
""" + footer(L).replace("</body>", "</main>\n</div>\n<script type=\"application/ld+json\">" + json.dumps(ld, ensure_ascii=False) + "</script>\n</body>", 1)
    out = os.path.join(ROOT, L["path"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)


def not_found():
    L = LANGS["es"]; ui = L["ui"]
    html = head(L, ui["notFoundTitle"], L["description"], SITE + "404.html", [], "/", noindex=True) + f"""
<body>
<a class="skip" href="#main">{e(ui['skip'])}</a>
<div class="layout">
{side(L, 'es', '/en/', home='/')}
<main id="main"><section class="sec">
<h2>{e(ui['notFoundTitle'])}</h2>
<p>{e(ui['notFoundBody'])} <a href="/">{e(ui['notFoundBack'])}</a>.</p>
</section>
""" + footer(L).replace("</body>", "</main>\n</div>\n</body>", 1)
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(html)


def sitemap():
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{SITE}{x["path"]}"/>' for k, x in LANGS.items())
    urls = "".join(f"<url><loc>{SITE}{L['path']}</loc>{alts}</url>" for L in LANGS.values())
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + "</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")


for k in LANGS:
    page(k)
not_found()
sitemap()
print("built:", ", ".join("/" + L["path"] for L in LANGS.values()), "+ 404, sitemap, robots")
