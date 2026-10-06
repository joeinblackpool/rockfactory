"""Build one page per unit from UNITS below, using the storage page's header and footer.

Run from the repo root:  python3 source/units.py
Photos go in public/assets as <slug>-<n>.webp (plus -800.webp); see add_photo() at the bottom.
"""
import json, re
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://rockfactory.uk"

# Facts from the owner's unit list. Only units with photos get a page.
UNITS = [
    {"slug": "150-sq-ft-unit-blackpool", "size": 150, "price": 65, "title_h1": "ground-floor unit",
     "access": "Roller-shutter access", "storeys": "Ground floor", "short": "Ground floor · roller shutter",
     "about": "A ground-floor unit with roller-shutter access, so loading and unloading is easy. The unit is windowless.",
     "suits": "It suits personal storage, business stock, tools and equipment, or a small workshop (business use needs prior approval).",
     "features": [("150 sq ft ground floor", "A single ground-floor space. The unit is windowless."),
                  ("Roller-shutter access", "Load and unload easily through the roller shutter.")],
     "photos": [], "examples": [("unit-roller-shutter", 1400, 1050, "Example Rock Factory unit with grey floor, white walls, a personnel door and the roller shutter raised"), ("unit-interconnecting-doors", 1400, 1050, "Example Rock Factory unit interior with doors on both sides")]},
    {"slug": "160-sq-ft-unit-blackpool", "size": 160, "price": 69, "title_h1": "ground-floor unit",
     "access": "Security-door access", "storeys": "Ground floor", "short": "Ground floor · security door",
     "about": "A ground-floor unit with a secure security door for access. The unit is windowless.",
     "suits": "It suits personal storage, archive boxes, business stock or a quiet studio or work space (business use needs prior approval).",
     "features": [("160 sq ft ground floor", "A single ground-floor space. The unit is windowless."),
                  ("Security-door access", "Access through a secure security door.")],
     "photos": [], "examples": [("unit-personnel-door", 750, 1000, "Example Rock Factory unit with a grey security door, painted concrete floor and overhead light"), ("unit-interconnecting-doors", 1400, 1050, "Example Rock Factory unit interior with doors on both sides")]},
    {"slug": "180-sq-ft-unit-blackpool", "size": 180, "price": 78, "title_h1": "ground-floor unit",
     "access": "Roller-shutter access", "storeys": "Ground floor", "short": "Ground floor · roller shutter",
     "about": "A larger ground-floor unit with roller-shutter access, so loading and unloading is easy. The unit is windowless.",
     "suits": "It suits bulkier storage, business stock, trades and equipment, or a workshop (business use needs prior approval).",
     "features": [("180 sq ft ground floor", "A single ground-floor space. The unit is windowless."),
                  ("Roller-shutter access", "Load and unload easily through the roller shutter.")],
     "photos": [], "examples": [("unit-roller-shutter", 1400, 1050, "Example Rock Factory unit with grey floor, white walls, a personnel door and the roller shutter raised"), ("unit-interconnecting-doors", 1400, 1050, "Example Rock Factory unit interior with doors on both sides")]},
    {"slug": "two-storey-unit-blackpool", "size": 300, "price": 130, "title_h1": "two-storey unit",
     "access": "Roller-shutter access", "storeys": "Two storeys", "short": "Two storeys · roller shutter · upstairs office with window",
     "about": "Our largest unit: a ground floor with roller-shutter access, plus an upstairs office or storage area with a window. The ground floor is windowless.",
     "suits": "Use the ground floor for stock, equipment or a workshop and the upstairs as an office or extra storage. It suits small businesses that need storage and a desk in one place, makers and trades, or anyone with a lot to store.",
     "features": [("Two storeys, 300 sq ft", "Ground floor plus an upstairs office or storage area with a window, reached by a staircase inside the unit."),
                  ("Roller-shutter access", "Load and unload easily through the roller shutter at the front of the unit.")],
     "photos": [("unit-300-interior-stairs", 1400, 1050, "Inside the 300 sq ft two-storey unit: grey floor, white walls, a dark grey staircase up to the first floor and a grey door"),
                ("unit-300-exterior-shutter", 1030, 1526, "Outside the two-storey unit: Rock Factory sign, first-floor window and a galvanised roller shutter with a security camera above")]},
]

COMMON = [("Connected and secure", "Lighting, electricity and Wi-Fi already connected. Free CCTV app access covering the entrance and the area outside the units, with 24-hour access."),
          ("Shared facilities", "A shared tea and coffee room, shared toilets and water on site. Receive mail and clients at the unit.")]


