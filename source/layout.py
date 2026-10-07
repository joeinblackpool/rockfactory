"""Site-wide tidy-up, run LAST after any page generator:  python3 source/layout.py

- One header nav and one footer (with every hub, guide group and area) on every page.
- Speculation rules so the next page is prerendered on hover (near-instant navigation).
- sitemap.xml (every indexable page, with lastmod) and llms.txt rebuilt from the pages themselves.
Idempotent: running it twice gives the same files.
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
CONTENT = ROOT / "source" / "content"
SITE = "https://rockfactory.uk"
LASTMOD = "2026-10-07"
CSS_VERSION = "41"

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
                    ("/workshops-studios-blackpool.html", "Workshops &amp; studios"), ("/storage-pods-blackpool.html", "Small storage units"), ("/self-storage-blackpool.html", "Self storage Blackpool"),
                    ("/compare-units.html", "Compare units and prices")]),
        ("Guides", [("/storage-guides-blackpool.html", "Storage guides"), ("/what-size-storage-unit.html", "What size do I need?"), ("/cheap-storage-blackpool.html", "Cheap storage tips"), ("/short-term-storage-blackpool.html", "Short-term storage"),
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


# Photo descriptions written for each page they appear on (same file, page-specific wording).
# Keyed by page and the photo's position in <main>. Applied last, so regenerating a page never loses them.
IMAGE_ALT = {
    "index": [
        "Storage and business unit to rent in Blackpool: empty ground-floor unit with lighting, a personnel door and its roller shutter open",
        "Archive black-and-white photograph of a little girl biting a stick of Blackpool rock",
        "Archive black-and-white photograph of seaside rock being made by hand on a rock factory floor",
        "The end of a red stick of Blackpool rock, with Blackpool Rock lettered right through its white centre",
        "Archive photograph of rock-makers in white caps rolling a giant boil of rock by hand",
        "Long pink and blue twists of rock being rolled by hand on a rock factory table",
        "A rainbow stick of rock held up in front of Blackpool Tower on a sunny day",
        "Pink sticks of Blackpool rock in Blackpool Rock wrappers",
        "Vintage yellow rock-shop sign reading Direct from the Factory, Cut Price Rock",
    ],
    "storage-units-blackpool": [
        "Storage unit to rent in Blackpool with its roller shutter open and overhead lighting, at The Rock Factory on Keswick Road",
        "Blackpool storage unit with a personnel door, painted concrete floor and overhead light",
        "Adjoining storage units in Blackpool with personnel doors on both sides, so two units can be rented side by side",
        "Clean, empty storage unit in Blackpool with lighting and an access door, ready for personal or business storage",
        "Ground-floor storage unit at The Rock Factory, Blackpool, with its roller shutter raised for easy loading",
    ],
    "150-sq-ft-unit-blackpool": [
        "Inside the 150 sq ft ground-floor storage unit to rent in Blackpool: grey painted floor, white walls, overhead light and a dark grey door",
        "The 150 sq ft storage unit at The Rock Factory, Blackpool, empty and ready to move into, with lighting already fitted",
        "Roller-shutter entrance to the 150 sq ft storage unit on Keswick Road, Blackpool, set in a white rendered wall",
    ],
    "160-sq-ft-unit-blackpool": [
        "Inside the 160 sq ft ground-floor storage unit in Blackpool: grey floor, white walls, overhead light and a grey internal door",
        "The 160 sq ft storage unit at The Rock Factory, Blackpool, empty with lighting already connected",
        "Steel security door with a lever handle and lock on the 160 sq ft storage unit, Keswick Road, Blackpool",
    ],
    "180-sq-ft-unit-blackpool": [
        "Inside the 180 sq ft ground-floor storage unit in Blackpool, looking out through the raised roller shutter onto the lane",
        "The 180 sq ft storage unit at The Rock Factory, Blackpool: grey floor, white walls and a grey door beside the roller shutter",
        "Galvanised roller shutter on the 180 sq ft storage unit at The Old Rock Factory, Keswick Road, Blackpool",
    ],
    "two-storey-unit-blackpool": [
        "Inside the 300 sq ft two-storey unit to rent in Blackpool: grey floor, white walls and a staircase up to the first-floor room",
        "Staircase to the upstairs office or storage room in the 300 sq ft two-storey unit at The Rock Factory, Blackpool",
        "Outside the two-storey unit in Blackpool: Rock Factory sign, first-floor window and a galvanised roller shutter with a security camera above",
    ],
    "workshops-studios-blackpool": [
        "Workshop space to rent in Blackpool: grey unit with overhead lighting and personnel doors on both sides",
        "Unit being prepared for approved workshop and artist studio use at The Rock Factory, Blackpool",
        "Small workshop unit in Blackpool with a personnel door, painted concrete floor and overhead light",
        "Adjoining workshop units in Blackpool with personnel doors on both sides, for a larger studio or workshop",
        "Studio space to rent in Blackpool with lighting and an access door, ready to fit out",
        "Workshop unit with its roller shutter raised for loading tools and materials, The Rock Factory, Blackpool",
    ],
    "offices-to-let-blackpool": [
        "Small office to let in Blackpool being refurbished at The Rock Factory: a decorator painting the walls, a desk under dust sheets and a sign reading Offices under construction, available from Jan 2027",
    ],
}


def main_images(s):
    m = re.search(r"<main.*?</main>", s, re.S)
    return re.findall(r"<img[^>]*>", m.group(0)) if m else []


def apply_image_seo(s, slug):
    """Page-specific alt text, matching 'view full photograph' labels, and the page's main image in its structured data."""
    m = re.search(r"<main.*?</main>", s, re.S)
    if not m:
        return s
    main, alts, i = m.group(0), IMAGE_ALT.get(slug, []), [0]
    if alts and len(re.findall(r"<img[^>]*>", main)) != len(alts):
        print(f"  ! {slug}: photo count changed, page-specific alt text not applied; update IMAGE_ALT")
        alts = []
    def one(mm):
        a, img = mm.group(1) or "", mm.group(2)
        k = i[0]; i[0] += 1
        if k < len(alts):
            alt = html.escape(alts[k], quote=True)
            img = re.sub(r'alt="[^"]*"', f'alt="{alt}"', img, count=1)
            a = re.sub(r'aria-label="View (?:the )?full photograph[^"]*"', f'aria-label="View full photograph: {alt}"', a)
        return a + img
    main = re.sub(r'(<a [^>]*>)?(<img[^>]*>)', one, main)
    s = s[:m.start()] + main + s[m.end():]
    imgs = main_images(s)
    j = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if imgs and j:
        first = imgs[0]
        src = re.search(r'src="([^"]+)"', first).group(1)
        w, h = re.search(r'width="(\d+)"', first), re.search(r'height="(\d+)"', first)
        alt = html.unescape(re.search(r'alt="([^"]*)"', first).group(1))
        data = json.loads(j.group(1))
        for node in data.get("@graph", []):
            if node.get("@type") in ("WebPage", "Article", "CollectionPage", "AboutPage", "ContactPage") and "url" in node:
                node["primaryImageOfPage"] = {"@type": "ImageObject", "url": SITE + src, "caption": alt,
                                              **({"width": int(w.group(1)), "height": int(h.group(1))} if w and h else {})}
                break
        s = s[:j.start(1)] + json.dumps(data, ensure_ascii=False) + s[j.end(1):]
    return s


