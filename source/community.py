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
MIN_TO_INDEX = 2

# name, what they do (one or two sentences), category, website (or ""), extra line (or ""), profile page slug (or "")
BUSINESSES = [
    ("IceWork", "Web design, SEO and hosting for small businesses in Blackpool and the Fylde coast. Three-page websites with a domain name and a year of hosting included.",
     "Web design · SEO", "https://icework.co.uk/", "Rock Factory tenants: a complete website package for £200 (usually £350).", "icework-web-design-blackpool"),
    ("Blackpool Building Services", "Building services in Blackpool. More details coming soon.", "Building services", "", "", ""),
]

WA_JOIN = "https://wa.me/447366991012?text=" + urllib.parse.quote(
    "Hi, I'm a Rock Factory tenant and I'd like a free listing on the Our businesses page. "
    "Business name: / What we do: / Website: ")
WA_HIRE = "https://wa.me/447366991012?text=" + urllib.parse.quote(
    "Hi, I'm interested in a unit at The Rock Factory and joining the business community there.")


def card(b):
    name, what, cat, web, extra, prof = b
    link = f'<a class="text-link" href="{web}" target="_blank" rel="noopener">{re.sub(r"^https?://(www\.)?", "", web).rstrip("/")}</a>' if web else ""
    return (f'<article class="biz-card"><p class="eyebrow">{cat}</p><h3>{name}</h3><p>{what}</p>'
            + (f'<p class="biz-extra">{extra}</p>' if extra else "") + (f'<p><a class="row-more" href="/{prof}.html">About {name} →</a></p>' if prof else "")
            + (f'<p>{link}</p>' if link else "") + '</article>')


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


