"""Guides, area pages and core pages from the JSON files in source/content/.

Run from the repo root:  python3 source/guides.py   (then python3 source/layout.py)
Each content file holds {"hub": PAGE or null, "pages": [PAGE, ...]}; the format and the facts the copy
may use are in source/content/BRIEF.md. industries.json is read by ideas.py, not here.
"""
import json, re, urllib.parse
from pathlib import Path
from ideas import crumbs_html, faq_html

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
CONTENT = ROOT / "source" / "content"
SITE = "https://rockfactory.uk"
UPDATED = ("2026-10-07", "October 2026")
WA = "https://wa.me/447366991012?text=" + urllib.parse.quote("Hi, I have a question about a space at The Rock Factory.")
WA_H = WA.replace("&", "&amp;")
FILES = ["core.json", "storage-guides.json", "business-guides.json", "areas.json"]
ORG = {"@id": f"{SITE}/#business"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load():
    clusters = []
    for f in FILES:
        p = CONTENT / f
        if p.exists():
            clusters.append(json.loads(p.read_text()))
    return clusters


def page_names(clusters):
    """slug -> (short name, description) for related-page cards, from content files and existing pages."""
    names = {}
    for f in PUB.glob("*.html"):
        s = f.read_text()
        t = re.search(r"<title>(.*?)</title>", s)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        if t:
            names[f.stem] = (t.group(1).split(" | ")[0].replace("&amp;", "&").replace(" — ", ": "), d.group(1) if d else "")
    for c in clusters:
        for p in ([c["hub"]] if c.get("hub") else []) + c["pages"]:
            names[p["slug"]] = (p["title"].split(" | ")[0], p["desc"])
    return names


def card(slug, names, label="Read the guide"):
    n, d = names.get(slug, (slug, ""))
    return f'<a class="idea-card" href="/{slug}.html"><h3>{esc(n)}</h3><p>{esc(d)}</p><span class="row-more">{label} →</span></a>'


def render(template, p, names, hub=None, children=()):
    slug = p["slug"]; url = f"{SITE}/{slug}.html"
    title, desc = p["title"], p["desc"]
    s = template
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + esc(desc), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(title), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:type" content=")[^"]*', lambda m: m.group(1) + ("article" if p["type"] == "Article" else "website"), s, count=1)

    crumb = ([(hub["crumb"], f"/{hub['slug']}.html")] if hub else []) + [(p["crumb"], f"/{slug}.html")]
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x.get("@id", "").endswith("/#business"))
    node = {"@type": p["type"], "@id": url + "#page", "url": url, "name": title.split(" | ")[0], "description": desc,
            "inLanguage": "en-GB", "isPartOf": {"@id": f"{SITE}/#website"}, "dateModified": UPDATED[0]}
    if p["type"] == "Article":
        node.update({"headline": title.split(" | ")[0], "author": ORG, "publisher": ORG, "image": f"{SITE}/assets/share.jpg",
                     "datePublished": UPDATED[0], "mainEntityOfPage": url})
    else:
        node["about"] = ORG
    if children:
        node["mainEntity"] = {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{c['slug']}.html", "name": c["title"].split(" | ")[0]} for i, c in enumerate(children)]}
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}] + [
        {"@type": "ListItem", "position": i + 2, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumb)]
    graph = [biz, node, {"@type": "BreadcrumbList", "itemListElement": crumbs}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]

    secs = p["sections"]
    toc = "".join(f'<li><a href="#{x["id"]}">{x["h2"]}</a></li>' for x in secs)
    if p.get("faqs"):
        toc += '<li><a href="#faq">Questions</a></li>'
    body = ""
    if children:
        body += f'<h2 id="all-guides">All {esc(p["crumb"].lower())}</h2><div class="idea-cards">' + "".join(card(c["slug"], names) for c in children) + "</div>"
        toc = '<li><a href="#all-guides">All guides</a></li>' + toc
    for x in secs:
        body += f'<h2 id="{x["id"]}">{x["h2"]}</h2>{x["html"]}'
    if p.get("faqs"):
        body += f'<h2 id="faq">Questions</h2><div class="faq-list">{faq_html(p["faqs"])}</div>'
    if p.get("sources"):
        body += '<h2 id="sources">Sources and official guidance</h2><ul class="source-list">' + "".join(
            f'<li><a class="text-link" href="{u}" target="_blank" rel="noopener noreferrer">{n}</a></li>' for n, u in p["sources"]) + "</ul>"
    body = body.replace("{{WA}}", WA_H)
    related = [r for r in p.get("related", []) if r != slug and r in names][:4]
    rel = ('<section class="section wrap related"><div class="section-head"><h2>Keep<br><em>reading</em></h2><p>More from The Rock Factory, Blackpool.</p></div>'
           f'<div class="idea-cards">{"".join(card(r, names, "Read more") for r in related)}</div></section>') if related else ""
    meta = f'By The Rock Factory, Blackpool · Updated {UPDATED[1]}' if p["type"] in ("Article", "CollectionPage") else f'The Old Rock Factory, Keswick Road, Blackpool FY1 5PB'
    main = f'''<main id="main">
{crumbs_html(crumb)}
<section class="wrap guide-hero"><p class="eyebrow">{p["eyebrow"]}</p><h1>{p["h1"][0]}<br><em>{p["h1"][1]}</em></h1><p class="intro">{p["lead"]}</p><p class="guide-meta">{meta}</p><div class="actions"><a class="button" href="{WA_H}" target="_blank" rel="noopener noreferrer">Ask us on WhatsApp</a><a class="button secondary" href="/compare-units.html">Compare units and prices</a></div></section>
<section class="section wrap guide-body"><div class="guide-grid"><aside class="guide-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}</ol></aside>
<div class="guide-content">{body}
<p class="fine-print">Prices are subject to availability. Minimum rental term: one month, then one month’s notice to leave. Electricity usage is charged separately at the supplier rate, with no markup. Business use needs prior approval. Car storage is not permitted.</p></div></div></section>
{rel}
</main>'''
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)
    return s[:s.find("<main")] + main + s[s.find("</main>") + 7:]


def build():
    template = (PUB / "storage-units-blackpool.html").read_text()
    clusters = load()
    names = page_names(clusters)
    built = []
    for c in clusters:
        hub = c.get("hub")
        if hub:
            (PUB / f"{hub['slug']}.html").write_text(render(template, hub, names, children=c["pages"]))
            built.append(hub["slug"])
        for p in c["pages"]:
            (PUB / f"{p['slug']}.html").write_text(render(template, p, names, hub=hub))
            built.append(p["slug"])
    print("built", len(built), "pages")
    return built


if __name__ == "__main__":
    build()
