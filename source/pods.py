"""First-floor storage pods and rooms (opening spring 2027).

Run from the repo root:  python3 source/pods.py
Confirmed by the owner: first floor, small to medium storage pods and rooms, opening spring 2027.
Sizes, prices and access details are still to be confirmed, so none are stated.
"""
import json, re, urllib.parse
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://rockfactory.uk"
SLUG = "storage-pods-blackpool"
WA = "https://wa.me/447366991012?text=" + urllib.parse.quote(
    "Hi, please add me to the list for a first-floor storage pod or room at The Rock Factory (spring 2027). I need roughly: ")
WA_H = WA.replace("&", "&amp;")

# Guide prices set at the Blackpool middle for first-floor storage (October 2026 research: 21st Century Self
# Storage first-floor rates, Greens Self Storage, U Store, Storage King and published Blackpool guides; SSA UK 2025
# averages of £29.13 per sq ft per year nationally and £20.44 in the North). To be confirmed before opening.
SIZES = [
    ("Pod", 15, 10, "Roughly 30 to 40 boxes, or the contents of a large cupboard."),
    ("Pod", 25, 14, "Boxes plus a few pieces of furniture, such as a bed and a chest of drawers."),
    ("Pod", 35, 17, "Roughly the contents of a studio or small one-bedroom flat."),
    ("Room", 50, 22, "Roughly the contents of a one-bedroom flat, or a small business's stock."),
    ("Room", 75, 28, "Roughly the contents of a two-bedroom home."),
    ("Room", 100, 34, "Roughly the contents of a two to three-bedroom home."),
]

USES = [
    ("Household storage", "Furniture, boxes and belongings while you move house, renovate or declutter."),
    ("Students and seasonal items", "Belongings over the summer, or bikes, garden furniture, decorations and sports kit out of season."),
    ("Business archives", "Boxed records and paperwork you need to keep but not in your office."),
    ("Stock for small businesses", "Light stock for online sellers and market traders who do not need a ground-floor unit."),
    ("Hobby and collection storage", "Craft supplies, collections, records and books kept safe and organised."),
    ("Tools and equipment", "Hand tools, event kit and equipment that fits in a smaller space."),
]

FAQS = [
    ("When do the storage pods open?", "Spring 2027. Register your interest on WhatsApp and we will message you as soon as dates, sizes and prices are confirmed."),
    ("Where are the storage pods?", "On the first floor of The Old Rock Factory, Keswick Road, off Park Road, Blackpool FY1 5PB."),
    ("What sizes and prices will there be?", "Pods of 15, 25 and 35 sq ft from £10 a week, and rooms of 50, 75 and 100 sq ft from £22 a week. These are guide prices, set around the middle of Blackpool storage prices, and will be confirmed before we open."),
    ("How do I get to the first floor?", "By stairs. The pods and rooms suit boxes and items you can carry. For heavy or bulky items, our ground-floor units with roller-shutter access may suit you better."),
    ("I need storage before spring 2027. What can I do?", "Our ground-floor units are available from 1 November, from £65 a week for 150 sq ft, with roller-shutter or security-door access. Pre-book and your first week is free."),
    ("What can't I store?", "Nothing that is flammable, such as fuel, gas cylinders or solvents, and no cars. Low-risk items such as furniture, boxes, paper, fabric and dry goods are fine."),
]


