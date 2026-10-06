"""'Our businesses' community directory for tenants at The Rock Factory.

Run from the repo root:  python3 source/community.py
Add a tenant to BUSINESSES only with details the tenant has supplied and agreed to publish.
The page stays noindex (and out of the sitemap) until it lists at least MIN_TO_INDEX businesses,
so search engines never see a near-empty page.
"""
import json, re, urllib.parse
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://rockfactory.uk"
SLUG = "our-businesses"
MIN_TO_INDEX = 3

# name, what they do (one or two sentences), category, website (or ""), extra line (or "")
BUSINESSES = [
]

WA_JOIN = "https://wa.me/447366991012?text=" + urllib.parse.quote(
    "Hi, I'm a Rock Factory tenant and I'd like a free listing on the Our businesses page. "
    "Business name: / What we do: / Website: ")
WA_HIRE = "https://wa.me/447366991012?text=" + urllib.parse.quote(
    "Hi, I'm interested in a unit at The Rock Factory and joining the business community there.")


def card(b):
    name, what, cat, web, extra = b
    link = f'<a class="text-link" href="{web}" target="_blank" rel="noopener">{re.sub(r"^https?://(www\.)?", "", web).rstrip("/")}</a>' if web else ""
    return (f'<article class="biz-card"><p class="eyebrow">{cat}</p><h3>{name}</h3><p>{what}</p>'
            + (f'<p class="biz-extra">{extra}</p>' if extra else "") + (f'<p>{link}</p>' if link else "") + '</article>')


def build():
    t = (PUB / "storage-units-blackpool.html").read_text()
    url = f"{SITE}/{SLUG}.html"
    title = "Our Businesses: Local Firms at The Rock Factory, Blackpool"
    desc = "Meet the small businesses based at The Rock Factory, Keswick Road, Blackpool: local makers, traders and services supporting each other."
    s = t
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    indexable = len(BUSINESSES) >= MIN_TO_INDEX
    s = re.sub(r'(<meta name="robots" content=")[^"]*', lambda m: m.group(1) + ("index, follow, max-image-preview:large" if indexable else "noindex, follow"), s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x["@type"] == "LocalBusiness")
    graph = [biz,
             {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Our businesses", "item": url}]}]
    if BUSINESSES:
        graph.append({"@type": "ItemList", "name": "Businesses at The Rock Factory", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "LocalBusiness", "name": b[0], "description": b[1],
             **({"url": b[3]} if b[3] else {}), "address": biz["address"]}} for i, b in enumerate(BUSINESSES)]})
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)
    wa_join = WA_JOIN.replace("&", "&amp;"); wa_hire = WA_HIRE.replace("&", "&amp;")
    listings = (f'<div class="biz-grid">{"".join(card(b) for b in BUSINESSES)}</div>' if BUSINESSES else
                '<div class="callout"><h3>Our first businesses are moving in</h3><p>The Rock Factory opens on 1 November. As tenants move in, their businesses will appear here so you can find and support them.</p></div>')
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">Our businesses</span></nav>
<section class="wrap guide-hero"><p class="eyebrow">Community · The Old Rock Factory, Keswick Road</p><h1>Our<br><em>businesses</em></h1><p class="intro">The Rock Factory is home to small, independent Blackpool businesses: makers, sellers, trades and services working side by side. Find what they do, use their services, and help keep local businesses growing.</p></section>
<section class="section wrap" style="padding-top:0"><h2 class="sr-only">Businesses based here</h2>{listings}</section>
<section class="section rental-section"><div class="wrap split"><div class="opening-card"><p class="eyebrow">Tenants</p><h3>Get your free listing</h3><p>Every tenant can have a free listing here with a short description and a link to their website. Send us your details on WhatsApp and we will add you.</p><a class="button" href="{wa_join}" target="_blank" rel="noopener noreferrer">Send my details</a></div>
<div><p class="eyebrow">Why it helps</p><h2>Stronger<br><em>together</em></h2><ul class="tick-list"><li><strong>Be found.</strong> A listing and a link from this page help customers find your business.</li><li><strong>Use the address on Google.</strong> Tenants can use The Old Rock Factory, Keswick Road, Blackpool FY1 5PB on their Google Business Profile.</li><li><strong>Work with your neighbours.</strong> Need a website, a sign, a repair or storage? There may be a business a few doors away.</li><li><strong>Meet people.</strong> The shared tea and coffee room is a good place to swap ideas and contacts.</li></ul></div></div></section>
<section class="section wrap"><div class="callout coming"><p class="eyebrow">Want to join them?</p><h3>Units from £65 a week, available 1 November</h3><p>Monthly rent with one month’s notice, swap units any time, no utility deposits, and your first week free if you pre-book. <a class="text-link" href="/#prices">See units and prices</a> or <a class="text-link" href="{wa_hire}" target="_blank" rel="noopener noreferrer">message us on WhatsApp</a>.</p></div></section>
</main>'''
    s = s[:s.find("<main")] + main + s[s.find("</main>") + 7:]
    (PUB / f"{SLUG}.html").write_text(s)
    sm = PUB / "sitemap.xml"; x = sm.read_text()
    line = f"  <url><loc>{url}</loc></url>\n"
    if indexable and url not in x:
        x = x.replace("</urlset>", line + "</urlset>")
    if not indexable:
        x = x.replace(line, "")
    sm.write_text(x)
    print(f"built {SLUG}: {len(BUSINESSES)} businesses, {'indexed' if indexable else 'noindex until ' + str(MIN_TO_INDEX)}")


if __name__ == "__main__":
    build()
