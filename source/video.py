"""Video page: /how-rock-is-made-video.html (British Pathé archive film, 1957)

Run from the repo root:  python3 source/video.py   (then python3 source/layout.py)
The YouTube player only loads when the visitor presses play (thumbnail first, youtube-nocookie),
so the page stays fast and sets no YouTube cookies until then.
Archive film by British Pathé (film ID 57.18), embedded from their YouTube channel; credited on the page.
"""
import json, re
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://rockfactory.uk"
SLUG = "how-rock-is-made-video"
VIDEO_ID = "ye-xudhKfYg"
VIDEO_NAME = "'London Rock' Making Candy Factory (1957) | British Pathé"
VIDEO_DESC = "British Pathé film from 1957 showing how London Rock was made by hand at a sweet factory in Wood Green, London: boiling, colouring, building the letters, stretching and cutting."
UPLOAD_DATE = None  # e.g. "2026-10-01"; Google needs this for video rich results
THUMB = f"https://i.ytimg.com/vi/{VIDEO_ID}/hqdefault.jpg"
WA = "https://wa.me/447366991012?text=Hi%2C%20I%27ve%20watched%20your%20video%20and%20I%27d%20like%20to%20ask%20about%20a%20space%20at%20The%20Rock%20Factory."


def build():
    s = (PUB / "find-us.html").read_text()
    url = f"{SITE}/{SLUG}.html"
    title = "How Seaside Rock Was Made: 1957 Film | The Rock Factory"
    desc = "Watch how a stick of rock was made by hand in 1957, from boiling the sugar to building the letters that run through it. British Pathé archive film."
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x.get("@id", "").endswith("/#business"))
    video = {"@type": "VideoObject", "@id": url + "#video", "name": VIDEO_NAME, "description": VIDEO_DESC,
             "thumbnailUrl": THUMB, "embedUrl": f"https://www.youtube-nocookie.com/embed/{VIDEO_ID}",
             "contentUrl": f"https://www.youtube.com/watch?v={VIDEO_ID}", "publisher": {"@id": f"{SITE}/#business"}}
    if UPLOAD_DATE:
        video["uploadDate"] = UPLOAD_DATE
    graph = [biz,
             {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title.split(" | ")[0], "description": desc,
              "inLanguage": "en-GB", "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#business"},
              "mainEntity": {"@id": url + "#video"}},
             video,
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "How rock is made", "item": url}]}]
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    main = f'''<main id="main">
<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">How rock is made</span></nav>
<section class="wrap guide-hero"><p class="eyebrow">From the archive, 1957</p><h1>How seaside rock<br><em>was made</em></h1><p class="intro">Ever wondered how the letters get all the way through a stick of rock? This British Pathé film from 1957 shows it being made by hand, from a barrel of boiling sugar to seven-inch sticks ready to wrap.</p></section>
<section class="section wrap video-section" aria-label="Video">
<div class="video-frame"><button class="video-play" type="button" data-id="{VIDEO_ID}" aria-label="Play video: {VIDEO_NAME}">
<img src="{THUMB}" width="480" height="360" alt="Still from the 1957 British Pathé film of rock being made by hand" decoding="async" fetchpriority="high"><span class="video-play-icon" aria-hidden="true"></span></button></div>
<p class="fine-print">Film: &lsquo;London Rock&rsquo; Making Candy Factory (1957), &copy; British Pathé, filmed in Wood Green, London. Plays from YouTube. <a class="text-link" href="https://www.youtube.com/watch?v={VIDEO_ID}" target="_blank" rel="noopener noreferrer">Watch on YouTube</a>.</p>
</section>
<section class="section wrap"><div class="section-head"><h2>What you are<br><em>watching</em></h2><p>The same craft that gave The Old Rock Factory in Blackpool its name.</p></div>
<div class="guide-content"><ol class="steps">
<li><strong>Boiling the sugar</strong><span>Cane sugar and glucose are boiled in a big copper to about 260&deg;F, then run off as a thick, glue-like toffee and poured across a long table.</span></li>
<li><strong>Colouring</strong><span>Colour is worked into part of the batch by hand, ready for the casing and the letters.</span></li>
<li><strong>Building the letters</strong><span>Strips of red and white toffee are shaped into rolls, one letter each. The rock-maker in the film had been doing it for 38 years.</span></li>
<li><strong>The big roll</strong><span>The letter rolls are packed into one huge roll and wrapped, so the words run right through the middle.</span></li>
<li><strong>Stretching and rolling</strong><span>Three men lift and hang the roll to stretch it, then roll it thinner and thinner by hand. They have about an hour before the toffee sets too hard.</span></li>
<li><strong>Cutting</strong><span>The long thin lengths are measured and cut with big scissors into seven-inch sticks, ready to wrap.</span></li>
</ol>
<p>Want more? Read our short <a class="text-link" href="/blackpool-rock-history.html">history of Blackpool rock</a>. The rock-making has gone from our building, but the making has not: the units are home to Blackpool makers, sellers and traders.</p></div></section>
<section class="section wrap"><div class="section-head"><h2>Make things<br><em>in Blackpool</em></h2><p>Units from £65 a week, available from 1 November. Pre-book and your first week is free.</p></div>
<div class="idea-cards">
<a class="idea-card" href="/storage-units-blackpool.html"><h3>Storage units</h3><p>Ground-floor units from 150 to 300 sq ft, with lighting, electricity and Wi-Fi already on.</p><span class="row-more">See storage units →</span></a>
<a class="idea-card" href="/workshops-studios-blackpool.html"><h3>Workshops and studios</h3><p>Space for makers, repairers and artists, subject to approval.</p><span class="row-more">See workshops →</span></a>
<a class="idea-card" href="/storage-pods-blackpool.html"><h3>Small storage units</h3><p>First-floor pods and rooms from 15 sq ft, opening spring 2027.</p><span class="row-more">See small units →</span></a>
<a class="idea-card" href="/find-us.html"><h3>Find us</h3><p>Keswick Road, off Park Road, Blackpool FY1 5PB.</p><span class="row-more">Directions →</span></a>
</div>
<div class="actions"><a class="button" href="{WA}" target="_blank" rel="noopener noreferrer">Ask us on WhatsApp</a><a class="button secondary" href="/compare-units.html">Compare units and prices</a></div></section>
<script>document.querySelectorAll(".video-play").forEach(function(b){{b.addEventListener("click",function(){{var f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+b.dataset.id+"?autoplay=1&rel=0";f.title="{VIDEO_NAME}";f.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";f.referrerPolicy="strict-origin-when-cross-origin";f.allowFullscreen=true;b.replaceWith(f);}});}});</script>
</main>'''
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)
    s = s[:s.find("<main")] + main + s[s.find("</main>") + 7:]
    (PUB / f"{SLUG}.html").write_text(s)
    print("built", SLUG)


if __name__ == "__main__":
    build()
