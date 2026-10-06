# Writing brief: rockfactory.uk content expansion

You are writing web page content for The Rock Factory, Blackpool (https://rockfactory.uk): storage units, business units,
workshops, artist studios and small offices to let. Output is ONE JSON file (path given in your task). Do not edit any other
file in the repo. Do not run git. Do not call any mcp__hearthbot__ tools.

## Confirmed facts (the ONLY business facts you may state)
- Name: The Rock Factory. Address: The Old Rock Factory, Keswick Road (off Park Road), Blackpool FY1 5PB.
- Enquiries and viewings: WhatsApp 07366 991012 (link placeholder `{{WA}}` – the generator swaps in the wa.me link). No email, no phone calls stated, no enquiry form.
- Ground-floor units, all windowless:
  - 150 sq ft, roller-shutter access, £65/week  (page /150-sq-ft-unit-blackpool.html)
  - 160 sq ft, security (personnel) door access, £69/week  (/160-sq-ft-unit-blackpool.html)
  - 180 sq ft, roller-shutter access, £78/week  (/180-sq-ft-unit-blackpool.html)
  - 300 sq ft two-storey unit, roller shutter, upstairs office or storage area WITH a window, internal staircase, £130/week (/two-storey-unit-blackpool.html)
- Two separate offices, £70/week each, being refurbished, available from January 2027 (/offices-to-let-blackpool.html).
- First-floor storage pods and rooms opening spring 2027, reached by stairs: GUIDE prices (to be confirmed) pods 15/25/35 sq ft from £10/£14/£17 a week, rooms 50/75/100 sq ft £22/£28/£34 a week (/storage-pods-blackpool.html). Always call these "guide prices".
- Units available from 1 November 2026. Pre-bookings get the first week free.
- Rent is based on floor area. Prices subject to availability. Minimum term one month, then one month's notice to leave. Rolling monthly, no long lease.
- Swap to a bigger or smaller unit any time, subject to availability. Some units have interconnecting doors: rent two or three adjoining units; side-by-side units can give both roller-shutter and personnel-door access.
- Lighting, electricity and Wi-Fi already connected in every unit. Standard single-phase electricity only (no three-phase). Electricity usage charged separately at the supplier rate, no markup. No utility deposits.
- 24-hour access. Free app access to CCTV covering the entrance and the area outside the units.
- Shared facilities: tea and coffee room, toilets, water. Tenants can receive mail and clients at the unit.
- Tenants may use the Rock Factory address on their Google Business Profile.
- To move in: one month's rent in advance, security deposit equal to one month's rent, valid government-issued photo ID, signed Direct Debit mandate.
- All business use needs prior approval. Car storage NOT permitted (buildings insurance). Not allowed: melting/heating combustibles (waxes, plastics, resins, oils: candle/soap making, resin casting, 3D print farms), flammable liquids or gases in bulk (fuel, solvent-based paints/chemicals, gas cylinders) unless agreed in writing, cooking/hot food. Low-risk materials (wood, paper, card, fabric, dry goods) are fine.
- Business rates: may apply to commercial units; ask us about the unit; Small Business Rate Relief exists (GOV.UK).
- Tenants in the building: IceWork (web design/SEO; tenant website £200, usually £350; /icework-web-design-blackpool.html) and Blackpool Building Services.
- The rock-making has gone; the building carries the name. Do NOT claim the history of this particular premises.

Never invent: other prices, distances, drive times, parking arrangements, opening hours beyond "24-hour access", insurance included,
reviews, testimonials, customer numbers, awards, staff names, security features beyond the CCTV app, loading bays, lifts, alarm systems,
climate control, ceiling heights, unit dimensions (only sq ft areas), availability counts. If something is unknown, say "ask us on WhatsApp".
Computed facts are fine (e.g. £65 a week is about £282 a month (65×52/12), or about £22.53 per sq ft per year).
General knowledge (how to pack, what a roller shutter is, UK business admin) is fine; for UK rules/legal/tax/money points,
cite the official source (gov.uk, hse.gov.uk, ico.org.uk, legislation.gov.uk, food.gov.uk, blackpool.gov.uk) in "sources"
and only state what you are confident is current; keep it general and add "check the official guidance" rather than precise
thresholds you are unsure of. You may use WebSearch/WebFetch to verify facts; if you can't verify something, leave it out.

## Style
- UK English. Plain, warm, direct, short sentences. Second person ("you"). Sentence-case headings.
- No em dashes (—). Use full stops, commas or colons. En dash only in number ranges is ok.
- Every page genuinely useful and DIFFERENT from the others: no paragraph templates repeated across pages.
- Lead naturally to the right unit with internal links, but no hard sell. One WhatsApp call to action within the body at most.
- Target: guides 1,200–1,700 words of visible text each (sections + FAQs); hubs 800–1,100 words.

## JSON format
{
  "hub": PAGE or null,
  "pages": [PAGE, ...]
}
PAGE = {
  "slug": "kebab-case-slug",                 // file becomes /<slug>.html; use exactly the slugs assigned to you
  "type": "Article" | "WebPage" | "AboutPage" | "ContactPage" | "CollectionPage",
  "title": "Keyword-led title | The Rock Factory",   // TOTAL <= 60 characters including the suffix; unique
  "desc": "Meta description, 120–155 characters, includes Blackpool where natural",
  "crumb": "Short breadcrumb name (2–4 words)",
  "eyebrow": "Small label above the H1",
  "h1": ["First line of H1", "second line (shown in italic accent)"],   // together read as one heading, include main keyword
  "lead": "One or two sentence intro paragraph (plain text, no HTML)",
  "sections": [ {"id": "kebab-id", "h2": "Section heading", "html": "<p>…</p>…"} ],   // 5–9 sections
  "faqs": [["Question?", "Answer (plain text or inline <a>/<strong>)"]],               // 3–6, not duplicating other pages verbatim
  "sources": [["Name (Publisher)", "https://…"]],      // official sources only, may be []
  "related": ["slug", "slug", "slug"]                  // 3–5 slugs from the site list below
}
Allowed HTML inside "html": <p>, <h3>, <strong>, <em>, <br>,
<ul class="tick-list"><li>…</li></ul>, <ul class="tick-list cross"><li>…</li></ul> (for "don't"s),
<ol class="steps"><li><strong>Step title</strong><span>Step text</span></li></ol>,
<div class="table-wrap"><table class="price-table"><thead><tr><th scope="col">…</th></tr></thead><tbody><tr><th scope="row">…</th><td>…</td></tr></tbody></table></div>,
<div class="callout"><h3>…</h3><p>…</p></div>,
<a class="text-link" href="/slug.html">descriptive anchor text</a> (internal), external links: <a class="text-link" href="https://…" target="_blank" rel="noopener noreferrer">…</a>.
WhatsApp link: <a class="text-link" href="{{WA}}" target="_blank" rel="noopener noreferrer">message us on WhatsApp</a>.
No other tags, no classes beyond these, no inline styles, no images, no H1/H2 inside html. Use &amp; for ampersands in HTML text.
Every internal href must be one of the site pages listed below (with .html, or "/" for home, "/#prices" for prices).
Anchor text must be descriptive (never "click here"/"read more").

## Site pages (existing + being written now)
Existing: / , /storage-units-blackpool.html, /offices-to-let-blackpool.html, /workshops-studios-blackpool.html,
/150-sq-ft-unit-blackpool.html, /160-sq-ft-unit-blackpool.html, /180-sq-ft-unit-blackpool.html, /two-storey-unit-blackpool.html,
/storage-pods-blackpool.html, /small-business-unit-ideas-blackpool.html, /unit-ideas-online-sellers.html,
/unit-ideas-textiles-leather.html, /unit-ideas-makers-studios.html, /unit-ideas-tech-repair.html, /unit-ideas-trades-storage.html,
/our-businesses.html, /icework-web-design-blackpool.html
Core (cluster E): /about.html, /find-us.html, /rental-terms.html, /faqs.html, /glossary.html, /compare-units.html,
/storage-prices-explained.html, /blackpool-rock-history.html
Storage guides (cluster A): hub /storage-guides-blackpool.html, /what-size-storage-unit.html, /how-to-pack-a-storage-unit.html,
/storage-when-moving-house.html, /storage-during-renovation.html, /student-storage-blackpool.html, /furniture-storage-blackpool.html,
/document-archive-storage.html, /seasonal-storage-blackpool.html, /declutter-with-storage.html, /what-not-to-store.html,
/storage-security-tips.html, /storage-insurance-guide.html, /storage-unit-vs-garage.html
Business guides (cluster B): hub /business-guides-blackpool.html, /start-a-business-blackpool.html, /business-rates-small-units.html,
/move-business-out-of-home.html, /google-business-profile-address.html, /small-business-insurance-guide.html,
/health-and-safety-small-unit.html, /unit-vs-shop-vs-coworking.html, /set-up-a-small-workshop.html, /working-in-a-windowless-unit.html,
/sole-trader-or-limited-company.html, /selling-at-blackpool-markets.html, /seasonal-business-blackpool.html
New industries (cluster C): /unit-ideas-event-hire.html, /unit-ideas-market-traders.html, /unit-ideas-furniture-upcycling.html,
/unit-ideas-gardening-landscaping.html, /unit-ideas-clubs-community.html, /unit-ideas-mobile-services.html
Areas (cluster D): hub /storage-fylde-coast.html, /storage-south-shore.html, /storage-north-shore-bispham.html, /storage-layton.html,
/storage-marton.html, /storage-st-annes.html, /storage-lytham.html, /storage-poulton-le-fylde.html,
/storage-thornton-cleveleys.html, /storage-fleetwood.html

## Done means
Valid JSON (check with `python3 -c "import json;json.load(open(PATH))"`), every slug as assigned, titles <= 60 chars and unique,
descs 120–155 chars, word counts in range (check with a quick script), no em dashes, no invented facts. Reply with a 3-line summary
(pages, total words, anything you were unsure about and left out).
