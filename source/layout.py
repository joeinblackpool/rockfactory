"""Site-wide tidy-up, run LAST after any page generator:  python3 source/layout.py

- One header nav and one footer (with every hub, guide group and area) on every page.
- Speculation rules so the next page is prerendered on hover (near-instant navigation).
- sitemap.xml (every indexable page, with lastmod) and llms.txt rebuilt from the pages themselves.
Idempotent: running it twice gives the same files.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
CONTENT = ROOT / "source" / "content"
SITE = "https://rockfactory.uk"
LASTMOD = "2026-10-07"
CSS_VERSION = "27"

NAV = [("/", "Home"), ("/storage-units-blackpool.html", "Storage"), ("/offices-to-let-blackpool.html", "Offices"),
       ("/workshops-studios-blackpool.html", "Workshops &amp; studios"), ("/compare-units.html", "Prices"),
       ("/storage-guides-blackpool.html", "Guides"), ("/find-us.html", "Find us")]


def content(name):
    p = CONTENT / name
    return json.loads(p.read_text()) if p.exists() else {"hub": None, "pages": []}


def section_of(slug):
    """Which nav item a page belongs to, for aria-current."""
    if slug == "index":
        return "/"
    if slug in ("storage-units-blackpool", "storage-pods-blackpool") or slug.endswith("-unit-blackpool"):
        return "/storage-units-blackpool.html"
    if slug in ("compare-units", "storage-prices-explained", "rental-terms"):
        return "/compare-units.html"
    if slug == "find-us":
        return "/find-us.html"
    guides = {p["slug"] for f in ("storage-guides.json", "business-guides.json", "areas.json") for c in [content(f)]
              for p in ([c["hub"]] if c.get("hub") else []) + c["pages"]}
    if slug in guides or slug.startswith("unit-ideas-") or slug in ("small-business-unit-ideas-blackpool", "glossary", "faqs"):
        return "/storage-guides-blackpool.html"
    return f"/{slug}.html"


def nav_html(slug):
    cur = section_of(slug)
    cur_attr = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur_attr if h == cur else ""}>{t}</a>' for h, t in NAV)
    return f'<nav class="nav" aria-label="Main navigation">{links}</nav>'


def footer_html():
    areas = content("areas.json")
    cols = [
        ("Spaces", [("/storage-units-blackpool.html", "Storage units"), ("/150-sq-ft-unit-blackpool.html", "150 sq ft unit"),
                    ("/160-sq-ft-unit-blackpool.html", "160 sq ft unit"), ("/180-sq-ft-unit-blackpool.html", "180 sq ft unit"),
                    ("/two-storey-unit-blackpool.html", "300 sq ft two-storey unit"), ("/offices-to-let-blackpool.html", "Offices"),
                    ("/workshops-studios-blackpool.html", "Workshops &amp; studios"), ("/storage-pods-blackpool.html", "Storage pods (spring 2027)"),
                    ("/compare-units.html", "Compare units and prices")]),
        ("Guides", [("/storage-guides-blackpool.html", "Storage guides"), ("/what-size-storage-unit.html", "What size do I need?"),
                    ("/business-guides-blackpool.html", "Small business guides"), ("/small-business-unit-ideas-blackpool.html", "Business ideas for a unit"),
                    ("/storage-prices-explained.html", "Prices explained"), ("/faqs.html", "Questions and answers"), ("/glossary.html", "Glossary")]),
        ("Areas", ([(f"/{areas['hub']['slug']}.html", "Fylde coast")] if areas.get("hub") else []) +
                  [(f"/{p['slug']}.html", p["crumb"]) for p in areas["pages"]]),
        ("The Rock Factory", [("/about.html", "About us"), ("/find-us.html", "Find us"), ("/rental-terms.html", "Rental terms"),
                              ("/our-businesses.html", "Our businesses"), ("/blackpool-rock-history.html", "Blackpool rock history")]),
    ]
    cols = [(h, [(u, t) for u, t in links if (PUB / (u.strip("/") or "index.html")).exists()]) for h, links in cols]
    colhtml = "".join(f'<div class="footer-col"><p class="footer-head">{h}</p><ul>' + "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in links) + "</ul></div>"
                      for h, links in cols if links)
    return ('<footer class="site-footer site-footer-mega wrap"><div class="footer-brand"><a class="brand" href="/"><img class="brand-logo" src="/assets/rock-factory-logo.webp" width="640" height="453" alt="The Rock Factory" loading="lazy"><span class="brand-town">Blackpool<br><small>Storage &amp; business space</small></span></a>'
            '<p class="footer-note">The Old Rock Factory, Keswick Road, off Park Road, Blackpool FY1 5PB.<br>WhatsApp <a href="https://wa.me/447366991012">07366 991012</a><br>Prices subject to availability · Minimum term: one month.</p></div>'
            f'<nav class="footer-cols" aria-label="Footer navigation">{colhtml}</nav></footer>')


SPEC = ('<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/assets/*"}}]},"eagerness":"moderate"}]}</script>')


def tidy(path):
    s = path.read_text(); slug = path.stem
    s = re.sub(r'<nav class="nav" aria-label="Main navigation">.*?</nav>', lambda m: nav_html(slug), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer.*?</footer>', lambda m: footer_html(), s, count=1, flags=re.S)
    s = s.replace('src="assets/', 'src="/assets/').replace('srcset="assets/', 'srcset="/assets/').replace(', assets/', ', /assets/')
    s = re.sub(r'href="(?!/|https?:|#|mailto:|data:)([a-z0-9-]+\.html)', r'href="/\1', s)
    s = re.sub(r'/styles\.css\?v=\d+', f'/styles.css?v={CSS_VERSION}', s)
    if "speculationrules" not in s:
        s = s.replace("</head>", f"  {SPEC}\n</head>", 1)
    path.write_text(s)
    return s


def indexable(s):
    return not re.search(r'<meta name="robots" content="[^"]*noindex', s)


ORDER = ["index", "storage-units-blackpool", "offices-to-let-blackpool", "workshops-studios-blackpool", "compare-units",
         "150-sq-ft-unit-blackpool", "160-sq-ft-unit-blackpool", "180-sq-ft-unit-blackpool", "two-storey-unit-blackpool",
         "storage-pods-blackpool", "find-us", "about", "rental-terms", "faqs"]


def main():
    pages = {}
    for f in sorted(PUB.glob("*.html")):
        s = tidy(f)
        if f.stem != "404" and indexable(s):
            pages[f.stem] = s
    slugs = [x for x in ORDER if x in pages] + sorted(x for x in pages if x not in ORDER)
    loc = lambda x: f"{SITE}/" if x == "index" else f"{SITE}/{x}.html"
    (PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{loc(x)}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for x in slugs) + "</urlset>\n")
    # llms.txt: keep the hand-written summary at the top, then list every page with its description.
    llms = PUB / "llms.txt"; head = llms.read_text().split("\n## ")[0].rstrip()
    def line(x):
        t = re.search(r"<title>(.*?)</title>", pages[x]).group(1).split(" | ")[0].replace("&amp;", "&")
        d = re.search(r'<meta name="description" content="([^"]*)"', pages[x]).group(1).replace("&amp;", "&")
        return f"- [{t}]({loc(x)}): {d}"
    groups = [("Spaces and prices", [x for x in slugs if section_of(x) in ("/", "/storage-units-blackpool.html", "/compare-units.html")
                                      or x in ("offices-to-let-blackpool", "workshops-studios-blackpool")]),
              ("About and contact", [x for x in slugs if x in ("about", "find-us", "our-businesses", "icework-web-design-blackpool", "blackpool-rock-history")])]
    used = {x for _, g in groups for x in g}
    groups.append(("Guides", [x for x in slugs if x not in used]))
    body = "".join(f"\n\n## {h}\n\n" + "\n".join(line(x) for x in g) for h, g in groups if g)
    llms.write_text(head + body + "\n")
    print(f"tidied {len(list(PUB.glob('*.html')))} pages, sitemap {len(slugs)} URLs")


if __name__ == "__main__":
    main()