def business_type(s):
    """The site's own business is a self-storage facility (it also lets offices and workshops): use schema.org SelfStorage,
    a LocalBusiness subtype, so search engines file it under storage. Other businesses on the page keep their own types."""
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not m:
        return s
    data = json.loads(m.group(1))
    for node in data.get("@graph", []):
        if node.get("@id", "").endswith("/#business"):
            node["@type"] = "SelfStorage"
    return s[:m.start(1)] + json.dumps(data, ensure_ascii=False) + s[m.end(1):]


def add_faq_schema(s):
    """Add FAQPage structured data from the visible questions on any page that has them and lacks it."""
    if 'class="faq-list"' not in s or '"FAQPage"' in s:
        return s
    qa = []
    for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", s, re.S):
        strip = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
        qa.append({"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}})
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not qa or not m:
        return s
    data = json.loads(m.group(1))
    url = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    data.setdefault("@graph", []).append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": qa})
    return s[:m.start(1)] + json.dumps(data, ensure_ascii=False) + s[m.end(1):]


def tidy(path):
    s = path.read_text(); slug = path.stem
    s = re.sub(r'<nav class="nav" aria-label="Main navigation">.*?</nav>', lambda m: nav_html(slug), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer.*?</footer>', lambda m: footer_html(), s, count=1, flags=re.S)
    s = s.replace('src="assets/', 'src="/assets/').replace('srcset="assets/', 'srcset="/assets/').replace(', assets/', ', /assets/')
    s = re.sub(r'href="(?!/|https?:|#|mailto:|data:)([a-z0-9-]+\.html)', r'href="/\1', s)
    s = re.sub(r'/styles\.css\?v=\d+', f'/styles.css?v={CSS_VERSION}', s)
    s = re.sub(r'\s*<script src="/motion\.js[^"]*" defer></script>', '', s)
    s = s.replace("</head>", f'  <script src="/motion.js?v={CSS_VERSION}" defer></script>\n</head>', 1)
    pre = '<link rel="preload" href="/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
    for f in ("jost-latin-wght.woff2", "yellowtail-latin-400.woff2"):
        tag = f'<link rel="preload" href="/fonts/{f}" as="font" type="font/woff2" crossorigin>'
        if tag not in s and pre in s:
            s = s.replace(pre, pre + "\n  " + tag, 1)
    s = add_faq_schema(s)
    s = apply_image_seo(s, slug)
    s = business_type(s)
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
    def imgs(x):
        srcs = list(dict.fromkeys(re.search(r'src="([^"]+)"', i).group(1) for i in main_images(pages[x])))
        return "".join(f"<image:image><image:loc>{SITE}{u}</image:loc></image:image>" for u in srcs if u.startswith("/assets/"))
    (PUB / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                     'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                                     + "".join(f"  <url><loc>{loc(x)}</loc><lastmod>{LASTMOD}</lastmod>{imgs(x)}</url>\n" for x in slugs) + "</urlset>\n")
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
