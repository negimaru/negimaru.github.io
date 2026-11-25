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
V = {"css": 5, "js": 3}
LANGS = S["langs"]


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
<script>try{{var t=localStorage.getItem("theme");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}}catch(_){{}}</script>
<link rel="stylesheet" href="{pre}assets/css/site.css?v={V['css']}">
<script src="{pre}assets/js/site.js?v={V['js']}" defer></script>
</head>"""


IDS = {"es": ["trabajo", "proyectos", "formacion"], "en": ["work", "projects", "education"]}


def masthead(L, key, home, other_href):
    ui = L["ui"]
    other = "en" if key == "es" else "es"
    nav = "".join(f'<li><a href="{home}#{i}">{e(n)}</a></li>' for i, n in zip(IDS[key], ui["nav"]))
    seg = "".join(f'<button type="button" data-theme-set="{v}" aria-pressed="false">{e(t)}</button>'
                  for v, t in zip(["light", "dark", "auto"], ui["themes"]))
    return f"""<a class="skip" href="#main">{e(ui['skip'])}</a>
<header class="bar"><div class="wrap bar-in">
<a class="me" href="{home}">Victor Martin<span class="surname"> Rodriguez</span></a>
<nav aria-label="{e(ui['navLabel'])}"><ul class="nav">{nav}</ul></nav>
<div class="bar-tools">
<div class="seg" role="group" aria-label="{e(ui['theme'])}" hidden>{seg}</div>
<a class="lang" href="{other_href}" hreflang="{other}" lang="{other}">{e(ui['otherLang'])}</a>
</div>
</div></header>"""


def footer(L):
    return f"""<footer class="foot"><div class="wrap">
<p>{links(L['footer'], L['ui'])}</p>
</div></footer>
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

    plays = []
    for p in pl["items"]:
        plays.append(f'<li class="play"><figure class="screen"><img src="{pre}assets/img/{p["img"]}" width="1200" height="675" '
                     f'alt="{e(p["alt"])}" loading="lazy" decoding="async"></figure>'
                     f'<h3>{e(p["name"])}</h3><p class="role">{e(p["meta"])}</p><p>{P(p["body"])}</p></li>')
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
    html = head(L, L["title"], L["description"], canonical, alternates, pre) + f"""
<body>
{masthead(L, key, "./", other_href)}
<main id="main">
<section class="wrap hero" aria-labelledby="t-intro">
<h1 id="t-intro">{e(S['fullName'])}</h1>
<p class="tagline">{e(it['role'])}</p>
<div class="hero-text">{intro}</div>
</section>

<section id="{ids[0]}" class="wrap sec" aria-labelledby="t-work">
<h2 id="t-work">{e(w['title'])}</h2>
<ol class="rows">{''.join(jobs)}</ol>
</section>

<section class="wrap sec case" aria-labelledby="t-case">
<div class="case-text">
<h2 id="t-case">{e(c['title'])}</h2>
<h3>{e(c['name'])}</h3>
<p class="role">{e(c['years'])}</p>
{case_body}
</div>
<figure class="screen"><img src="{pre}assets/img/{c['img']}" width="{c['w']}" height="{c['h']}" alt="{e(c['alt'])}" loading="lazy" decoding="async"></figure>
</section>

<section id="{ids[1]}" class="tint" aria-labelledby="t-play"><div class="wrap sec">
<h2 id="t-play">{e(pl['title'])}</h2>
<p class="lede">{e(pl['intro'])}</p>
<ul class="plays">{''.join(plays)}</ul>
<h3 class="also-t">{e(pl['alsoTitle'])}</h3>
<ul class="also">{also}</ul>
</div></section>

<section id="{ids[2]}" class="wrap sec duo" aria-labelledby="t-edu">
<div><h2 id="t-edu">{e(ed['title'])}</h2>
<ol class="rows rows-tight">{edu}</ol></div>
<div><h2 id="t-lang">{e(lg['title'])}</h2>
<p>{e(lg['text'])}</p></div>
</section>
</main>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
""" + footer(L)
    out = os.path.join(ROOT, L["path"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)


def not_found():
    L = LANGS["es"]; ui = L["ui"]
    html = head(L, ui["notFoundTitle"], L["description"], SITE + "404.html", [], "/", noindex=True) + f"""
<body>
{masthead(L, 'es', '/', '/en/')}
<main id="main"><section class="wrap hero">
<h1>{e(ui['notFoundTitle'])}</h1>
<p>{e(ui['notFoundBody'])} <a href="/">{e(ui['notFoundBack'])}</a>.</p>
</section></main>
""" + footer(L)
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
