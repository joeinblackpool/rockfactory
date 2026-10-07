"""First-floor storage pods and rooms (opening spring 2027).

Run from the repo root:  python3 source/pods.py
Confirmed by the owner: first floor, small to medium storage pods and rooms, opening spring 2027.
Sizes and prices below are guide prices, always labelled as such, to be confirmed before opening.
Targets "small storage units Blackpool"; the pods and rooms are the small end of the range.
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

# Named price comparison. Monthly prices as published by each provider; CHECKED is the date the owner confirmed
# them on the providers' own websites (keep dated screenshots). Like-for-like note per provider.
SHOW_COMPARISON = False
CHECKED = "6 October 2026"
COMPETITORS = [
    # name, url, floor/notes, {sq ft: monthly £}
    ("21st Century Self Store", "https://www.21stcenturyselfstore.co.uk/", "First floor (prices from 1 May 2026)",
     {35: 54.63, 50: 64.40, 75: 79.35, 100: 99.48}),
    ("Greens Self Storage", "https://www.greensselfstorage.co.uk/availability-pricing-for-greens-self-storage/", "Indoor units",
     {25: 81.12, 50: 118.56, 75: 156.00, 100: 205.92}),
    ("U Store Blackpool", "https://www.comparethestorage.com/self-storage-finder.php?store=U+Store+-+Blackpool", "Listed price",
     {75: 121.33}),
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
    title = "Small Storage Units & Pods Blackpool | The Rock Factory"
    desc = ("Small storage units in Blackpool: pods from 15 sq ft and rooms up to 100 sq ft, guide prices from £10 a week. "
            "Opening spring 2027 at The Old Rock Factory, FY1 5PB.")
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
                 {"@type": "ListItem", "position": 3, "name": "Small storage units", "item": url}]},
             {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                 {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in FAQS]}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    rows = "".join(f'<tr><th scope="row">{k} · {sz} sq ft</th><td>{fit}</td><td class="price">£{w}<small> / week</small><br><small>about £{round(w * 52 / 12)} a month</small></td></tr>' for k, sz, w, fit in SIZES)
    chart = (f'<section class="section wrap" id="prices" aria-labelledby="pod-prices"><div class="section-head"><h2 id="pod-prices">Sizes and<br><em>guide prices</em></h2>'
             '<p>Six sizes, from a small pod to a room. Prices are set around the middle of Blackpool storage prices.</p></div>'
             '<div class="table-wrap"><table class="price-table"><thead><tr><th scope="col">Size</th><th scope="col">What fits</th><th scope="col">Guide price</th></tr></thead>'
             f'<tbody>{rows}</tbody></table></div>'
             '<p class="fine-print">Guide prices for spring 2027, to be confirmed before opening. Sizes and what fits are approximate; how much fits depends on how you pack. First floor, reached by stairs.</p></section>')
    comparison = ""
    if SHOW_COMPARISON:
        sizes = [25, 35, 50, 75, 100]
        ours = {sz: round(w * 52 / 12) for _, sz, w, _ in SIZES}
        head = "".join(f"<th scope=\"col\">{sz} sq ft</th>" for sz in sizes)
        body = '<tr class="ours"><th scope="row">The Rock Factory<br><small>First floor, by stairs · guide prices</small></th>' + "".join(f"<td>£{ours[sz]}</td>" for sz in sizes) + "</tr>"
        for name, link, note, prices in COMPETITORS:
            body += (f'<tr><th scope="row"><a href="{link}" target="_blank" rel="noopener nofollow">{name}</a><br><small>{note}</small></th>'
                     + "".join(f"<td>£{prices[sz]:.0f}</td>" if sz in prices else '<td class="na">–</td>' for sz in sizes) + "</tr>")
        comparison = (f'<section class="section wrap" id="compare" aria-labelledby="compare-title"><div class="section-head"><h2 id="compare-title">How we compare<br><em>in Blackpool</em></h2>'
                      '<p>Monthly prices for similar-sized storage in Blackpool, so you can see where we sit.</p></div>'
                      f'<div class="table-wrap"><table class="price-table compare-table"><thead><tr><th scope="col">Monthly price</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
                      f'<p class="fine-print">Competitor prices are as published on each provider’s website, checked on {CHECKED}, rounded to the nearest pound. They can change at any time and may not include extras such as insurance, padlocks or offers, so check with the provider. Ours are guide prices for spring 2027, about 4.33 weeks to a month, to be confirmed before opening. Our pods and rooms are on the first floor, reached by stairs. – means no comparable size listed. <a class="text-link" href="/self-storage-prices-blackpool.html">Full Blackpool storage price guide</a>.</p></section>')
    smallthinking = ('<section class="section wrap" id="why-small" aria-labelledby="why-small-title"><div class="section-head"><h2 id="why-small-title">Why small<br><em>is the smart buy</em></h2>'
        '<p>Nobody wants storage. They want their spare room back. Here is how to get it for less.</p></div><div class="features">'
        '<div class="feature"><h3>Stop paying to store air</h3><p>Empty floor space costs the same as full floor space. A pod sized to what you own beats a unit sized to what you might own one day.</p></div>'
        '<div class="feature"><h3>The hallway tax</h3><p>Boxes in the hall, bikes in the kitchen, stock on the stairs: you are already paying for storage, in space and patience. A pod moves the cost somewhere you can see it.</p></div>'
        '<div class="feature"><h3>Weekly and monthly, side by side</h3><p>A weekly price can look smaller than it is. We show both, so you budget for the real number and there are no surprises.</p></div>'
        '<div class="feature"><h3>Room to change your mind</h3><p>Start small. If you need more space later, a room or a ground-floor unit is in the same building, subject to availability.</p></div>'
        '<div class="feature"><h3>Keep things, not decisions</h3><p>Storage is brilliant for things you will use again. Sort first, store second, and you will need a smaller pod than you think.</p></div>'
        '<div class="feature"><h3>Honest guide prices</h3><p>Pod and room prices are guide prices, set around the middle of Blackpool storage prices, and we will confirm them before we open.</p></div>'
        '</div><p class="fine-print">More help: <a class="text-link" href="/cheap-storage-blackpool.html">how to get cheap storage in Blackpool</a>, '
        '<a class="text-link" href="/self-storage-blackpool.html">how self storage works here</a> and '
        '<a class="text-link" href="/short-term-storage-blackpool.html">short-term storage for moves and renovations</a>.</p></section>')
    uses = "".join(f'<div class="feature"><h3>{h}</h3><p>{p}</p></div>' for h, p in USES)
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQS)
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/storage-units-blackpool.html">Storage units</a> <span aria-hidden="true">/</span> <span aria-current="page">Small storage units</span></nav>
<section class="page-hero wrap"><div class="page-hero-copy"><p class="eyebrow">First floor · From £10 a week · Opening spring 2027</p><h1>Small storage units<br><em>in Blackpool</em></h1><p class="intro">Storage pods and rooms from 15 to 100 sq ft are coming to the first floor of The Old Rock Factory, Keswick Road, Blackpool. For the boxes, furniture and stock that do not need a whole unit, at a price that does not feel like one.</p><div class="actions"><a class="button" href="{WA_H}" target="_blank" rel="noopener noreferrer">Register interest on WhatsApp</a><a class="button secondary" href="#prices">Sizes and prices</a></div></div>
<div class="page-visual"><figure class="page-photo"><img srcset="/assets/unit-300-exterior-shutter-800.webp 800w, /assets/unit-300-exterior-shutter.webp 1030w" sizes="(max-width: 800px) 100vw, 50vw" src="/assets/unit-300-exterior-shutter.webp" width="1030" height="1526" alt="The Rock Factory sign on the building at The Old Rock Factory, Keswick Road, Blackpool" fetchpriority="high" decoding="async"><figcaption class="example-tag">The Old Rock Factory, Keswick Road</figcaption></figure><aside class="price-ticket"><span class="panel-label">First-floor storage pods and rooms</span><strong>Spring 2027</strong><span>pods from £10 a week, rooms from £22</span><small>Register your interest on WhatsApp: 07366 991012</small></aside></div></section>
<div class="compact-notice"><div class="wrap"><p><strong>Opening spring 2027.</strong> Pods from £10 a week and rooms from £22 a week on the first floor, reached by stairs. Register your interest to hear first when bookings open.</p></div></div>
{chart}{comparison}{smallthinking}<section class="section wrap"><div class="section-head"><h2>What people<br><em>store in a pod</em></h2><p>A storage pod or room is a simple, secure space for things you want to keep but do not want at home or in your shop.</p></div><div class="features">{uses}</div></section>
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