def build():
    t = (PUB / "storage-units-blackpool.html").read_text()
    url = f"{SITE}/{SLUG}.html"
    title = "Storage Pods & Rooms Blackpool, Spring 2027 | The Rock Factory"
    title = "Storage Pods & Rooms Blackpool | The Rock Factory"
    desc = ("First-floor storage pods from £10 a week and rooms from £22 a week, opening spring 2027 at The Old Rock Factory, "
            "Keswick Road, Blackpool FY1 5PB. 15 to 100 sq ft.")
    s = t
    s = re.sub(r"<title>.*?</title>", f"<title>{title.replace('&', '&amp;')}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title.replace("&", "&amp;"), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x["@type"] == "LocalBusiness")
    graph = [biz,
             {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Storage units", "item": f"{SITE}/storage-units-blackpool.html"},
                 {"@type": "ListItem", "position": 3, "name": "Storage pods and rooms", "item": url}]}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    rows = "".join(f'<tr><th scope="row">{k} · {sz} sq ft</th><td>{fit}</td><td class="price">£{w}<small> / week</small><br><small>about £{round(w * 52 / 12)} a month</small></td></tr>' for k, sz, w, fit in SIZES)
    chart = (f'<section class="section wrap" id="prices" aria-labelledby="pod-prices"><div class="section-head"><h2 id="pod-prices">Sizes and<br><em>guide prices</em></h2>'
             '<p>Six sizes, from a small pod to a room. Prices are set around the middle of Blackpool storage prices.</p></div>'
             '<div class="table-wrap"><table class="price-table"><thead><tr><th scope="col">Size</th><th scope="col">What fits</th><th scope="col">Guide price</th></tr></thead>'
             f'<tbody>{rows}</tbody></table></div>'
             '<p class="fine-print">Guide prices for spring 2027, to be confirmed before opening. Sizes and what fits are approximate; how much fits depends on how you pack. First floor, reached by stairs.</p></section>')
    uses = "".join(f'<div class="feature"><h3>{h}</h3><p>{p}</p></div>' for h, p in USES)
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQS)
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/storage-units-blackpool.html">Storage units</a> <span aria-hidden="true">/</span> <span aria-current="page">Storage pods and rooms</span></nav>
<section class="page-hero wrap"><div class="page-hero-copy"><p class="eyebrow">First floor · From £10 a week · Opening spring 2027</p><h1>Storage pods<br><em>and rooms</em></h1><p class="intro">Small to medium storage pods and rooms are coming to the first floor of The Old Rock Factory, Keswick Road, Blackpool. Ideal when you need somewhere safe for boxes, furniture or stock, but not a whole unit.</p><div class="actions"><a class="button" href="{WA_H}" target="_blank" rel="noopener noreferrer">Register interest on WhatsApp</a><a class="button secondary" href="#prices">Sizes and prices</a></div></div>
<div class="page-visual"><figure class="page-photo"><img srcset="/assets/unit-300-exterior-shutter-800.webp 800w, /assets/unit-300-exterior-shutter.webp 1030w" sizes="(max-width: 800px) 100vw, 50vw" src="/assets/unit-300-exterior-shutter.webp" width="1030" height="1526" alt="The Rock Factory sign on the building at The Old Rock Factory, Keswick Road, Blackpool" fetchpriority="high" decoding="async"><figcaption class="example-tag">The Old Rock Factory, Keswick Road</figcaption></figure><aside class="price-ticket"><span class="panel-label">First-floor storage pods and rooms</span><strong>Spring 2027</strong><span>pods from £10 a week, rooms from £22</span><small>Register your interest on WhatsApp: 07366 991012</small></aside></div></section>
<div class="compact-notice"><div class="wrap"><p><strong>Opening spring 2027.</strong> Pods from £10 a week and rooms from £22 a week on the first floor, reached by stairs. Register your interest to hear first when bookings open.</p></div></div>
{chart}<section class="section wrap"><div class="section-head"><h2>What people<br><em>store in a pod</em></h2><p>A storage pod or room is a simple, secure space for things you want to keep but do not want at home or in your shop.</p></div><div class="features">{uses}</div></section>
<section class="section wrap"><div class="office-details"><div><p class="eyebrow">Pod, room or unit?</p><h2>Choose the right<br><em>size of space</em></h2><p><strong>Storage pods</strong> suit boxes, a few pieces of furniture and smaller items.</p><p><strong>Storage rooms</strong> give you more room for the contents of a flat, larger furniture or business stock.</p><p><strong>Ground-floor units</strong> from 150 sq ft suit bulky or heavy items, trades and small businesses, with roller-shutter or security-door access. They are available from 1 November.</p></div>
<div class="office-feature-list"><div class="office-feature"><h3>First floor, by stairs</h3><p>The pods and rooms are on the first floor of The Old Rock Factory, reached by stairs. If you need to move heavy or bulky items, a ground-floor unit may suit you better.</p></div><div class="office-feature"><h3>Central Blackpool</h3><p>Keswick Road, off Park Road, Blackpool FY1 5PB.</p></div><div class="office-feature"><h3>Hear first</h3><p>Tell us roughly how much you need to store and we will message you when sizes and prices are confirmed.</p></div></div></div></section>
<section class="section rental-section" id="sooner"><div class="wrap split"><div class="opening-card"><p class="eyebrow">Need space sooner?</p><h3>Ground-floor units<br>from 1 November</h3><p>From £65 a week for 150 sq ft. Monthly rent with one month’s notice, swap units any time, no utility deposits, and your <strong>first week free</strong> if you pre-book.</p><a class="button" href="/storage-units-blackpool.html">See units and prices</a></div>
<div><p class="eyebrow">Available to pre-book now</p><h2>Units from<br><em>£65 a week</em></h2><ol class="steps"><li><strong><a href="/150-sq-ft-unit-blackpool.html">150 sq ft · £65 a week</a></strong><span>Ground floor, roller-shutter access.</span></li><li><strong><a href="/160-sq-ft-unit-blackpool.html">160 sq ft · £69 a week</a></strong><span>Ground floor, security-door access.</span></li><li><strong><a href="/180-sq-ft-unit-blackpool.html">180 sq ft · £78 a week</a></strong><span>Ground floor, roller-shutter access.</span></li><li><strong><a href="/two-storey-unit-blackpool.html">300 sq ft · £130 a week</a></strong><span>Two storeys, roller shutter, upstairs office or storage area with a window.</span></li></ol></div></div></section>
<section class="section faq-section"><div class="wrap faq-layout"><div><p class="eyebrow">Storage pods</p><h2>Common<br>questions</h2></div><div class="faq-list">{faqs}</div></div></section>
</main>'''
    s = s[:s.find("<main")] + main + s[s.find("</main>") + 7:]
    (PUB / f"{SLUG}.html").write_text(s)
    print("built", SLUG, len(title))


if __name__ == "__main__":
    build()
