"""'Self storage prices in Blackpool compared' page.

Run from the repo root:  python3 source/compare.py
Uses COMPETITORS, SIZES, SHOW_COMPARISON and CHECKED from source/pods.py, so prices live in one place.
Competitors are named factually in the body only (never in the title or meta as if we were them).
The page is only built while SHOW_COMPARISON is True, i.e. after the owner has confirmed every figure.
"""
import importlib.util, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pods", ROOT / "source" / "pods.py")
pods = importlib.util.module_from_spec(spec); spec.loader.exec_module(pods)
PUB = pods.PUB
SITE = "https://rockfactory.uk"
SLUG = "self-storage-prices-blackpool"
# Locations only where confirmed from a public listing.
LOCATIONS = {"Greens Self Storage": "Mowbray Drive, Blackpool FY3"}


def build(pub=PUB):
    out = pub / f"{SLUG}.html"
    sm = pub / "sitemap.xml"; x = sm.read_text(); line = f"  <url><loc>{SITE}/{SLUG}.html</loc></url>\n"
    if not pods.SHOW_COMPARISON:
        if out.exists(): out.unlink()
        sm.write_text(x.replace(line, ""))
        print("comparison off: page not built"); return
    t = (pub / "storage-units-blackpool.html").read_text()
    url = f"{SITE}/{SLUG}.html"
    title = "Self Storage Prices in Blackpool, Compared | The Rock Factory"
    desc = (f"Compare self storage prices in Blackpool by size, checked {pods.CHECKED}. Storage in central Blackpool FY1 "
            "from £10 a week at The Rock Factory, Keswick Road.")
    s = t
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(g for g in json.loads(m.group(1))["@graph"] if g["@type"] == "LocalBusiness")
    graph = [biz,
             {"@type": "Article", "@id": url + "#article", "headline": "Self storage prices in Blackpool, compared", "description": desc,
              "url": url, "inLanguage": "en-GB", "dateModified": "2026-10-06", "author": {"@id": f"{SITE}/#business"},
              "publisher": {"@id": f"{SITE}/#business"}, "isPartOf": {"@id": f"{SITE}/#website"}},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Storage pods", "item": f"{SITE}/storage-pods-blackpool.html"},
                 {"@type": "ListItem", "position": 3, "name": "Blackpool storage prices compared", "item": url}]}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)

    sizes = [25, 35, 50, 75, 100]
    ours = {sz: round(w * 52 / 12) for _, sz, w, _ in pods.SIZES}
    head = "".join(f'<th scope="col">{sz} sq ft</th>' for sz in sizes)
    body = ('<tr class="ours"><th scope="row">The Rock Factory<br><small>Central Blackpool FY1 · first floor, by stairs · guide prices</small></th>'
            + "".join(f"<td>£{ours[sz]}</td>" for sz in sizes) + "</tr>")
    for name, link, note, prices in pods.COMPETITORS:
        loc = LOCATIONS.get(name)
        body += (f'<tr><th scope="row"><a href="{link}" target="_blank" rel="noopener nofollow">{name}</a><br><small>{note}{" · " + loc if loc else ""}</small></th>'
                 + "".join(f"<td>£{prices[sz]:.0f}</td>" if sz in prices else '<td class="na">–</td>' for sz in sizes) + "</tr>")
    all_prices = [p for *_, pr in pods.COMPETITORS for p in pr.values()] + list(ours.values())
    lo, hi = round(min(all_prices)), round(max(all_prices))
    names = ", ".join(c[0] for c in pods.COMPETITORS[:-1]) + " and " + pods.COMPETITORS[-1][0]
    faqs = [
        ("How much does self storage cost in Blackpool?", f"In our comparison, checked on {pods.CHECKED}, monthly prices for 25 to 100 sq ft ranged from about £{lo} to £{hi}. Price depends on size, floor, access and extras such as insurance."),
        ("Is there self storage in central Blackpool?", "Yes. The Rock Factory is at The Old Rock Factory, Keswick Road, off Park Road, Blackpool FY1 5PB. Storage pods and rooms open on the first floor in spring 2027, and ground-floor units are available from 1 November."),
        ("Why is first-floor storage cheaper?", "Ground-floor storage is easier to load, so it usually costs more. First-floor storage reached by stairs suits boxes and items you can carry."),
        ("What else should I compare apart from price?", "Check the minimum term and notice period, deposits, insurance, padlocks, access hours, whether the unit is on the ground floor, and how far it is from you."),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/storage-pods-blackpool.html">Storage pods</a> <span aria-hidden="true">/</span> <span aria-current="page">Blackpool storage prices compared</span></nav>
<section class="wrap guide-hero"><p class="eyebrow">Price guide · Checked {pods.CHECKED}</p><h1>Self storage prices<br><em>in Blackpool, compared</em></h1><p class="intro">Looking for storage in Blackpool? We compared published monthly prices from {names} with our own guide prices, size by size, so you can see what storage costs in Blackpool and where we sit.</p><p class="guide-meta">By The Rock Factory, Blackpool · Updated {pods.CHECKED}</p></section>
<section class="section wrap" style="padding-top:0"><div class="table-wrap"><table class="price-table compare-table"><thead><tr><th scope="col">Monthly price</th>{head}</tr></thead><tbody>{body}</tbody></table></div>
<p class="fine-print">Competitor prices are as published on each provider’s website, checked on {pods.CHECKED}, rounded to the nearest pound. They can change at any time and may not include extras such as insurance, padlocks or offers, so check with the provider. Ours are guide prices for spring 2027, converted at about 4.33 weeks to a month, to be confirmed before opening. – means no comparable size listed.</p></section>
<section class="section wrap guide-body"><div class="guide-content wide">
<h2>Storage in central Blackpool</h2><p>The Rock Factory is at The Old Rock Factory, Keswick Road, off Park Road, Blackpool FY1 5PB, close to the town centre. If you live or work in central Blackpool, that can mean shorter trips every time you drop off or collect.</p>
<ul class="tick-list"><li><strong>Storage pods and rooms</strong> on the first floor from £10 a week, opening spring 2027. <a class="text-link" href="/storage-pods-blackpool.html">Sizes and guide prices</a></li><li><strong>Ground-floor units</strong> from £65 a week for 150 sq ft, available from 1 November, with roller-shutter or security-door access. <a class="text-link" href="/storage-units-blackpool.html">Units and prices</a></li><li>Monthly rent with one month’s notice, swap units any time subject to availability, and no utility deposits.</li></ul>
<h2>How to compare storage prices</h2><ul class="tick-list"><li><strong>Compare the same size.</strong> Prices rise with floor area, so compare 50 sq ft with 50 sq ft.</li><li><strong>Check the floor.</strong> Ground-floor units usually cost more than first-floor storage reached by stairs.</li><li><strong>Weekly or monthly?</strong> A month is about 4.33 weeks, so £20 a week is about £87 a month.</li><li><strong>Add the extras.</strong> Insurance, padlocks, deposits and admin fees can change the real cost.</li><li><strong>Check the terms.</strong> Minimum term, notice period and access hours matter as much as price.</li></ul>
<h2>Questions</h2><div class="faq-list">{faq_html}</div>
<p class="fine-print">The Rock Factory is not connected with any other provider named on this page. Names are used only to identify their published prices.</p>
</div></section>
</main>'''
    s = s[:s.find("<main")] + main + s[s.find("</main>") + 7:]
    out.write_text(s)
    if line not in x: sm.write_text(x.replace("</urlset>", line + "</urlset>"))
    print("built", SLUG)


if __name__ == "__main__":
    build()