def icework_page():
    """Profile page for IceWork (tenant). Facts from IceWork's own site and the owner: £350 3-page package,
    SEO for 10 search terms, domain + first year of hosting, Get on Google package free in 2026,
    logos from £50, email-first, reply within 24 hours; £200 package price for Rock Factory tenants."""
    t = (PUB / "storage-units-blackpool.html").read_text()
    slug = "icework-web-design-blackpool"; url = f"{SITE}/{slug}.html"
    title = "IceWork Web Design Blackpool | The Rock Factory"
    desc = "IceWork builds £350 websites for Blackpool businesses from The Rock Factory, Keswick Road. Rock Factory tenants get the full website package for £200."
    s = t
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x["@type"] == "LocalBusiness")
    ice = {"@type": "ProfessionalService", "@id": url + "#icework", "name": "IceWork", "url": "https://icework.co.uk/",
           "email": "iceworks@f1rst.co.uk", "description": "Web design, SEO and hosting for small businesses in Blackpool and the Fylde coast.",
           "address": biz["address"], "areaServed": [{"@type": "City", "name": n} for n in ["Blackpool", "Lytham St Annes", "Poulton-le-Fylde", "Thornton-Cleveleys", "Fleetwood", "Preston"]],
           "makesOffer": [{"@type": "Offer", "name": "3-page website package", "price": "350", "priceCurrency": "GBP",
                           "description": "3-page website, SEO for 10 search terms, domain name and first year of hosting"},
                          {"@type": "Offer", "name": "3-page website package for Rock Factory tenants", "price": "200", "priceCurrency": "GBP",
                           "eligibleCustomerType": "Rock Factory tenants"}]}
    graph = [biz, ice,
             {"@type": "ProfilePage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "isPartOf": {"@id": f"{SITE}/#website"}, "mainEntity": {"@id": url + "#icework"}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Our businesses", "item": f"{SITE}/{SLUG}.html"},
                 {"@type": "ListItem", "position": 3, "name": "IceWork", "item": url}]}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)
    mail = "mailto:iceworks@f1rst.co.uk?subject=" + urllib.parse.quote("Rock Factory tenant website (£200)")
    L = lambda path, text: f'<a class="text-link" href="https://icework.co.uk{path}" target="_blank" rel="noopener">{text}</a>'
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/{SLUG}.html">Our businesses</a> <span aria-hidden="true">/</span> <span aria-current="page">IceWork</span></nav>
<section class="wrap guide-hero"><p class="eyebrow">Our businesses · Web design · SEO</p><h1>IceWork<br><em>web design in Blackpool</em></h1><p class="intro">IceWork is a small web development business based at The Rock Factory on Keswick Road. It builds fast, simple websites for Blackpool and Fylde coast businesses, and helps them get found on Google.</p><div class="actions"><a class="button" href="{mail}">Email IceWork</a><a class="button secondary" href="https://icework.co.uk/" target="_blank" rel="noopener">Visit icework.co.uk</a></div></section>
<section class="section wrap" style="padding-top:0"><div class="cta-band tenant-offer"><div class="cta-inner"><div><p class="eyebrow">Tenant offer</p><h2>A website for<br>£200</h2><p>Every Rock Factory tenant can have IceWork’s complete website package for <strong>£200</strong> instead of £350. Move in, and get your business online from the same building.</p></div>
<ul class="tick-list offer-list"><li>A 3-page website, fully built</li><li>SEO for your top 10 search terms</li><li>Your domain name included</li><li>A full year of hosting included</li><li>No hidden fees</li></ul></div></div></section>
<section class="section wrap guide-body"><div class="guide-content wide">
<h2>What IceWork does</h2>
<div class="features"><div class="feature"><h3>Web design</h3><p>Fast, mobile-friendly websites for small businesses, built around the jobs you want more of. {L("/web-design", "Web design")}</p></div>
<div class="feature"><h3>SEO and Google</h3><p>Help to get found on Google and Bing, from search terms to your Google Business Profile. {L("/seo", "SEO")}</p></div>
<div class="feature"><h3>Hosting and care</h3><p>Your domain and a year of hosting come with the website package, so there is nothing else to set up. {L("/pricing", "Pricing")}</p></div>
<div class="feature"><h3>Hotel and guest house sites</h3><p>Websites for Blackpool hotels, guest houses and B&amp;Bs, with links to the booking system you already use. {L("/blackpool-hotel-web-design", "Hotel websites")}</p></div>
<div class="feature"><h3>Branding and logos</h3><p>Logos from £50, plus brand kits for new businesses. {L("/branding", "Branding")}</p></div>
<div class="feature"><h3>Free SEO checker</h3><p>Check how your current website scores for search, free and with no sign-up. {L("/seo-checker", "SEO checker")}</p></div></div>
<h2>Free “Get on Google” package in 2026</h2><p>Through 2026, IceWork’s Get on Google SEO package is free with a website: your site submitted to Google and Bing, your key pages sent for indexing, and your Google Business Profile set up so you can appear on Google Maps. Rock Factory tenants can use The Old Rock Factory, Keswick Road, Blackpool FY1 5PB as their address on Google.</p>
<h2>Why a Rock Factory business needs a website</h2><p>Most customers in Blackpool look for local services on their phone before they pick up the phone or visit. A simple website with your services, prices and location, plus a Google Business Profile, means people searching for what you do in Blackpool, Lytham St Annes, Poulton-le-Fylde, Thornton-Cleveleys or Fleetwood can find you, see you are a real local business and get in touch.</p><p>Having IceWork in the same building makes it easy: pop in, show them what you do, and they can photograph your unit and your work for the site.</p>
<h2>How to get your £200 website</h2><ol class="steps"><li><span><strong>Email IceWork</strong> at <a class="text-link" href="{mail}">iceworks@f1rst.co.uk</a> and say you are a Rock Factory tenant. IceWork prefers email and aims to reply within 24 hours.</span></li><li><span><strong>Tell them about your business:</strong> what you do, the areas you cover and the jobs you want more of.</span></li><li><span><strong>Go live</strong> with your 3-page website, domain name and a year of hosting, then add your Google Business Profile with the Rock Factory address.</span></li></ol>
<h2>Questions</h2><div class="faq-list">
<details><summary>How much is a website for a Rock Factory tenant?</summary><p>£200 for IceWork’s complete 3-page website package, which is usually £350. It includes the build, SEO for your top 10 search terms, your domain name and a full year of hosting.</p></details>
<details><summary>Do I have to be a tenant to use IceWork?</summary><p>No. IceWork builds websites for businesses across Blackpool and the Fylde coast for £350. The £200 price is for Rock Factory tenants.</p></details>
<details><summary>Can IceWork set up my Google Business Profile?</summary><p>Yes. It is part of the Get on Google package, which is free in 2026. Tenants can use the Rock Factory address on their profile.</p></details>
<details><summary>How do I contact IceWork?</summary><p>By email at iceworks@f1rst.co.uk. IceWork prefers email so it can focus on building websites, and aims to reply within 24 hours.</p></details></div>
<p class="fine-print">IceWork is an independent business based at The Rock Factory. Prices and the free Get on Google package are IceWork’s; the £200 tenant price applies to Rock Factory tenants. See {L("/pricing", "icework.co.uk/pricing")} for full details.</p>
<h2>More from The Rock Factory</h2><p><a class="text-link" href="/{SLUG}.html">All our businesses</a> · <a class="text-link" href="/#prices">Units and prices</a> · <a class="text-link" href="/small-business-unit-ideas-blackpool.html">30 business ideas for a small unit</a></p>
</div></section>
</main>'''
    s = s[:s.find("<main")] + main + s[s.find("</main>") + 7:]
    (PUB / f"{slug}.html").write_text(s)
    sm = PUB / "sitemap.xml"; x = sm.read_text()
    if url not in x:
        x = x.replace("</urlset>", f"  <url><loc>{url}</loc></url>\\n</urlset>")
    sm.write_text(x)
    print("built", slug)


if __name__ == "__main__":
    build()
    icework_page()