def img(p, extra):
    name, w, h, alt = p
    if w <= 800:
        return f'<img src="/assets/{name}.webp" width="{w}" height="{h}" alt="{alt}" {extra} decoding="async">'
    return (f'<img srcset="/assets/{name}-800.webp 800w, /assets/{name}.webp {w}w" sizes="(max-width: 800px) 100vw, 50vw" '
            f'src="/assets/{name}.webp" width="{w}" height="{h}" alt="{alt}" {extra} decoding="async">')


def build(u, template):
    url = f"{SITE}/{u['slug']}.html"
    name = f"{u['size']} sq ft {u['title_h1']}"
    title = f"{u['size']} sq ft {u['title_h1'].title().replace('-Floor', '-Floor').replace('Ground-Floor', 'Ground-Floor')}, Blackpool | The Rock Factory"
    title = f"{name[0].upper()}{name[1:]} to rent, Blackpool | The Rock Factory" if len(title) > 60 else title
    desc = (f"{u['size']} sq ft {u['title_h1']} to rent in Blackpool: {u['access'].lower()}, lighting, power and Wi-Fi. "
            f"£{u['price']}/week, available 1 November, first week free if you pre-book.")
    s = template
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x["@type"] == "LocalBusiness")
    photos = u["photos"] or u.get("examples", [])
    example = not u["photos"]
    images = [f"{SITE}/assets/{p[0]}.webp" for p in u["photos"]]
    graph = [biz,
             {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}},
             {"@type": "Offer", "@id": url + "#offer", "name": name, "url": url, "description": f"{u['storeys']}, {u['access'].lower()}",
              "price": str(u["price"]), "priceCurrency": "GBP",
              "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(u["price"]), "priceCurrency": "GBP", "unitText": "week"},
              "availabilityStarts": "2026-11-01", "offeredBy": {"@id": f"{SITE}/#business"}, **({"image": images} if images else {})},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Storage units", "item": f"{SITE}/storage-units-blackpool.html"},
                 {"@type": "ListItem", "position": 3, "name": name, "item": url}]}]
    if u["photos"]:
        p0 = photos[0]
        graph[1]["primaryImageOfPage"] = {"@type": "ImageObject", "url": f"{SITE}/assets/{p0[0]}.webp", "width": p0[1], "height": p0[2]}
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    wa = re.search(r'href="(https://wa\.me/[^"]+)"', s).group(1)

    hero_photo = (f'<figure class="page-photo"><a href="/assets/{photos[0][0]}.webp" target="_blank" rel="noopener noreferrer" '
                  f'aria-label="View the full photograph">{img(photos[0], "fetchpriority=\"high\"")}</a>'
                  + ('<figcaption class="example-tag">Example unit · photos of this unit coming soon</figcaption>' if example else '') + '</figure>')
    gallery = "".join(f'<figure><a href="/assets/{p[0]}.webp" target="_blank" rel="noopener noreferrer" aria-label="View full photograph">'
                      f'{img(p, "loading=\"lazy\"")}</a></figure>' for p in photos)
    feats = "".join(f'<div class="office-feature"><h3>{h}</h3><p>{t}</p></div>' for h, t in u["features"] + COMMON)
    others = [x for x in UNITS if x is not u and (x["photos"] or x.get("examples"))]
    other_links = " · ".join(f'<a class="text-link" href="/{x["slug"]}.html">{x["size"]} sq ft, £{x["price"]} a week</a>' for x in others)
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/storage-units-blackpool.html">Storage units</a> <span aria-hidden="true">/</span> <span aria-current="page">{name}</span></nav>
<section class="page-hero wrap"><div class="page-hero-copy"><p class="eyebrow">{u["short"]}</p><h1>{u["size"]} sq ft<br><em>{u["title_h1"]}</em></h1><p class="intro">{u["about"]} Lighting, electricity and Wi-Fi are already connected. At The Old Rock Factory, Keswick Road, Blackpool.</p><div class="actions"><a class="button" href="{wa}" target="_blank" rel="noopener noreferrer">Pre-book: first week free</a><a class="button secondary" href="#photos">See photos</a></div></div>
<div class="page-visual">{hero_photo}<aside class="price-ticket"><span class="panel-label">{name}</span><strong>£{u["price"]}</strong><span>per week</span><small>Available from 1 November · Pre-book and get your first week free · Minimum term: one month</small></aside></div></section>
<div class="compact-notice"><div class="wrap"><p><strong>Available from 1 November.</strong> Pre-book now and your first week is free. Message us on WhatsApp on 07366 991012.</p></div></div>
<section class="section wrap"><div class="office-details"><div><p class="eyebrow">About this unit</p><h2>{u["size"]} sq ft<br><em>at £{u["price"]} a week</em></h2><p>{u["about"]}</p><p>{u["suits"]}</p><p class="fine-print">Prices are based on the floor area of each unit, per sq ft per week, and are subject to availability. Minimum rental term: one month. Electricity usage is charged separately at the supplier rate, with no markup. Business use needs prior approval. Car storage is not permitted.</p></div>
<div class="office-feature-list">{feats}</div></div></section>
<section class="section wrap" id="photos"><div class="section-head"><h2>{"Example" if example else "Unit"}<br><em>photographs</em></h2><p>{("Photos of this unit are coming soon. These show an example unit at The Old Rock Factory, so layout and access may differ." if example else f"The {name} at The Old Rock Factory, Keswick Road, Blackpool.")}</p></div><div class="photo-gallery natural">{gallery}</div></section>
<section class="section rental-section"><div class="wrap split"><div id="opening" class="opening-card"><p class="eyebrow">Pre-booking offer</p><h3>Available from<br>1 November</h3><p>Pre-book the {name} before it opens and your <strong>first week is free</strong>.</p><a class="button" href="{wa}" target="_blank" rel="noopener noreferrer">Pre-book on WhatsApp</a></div>
<div id="moving-in"><p class="eyebrow">Three simple steps</p><h2>How pre-booking<br><em>works</em></h2><ol class="steps"><li><strong>Message us on WhatsApp</strong><span>Tell us you would like the {name} and what you will use it for. Business activities need prior approval.</span></li><li><strong>Reserve your space</strong><span>We confirm availability. Before you move in you will need one month’s rent in advance, a security deposit equal to one month’s rent, valid government-issued photo ID and a signed Direct Debit mandate.</span></li><li><strong>Move in from 1 November</strong><span>Your first week is free. Minimum term: one month.</span></li></ol></div></div></section>
<section class="section wrap"><div class="section-head"><h2>Other units</h2><p>All units have lighting, electricity and Wi-Fi connected.</p></div><p>{other_links}{" · " if other_links else ""}<a class="text-link" href="/storage-units-blackpool.html">Compare all units</a> · <a class="text-link" href="/offices-to-let-blackpool.html">Offices from £70 a week</a></p></section>
</main>'''
    return s[:s.find("<main")] + main + s[s.find("</main>") + 7:]


def link_pages():
    """Homepage prices table and storage-page cards link to every unit page that exists."""
    built = {u["size"]: u for u in UNITS if u["photos"] or u.get("examples")}
    idx = PUB / "index.html"; s = idx.read_text()
    for u in UNITS:
        row = re.search(rf'<tr><th scope="row">(?:<a [^>]*>)?{u["size"]} sq ft(?:</a>)?</th><td>.*?</td>', s)
        if not row: raise SystemExit(f"homepage row for {u['size']} sq ft not found")
        if u["size"] in built:
            href = f'/{u["slug"]}.html'
            new = (f'<tr><th scope="row"><a href="{href}">{u["size"]} sq ft</a></th>'
                   f'<td><a class="row-link" href="{href}">{u["short"]} <span class="row-more">{"Photos &amp; details" if u["photos"] else "Details"} →</span></a></td>')
        else:
            new = f'<tr><th scope="row">{u["size"]} sq ft</th><td>{u["short"]}</td>'
        s = s[:row.start()] + new + s[row.end():]
    idx.write_text(s)
    st = PUB / "storage-units-blackpool.html"; s = st.read_text()
    for size, u in built.items():
        href = f'/{u["slug"]}.html'
        s = re.sub(rf'<h3>(?:<a href="[^"]*">)?{size} <small>sq ft</small>(?:</a>)?</h3>', f'<h3><a href="{href}">{size} <small>sq ft</small></a></h3>', s, count=1)
    st.write_text(s)
    sm = PUB / "sitemap.xml"; x = sm.read_text()
    for u in built.values():
        loc = f"{SITE}/{u['slug']}.html"
        if loc not in x: x = x.replace("</urlset>", f"  <url><loc>{loc}</loc></url>\n</urlset>")
    sm.write_text(x)


if __name__ == "__main__":
    template = (PUB / "storage-units-blackpool.html").read_text()
    for u in UNITS:
        if not u["photos"]:
            print("using example photos until the owner sends this unit's own:", u["size"], "sq ft")
        (PUB / f"{u['slug']}.html").write_text(build(u, template))
        print("built", u["slug"])
    link_pages()
