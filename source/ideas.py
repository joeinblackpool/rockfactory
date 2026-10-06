"""Business ideas hub and industry pages.

Run from the repo root:  python3 source/ideas.py
Facts used are only those the owner has confirmed: unit sizes, prices, access, lighting/electricity/Wi-Fi,
24-hour access, CCTV app, shared facilities, approval of business use, no car storage, and the owner's
fire rule: no melting combustibles (waxes, plastics, resins, oils); low-risk combustibles (wood, paper,
card, fabric, dry goods) are fine.
"""
import json, re, urllib.parse
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://rockfactory.uk"
UPDATED = "October 2026"
WA = "https://wa.me/447366991012?text=" + urllib.parse.quote("Hi, I'd like to check whether my business would suit a unit at The Rock Factory.")
WA_H = WA.replace("&", "&amp;")
HUB = "small-business-unit-ideas-blackpool"

UNITS = {
    150: ("/150-sq-ft-unit-blackpool.html", "150 sq ft · roller shutter · £65 a week"),
    160: ("/160-sq-ft-unit-blackpool.html", "160 sq ft · security door · £69 a week"),
    180: ("/180-sq-ft-unit-blackpool.html", "180 sq ft · roller shutter · £78 a week"),
    300: ("/two-storey-unit-blackpool.html", "300 sq ft · two storeys with upstairs office · £130 a week"),
}

def unit_links(sizes):
    return " or ".join(f'<a class="text-link" href="{UNITS[s][0]}">{UNITS[s][1]}</a>' for s in sizes)

# Each industry: slug, title, h1, eyebrow, intro paragraphs, why units suit, uses, checklist extras, faqs
INDUSTRIES = [
 {"slug": "unit-ideas-online-sellers", "short": "Online sellers & e-commerce",
  "title": "Storage for Online Sellers in Blackpool | The Rock Factory",
  "desc": "Unit ideas for Amazon, eBay, Etsy, Vinted and Shopify sellers in Blackpool: stock storage, packing and dispatch from £65 a week at The Old Rock Factory.",
  "h1": ("Space for", "online sellers"),
  "lead": "Move your stock, packing table and parcels out of the spare room. A small unit gives an online shop a proper base: somewhere to store stock, photograph listings and pack orders, with lighting, electricity and Wi-Fi already connected.",
  "why": ["Online selling is mostly dry, clean work with cardboard, paper and boxed goods, which is exactly the low-risk kind of business our units are made for.",
          "Roller-shutter units make it easy to take in deliveries of stock and load outgoing parcels. The 160 sq ft unit with a security door suits smaller, higher-value stock.",
          "Wi-Fi is connected in every unit, so you can print labels, update listings and answer customers from the unit."],
  "uses": [
   ("E-commerce stock storage", [150, 180],
    "For sellers on Amazon, eBay, Etsy or their own Shopify store who have outgrown the house. Keep stock on shelving, a packing bench by the door and a label printer on Wi-Fi.",
    "Shelving along the long walls, a packing bench near the door, outgoing parcels stacked by the exit so collections are quick.",
    "Keep stock off the floor on shelving and in labelled boxes, and keep a simple stock list so you always know what is where."),
   ("Vintage and reseller clothing", [150, 160],
    "Clothing rails, a small photography corner and a packing desk for Vinted, Depop and eBay resellers. Clothes are low-risk stock and easy to organise on rails.",
    "Rails along one wall sorted by size or category, a plain wall or backdrop with a light for listing photos, a steaming and packing table.",
    "Garment steamers are fine. Keep bags and tissue paper in closed boxes and away from heaters."),
   ("Subscription box packing", [180, 300],
    "Store flat-pack boxes and dry items such as socks, stationery, books or packaged snacks, then pack and dispatch each month's boxes in batches.",
    "Flat-pack boxes standing upright on one side, products on shelving, a long packing table in the middle for an assembly line.",
    "The 300 sq ft unit lets you keep stock on the ground floor and run the admin from the upstairs office."),
   ("Trading cards, comics and books", [160],
    "A tidy, secure space to sort, grade, store and post trading cards, comics, rare books or vinyl records. The security-door unit suits small, valuable stock.",
    "Desk with good task lighting, shelving with archive boxes, a separate packing area so stock and packaging do not mix.",
    "Paper and card stock is fine. Keep it in boxes off the floor."),
   ("Board game and book publishing fulfilment", [180, 300],
    "Independent publishers of board games, card games, books and zines can store print runs and send out orders and pre-orders from one place.",
    "Pallet-sized stock stacks on shelving, a scale and label printer, outgoing orders by the door.",
    "Plan stock levels before a big launch so you do not run out of room."),
   ("Packaging supplies distribution", [180, 300],
    "Stock and deliver boxes, mailing bags, paper fill and eco-friendly packaging to other small businesses in Blackpool and the Fylde.",
    "Bulky but light stock up high on shelving, heavier stock low, a clear route from the shutter to the shelves.",
    "Paper and card are fine. Ask us before storing large quantities of plastic film or foam."),
  ],
  "faqs": [
   ("Can I receive deliveries at the unit?", "Yes. Tenants can receive mail and clients at the unit, and you have 24-hour access to meet couriers. Roller-shutter units make larger deliveries easier."),
   ("Which unit is best for an online shop?", f"For most sellers, {unit_links([150, 180])}. If you also want a desk away from the stock, the {unit_links([300])} has an upstairs office or storage area with a window."),
   ("Can I store stock that I sell on Amazon?", "Yes, dry, boxed and low-risk stock is fine. Tell us what you sell when you enquire, because all business use needs our approval first."),
  ]},
 {"slug": "unit-ideas-textiles-leather", "short": "Textiles, leather & sewing",
  "title": "Textile & Leather Workshops, Blackpool | The Rock Factory",
  "desc": "Workshop ideas for tailors, embroiderers, leatherworkers and curtain makers in Blackpool. Units from £65 a week with power and Wi-Fi at The Old Rock Factory.",
  "h1": ("Workshops for", "textiles & leather"),
  "lead": "Sewing machines, cutting tables and fabric rolls take over a home quickly. A unit gives you room to work properly and to welcome clients for fittings, with lighting, electricity and Wi-Fi already connected.",
  "why": ["Fabric, thread and leather are low-risk materials, and sewing, cutting and stitching involve no melting or heating of combustibles.",
          "A long cutting table fits comfortably in every unit size, and you can receive clients at the unit for fittings and collections.",
          "The 300 sq ft unit gives you a workshop downstairs and an upstairs room with a window for fittings or admin."],
  "uses": [
   ("Tailoring and alterations", [150, 160],
    "Room for one or two sewing machines, an overlocker, a cutting table, a steam iron and rails for work in progress and finished garments.",
    "Cutting table in the centre, machines along a wall near sockets, rails for jobs labelled by customer, a small fitting corner with a mirror.",
    "Keep the iron on a heat-proof stand and switch it off at the end of the day."),
   ("Embroidery and personalisation", [150, 180],
    "Commercial embroidery machines for logos on workwear, hats, team kit and gifts, plus stock of blank garments. Heat-press transfers can also work here; ask us about your machine.",
    "Machines on sturdy benches, blank stock on shelving by size, finished orders bagged and labelled by the door.",
    "The units have standard single-phase electricity, not three-phase, so choose machines that run from a normal plug socket."),
   ("Leather goods workshop", [150, 160],
    "Cutting, hand-stitching and finishing wallets, belts, bags and dog collars from dry leather hides, with a cutting mat and hand tools.",
    "Large cutting surface, hides stored flat or rolled on a rack, a stitching bench with good lighting, a finishing and packing area.",
    "Hand tools and dry hides are fine. Ask us before using solvent-based dyes or glues in quantity."),
   ("Curtains, blinds and soft furnishings", [180, 300],
    "A long table for measuring, cutting and sewing made-to-measure curtains, blinds and cushions, with fabric rolls stored on racks.",
    "The longest table you can fit down the middle of the unit, fabric rolls on a wall rack, finished orders hung or boxed by the door.",
    "Roller-shutter units make it easy to bring in long fabric rolls and take out finished curtains."),
   ("Costume and dancewear making", [150, 160],
    "Making and repairing costumes for dance schools, theatre groups and Blackpool's entertainment industry, with space to store fabrics and finished pieces.",
    "Rails for finished costumes, a sewing area, boxes for trims and embellishments, a mirror for fittings.",
    "Clients can visit the unit for fittings and collections."),
  ],
  "faqs": [
   ("Can I run industrial sewing machines in a unit?", "Most industrial sewing machines run on standard single-phase electricity, which is connected in every unit. There is no three-phase power, so check your machines run from a normal plug socket."),
   ("Can customers come to the unit for fittings?", "Yes. Tenants can receive clients at the unit, and there are shared toilets and a shared tea and coffee room on site."),
   ("Is a 150 sq ft unit big enough for a sewing business?", f"For one or two people, usually yes: room for machines, a cutting table and rails. For curtains or bulky work, look at the {unit_links([180, 300])}."),
  ]},
 {"slug": "unit-ideas-makers-studios", "short": "Makers & creative studios",
  "title": "Maker & Creative Studio Space, Blackpool | The Rock Factory",
  "desc": "Studio ideas for picture framers, woodworkers, jewellers, sign makers, photographers and podcasters in Blackpool. Units from £65 a week, power and Wi-Fi included.",
  "h1": ("Studios for", "makers & creatives"),
  "lead": "Artists, makers and content creators need a space they can leave set up. Our units give you a private studio with lighting, electricity and Wi-Fi already connected, 24-hour access and room to welcome clients.",
  "why": ["Wood, paper, card, canvas and metal hand-work are low-risk materials, so most dry making and creative work suits our units.",
          "The ground floors are windowless, which helps for photography and video, where you want to control the light yourself.",
          "You can leave your studio set up between sessions and lock up, instead of packing everything away at home."],
  "uses": [
   ("Picture framing", [150, 180],
    "A mitre saw or guillotine, an underpinner and mount cutter, with vertical racks for moulding lengths, mount board and glass.",
    "Moulding and board stored upright in wall racks, a cutting bench and an assembly bench, finished frames wrapped and stacked by the door.",
    "Store glass upright in a rack, never flat on the floor."),
   ("Small-scale woodworking", [180, 300],
    "Hand tools and benchtop machines for chopping boards, boxes, frames, signs and turned items. Wood is a low-risk material and fine to store and work.",
    "A sturdy workbench, timber stored on a wall rack, benchtop machines on mobile stands, a dust extractor or vacuum.",
    "Keep sawdust under control with a vacuum or extractor and clear offcuts daily. Ask us before using solvent-based finishes in quantity."),
   ("Jewellery bench", [160],
    "Stone setting, engraving, wire work, polishing and repairs at a jeweller's bench, with secure storage for tools and stock. The security-door unit suits valuable work.",
    "Jeweller's bench with task lighting, a polishing area kept separate, a lockable cabinet for metals and stones.",
    "Ask us before using an open-flame torch or a casting kiln, because these need our approval."),
   ("Vinyl signs and decals", [150, 180],
    "A vinyl plotter, weeding table and laminator for shop signs, vehicle graphics, wall art and decals for local businesses.",
    "Plotter and computer on one bench, a long weeding and application table, vinyl rolls on a wall rack.",
    "Vinyl sheet is fine to store and cut. There is no melting involved in plotting and weeding."),
   ("Paper goods and stationery", [150, 160],
    "Designing, printing, cutting and packing greeting cards, wedding invitations, notebooks and prints.",
    "Printer and guillotine on a bench, paper stock in flat drawers or boxes, a packing area for orders.",
    "Paper and card are low-risk stock. Keep them in closed boxes off the floor."),
   ("Product photography studio", [150, 180],
    "A backdrop, lights and a table for shooting product photos and videos for online shops, including your own or other local businesses.",
    "Backdrop on the short wall, lights on stands, a props shelf, a desk for editing on the Wi-Fi.",
    "The windowless ground floor gives you full control of the light."),
   ("Podcast and voiceover booth", [160],
    "A quiet room for recording podcasts, voiceovers and interviews, with acoustic panels, microphones and a desk.",
    "Acoustic panels on the walls, a recording desk away from the door, chairs for guests.",
    "Ask us before fixing anything to the walls."),
  ],
  "faqs": [
   ("Can I use power tools in the unit?", "Hand tools and benchtop power tools are generally fine for dry materials such as wood, metal and card. Tell us what you plan to use when you enquire, because all business use needs our approval."),
   ("Is the unit suitable for photography?", "The ground floors are windowless, which makes it easier to control the light for product photography and video. The 300 sq ft unit also has an upstairs room with a window."),
   ("Can I hold classes or workshops?", "Tenants can receive clients at the unit. If you plan to run classes, tell us how many people you expect so we can check it suits the space."),
  ]},
 {"slug": "unit-ideas-tech-repair", "short": "Tech & repair workshops",
  "title": "Repair Workshop Space, Blackpool | The Rock Factory",
  "desc": "Workshop ideas for phone, laptop, PC, drone and bike repairs in Blackpool. Secure units from £65 a week with power, Wi-Fi and 24-hour access.",
  "h1": ("Workshops for", "tech & repair"),
  "lead": "Repair work needs a clean bench, good lighting, plenty of sockets and somewhere secure to keep customers' devices overnight. Our units have lighting, electricity and Wi-Fi already connected, with 24-hour access and free CCTV app access covering the entrance.",
  "why": ["Repair, assembly and configuration are dry, mechanical jobs with a low fire risk.",
          "The 160 sq ft unit has a security door, which suits workshops holding customers' phones, laptops and other valuable kit.",
          "You can receive customers at the unit for drop-offs and collections."],
  "uses": [
   ("Phone, tablet and laptop repair", [160, 150],
    "Screen and battery replacements, micro-soldering and data recovery at an anti-static bench, with secure storage for customers' devices.",
    "Anti-static mats on a well-lit bench, tagged trays for each job, a lockable cabinet for devices awaiting collection.",
    "Store replacement batteries in their packaging and do not keep damaged or swollen batteries in the unit."),
   ("PC building and IT services", [150, 180],
    "Building custom PCs, testing hardware and setting up computers and networks for local offices, with stock of parts on shelving.",
    "Assembly bench, a test bench with a monitor, parts on labelled shelving, finished machines boxed by the door.",
    "Wi-Fi is connected, so you can install updates and test networking on site."),
   ("Drone assembly and repair", [150, 160],
    "Building, wiring, tuning and repairing camera and racing drones from modular parts.",
    "Clean assembly bench, parts drawers, a testing area kept clear of stock.",
    "Keep LiPo batteries in fire-safe charging bags and only charge them while you are in the unit. Ask us about battery storage."),
   ("Bicycle servicing", [150, 180],
    "Tune-ups, wheel building and mechanical repairs on push bikes, with a workstand, tool wall and space for bikes awaiting collection.",
    "Workstand in the middle, tools on a pegboard wall, bikes hung on wall hooks to save floor space.",
    "Ask us before working on e-bike batteries or storing several e-bikes."),
   ("Locksmith base and key cutting", [160],
    "A secure base for a mobile locksmith to cut keys, repair cylinders and store locks, hardware and stock.",
    "Key cutting machine on a solid bench, stock in labelled drawers, van stock prepared by the door.",
    "The security-door unit suits stock of locks and keys."),
   ("Tool and knife sharpening", [150],
    "Sharpening kitchen knives, scissors, garden tools and trade blades for customers and local businesses.",
    "Sharpening station on a solid bench, a clean area for finished work, a log of each customer's items.",
    "Keep the sharpening area clear of cardboard and paper. Ask us about any grinder that throws sparks."),
  ],
  "faqs": [
   ("Is it secure enough to keep customers' devices overnight?", "Tenants get free CCTV app access covering the entrance and the area outside the units. The 160 sq ft unit has a security door. We also recommend contents insurance for customers' goods in your care."),
   ("Can I charge batteries in the unit?", "Charging tools and devices is fine. Ask us before storing or charging large numbers of lithium batteries, such as e-bike or drone batteries."),
   ("Can customers drop off repairs?", "Yes. Tenants can receive clients at the unit, with 24-hour access."),
  ]},
 {"slug": "unit-ideas-trades-storage", "short": "Trades & business storage",
  "title": "Trade & Business Storage, Blackpool | The Rock Factory",
  "desc": "Secure storage in Blackpool for electricians, plumbers, decorators, event planners, home stagers and property managers. Units from £65 a week, 24-hour access.",
  "h1": ("Storage for", "trades & businesses"),
  "lead": "A secure lock-up close to central Blackpool for tools, materials, stock and equipment. Roller-shutter units make loading easy, and you get 24-hour access, lighting, electricity and Wi-Fi.",
  "why": ["Tools, timber, fixings, furniture and boxed stock are all low-risk to store.",
          "Roller-shutter access on the 150, 180 and 300 sq ft units makes it quick to load and unload. Car storage is not permitted.",
          "24-hour access means you can collect what you need for an early start."],
  "uses": [
   ("Tradesperson tool and materials store", [150, 180],
    "A base for electricians, plumbers, joiners and decorators to keep tools, fittings, cable, pipe and materials, so the van is not your warehouse.",
    "Heavy-duty shelving for materials, a tool wall, a bench for prep work, a clear route from the shutter.",
    "Water-based paints are fine. Ask us before storing solvent-based paints, fuel or gas cylinders."),
   ("Event and wedding prop storage", [180, 300],
    "Backdrops, arches, table linen, centrepieces, lighting and decorations stored safely between events.",
    "Tall items against the back wall, linen in labelled boxes, a staging area by the shutter for packing each event.",
    "The 300 sq ft unit gives you extra space upstairs for linen and small items."),
   ("Home staging furniture", [180, 300],
    "Accent furniture, rugs, lamps, cushions and art for staging homes for sale or rent.",
    "Furniture covered and stacked safely, rugs rolled on a rack, small items boxed by room style.",
    "Use furniture covers and keep items off the floor on pallets or shelving."),
   ("Property maintenance supplies", [150, 180],
    "Spare fittings, flooring, fixings, tools and turnover supplies for landlords and property managers.",
    "Shelving labelled by property or job type, a bench for small repairs, a stock list on the wall.",
    "Store everyday cleaning products in small quantities only, and ask us before storing anything flammable."),
   ("Cleaning company equipment", [150, 160],
    "Vacuums, floor machines, mops and everyday cleaning supplies for a commercial or domestic cleaning business.",
    "Machines lined up along one wall, supplies on shelving, a charging point for cordless kit.",
    "Keep cleaning chemicals to everyday quantities in their original containers."),
   ("Business archives and stock overflow", [160, 150],
    "Overflow stock, seasonal stock or boxed business records that you need to keep but not in your shop or office.",
    "Archive boxes on shelving, labelled by year or category, with an index so you can find things quickly.",
    "The units are not climate-controlled, so ask us if you need to store anything sensitive to temperature or damp."),
  ],
  "faqs": [
   ("Can I store my van or car in a unit?", "No. Car storage is not permitted."),
   ("Can I store paint and materials?", "Tools, timber, fixings and water-based paints are fine. Ask us before storing solvent-based paints, fuel, gas cylinders or anything flammable."),
   ("How early can I get in?", "Tenants have 24-hour access to their unit."),
  ]},
]

# More industries written later live in content/industries.json (same shape as an entry above).
_more = Path(__file__).resolve().parent / "content" / "industries.json"
if _more.exists():
    INDUSTRIES += [{**x, "h1": tuple(x["h1"]), "uses": [tuple(u) for u in x["uses"]], "faqs": [tuple(f) for f in x["faqs"]]}
                   for x in json.loads(_more.read_text())]

# Deep profiles (equipment, power, safety, floor plan, launch checklist) and hub comparison ratings.
PROFILES = json.loads((Path(__file__).resolve().parent / "content" / "profiles.json").read_text())
RANK = {"Low": 1, "Medium": 2, "Higher": 3, "High": 3, "Simple": 1, "Moderate": 2, "Complex": 3}
RATING_HELP = [
 ("Power need", "Low: lights, a laptop and chargers. Medium: a few machines running on standard sockets. Higher: motors or several machines at once, so plan which sockets each one uses. Every unit has standard single-phase electricity; there is no three-phase power."),
 ("Layout", "Simple: shelving and one bench. Moderate: separate zones for making and packing. Complex: long tables or machines that need clear space around them."),
 ("Set-up cost", "Compared with each other, not a quote. Low: shelving, a bench and basic tools. Medium: one or two specialist machines. High: specialist machines that are the biggest part of the start-up budget. Stock is not included."),
]

NOT_SUITABLE = [
 ("Melting or heating combustibles", "Candle making, soap making, wax melts, resin casting, plastic moulding and 3D print farms, or anything that melts waxes, plastics, resins or oils."),
 ("Flammable liquids and gases", "Fuel, solvent-based paints or chemicals in bulk, and gas cylinders, unless we have agreed otherwise in writing."),
 ("Cars and vehicles", "Car storage is not permitted."),
 ("Cooking", "Cooking, roasting or hot food preparation. Dry food packing may be possible; see our <a class=\"text-link\" href=\"/unit-ideas-dry-goods-botanicals.html\">dry goods guide</a> and ask us first."),
]

GENERAL_FAQS = [
 ("Can I run a business from a 150 sq ft unit?", "Yes. 150 sq ft is roughly the floor area of a single garage: enough for an online shop's stock and packing table, a sewing or repair bench, a small studio or a tradesperson's tools and materials. All business use needs our approval first, so tell us what you plan to do when you enquire."),
 ("What is included in the rent?", "Lighting, electricity and Wi-Fi are already connected in every unit. Electricity usage is charged separately at the supplier rate, with no markup. Tenants get 24-hour access, free CCTV app access covering the entrance and the area outside the units, and shared facilities: a tea and coffee room, toilets and water."),
 ("Can I use the address on my Google Business Profile?", "Yes. Tenants can use The Old Rock Factory, Keswick Road, Blackpool FY1 5PB as their business address on Google, so customers can find you without you putting your home address online."),
 ("Is there three-phase power?", "No. Every unit has standard single-phase electricity, the same as a normal plug socket. Choose machines and tools that run on single-phase power."),
 ("What can't I do in a unit?", "We do not allow anything that melts or heats combustible materials such as waxes, plastics, resins or oils, flammable liquids or gases in bulk, or car storage. Low-risk materials such as wood, paper, card, fabric and dry goods are fine. Every business use needs our approval."),
 ("How much does a unit cost?", "Units are £65 a week for 150 sq ft, £69 for 160 sq ft, £78 for 180 sq ft and £130 for the 300 sq ft two-storey unit. Two offices are £70 a week each, available from January 2027. Prices are based on floor area and subject to availability."),
 ("What do I need to move in?", "One month's rent in advance, a security deposit equal to one month's rent, valid government-issued photo ID and a signed Direct Debit mandate. The minimum term is one month."),
 ("When can I move in?", "The units are available from 1 November, and pre-bookings get their first week free. Small to medium first-floor storage pods and rooms open in spring 2027."),
 ("Can I change unit if my business changes?", "Yes. You can swap to a bigger or smaller unit at any time, subject to availability. As you grow you can rent two or three adjoining units, and some have interconnecting doors so you can move between them without going outside."),
 ("How much notice do I give to leave?", "One month. You rent month by month with a minimum term of one month, and there are no utility deposits."),
 ("Do I need business insurance?", "We recommend speaking to an insurance broker. Most small businesses consider public liability insurance and cover for their contents and stock. If you employ staff, employers' liability insurance is a legal requirement in the UK."),
 ("Do I have to pay business rates?", "Business rates can apply to commercial units. Ask us about the unit you are interested in, and check whether you qualify for Small Business Rate Relief on GOV.UK."),
]

SOURCES = [
 ("Set up a business (GOV.UK)", "https://www.gov.uk/set-up-business"),
 ("Small Business Rate Relief (GOV.UK)", "https://www.gov.uk/apply-for-business-rate-relief/small-business-rate-relief"),
 ("Employers' liability insurance (GOV.UK)", "https://www.gov.uk/employers-liability-insurance"),
 ("Register a food business (GOV.UK)", "https://www.gov.uk/food-business-registration"),
 ("Health and safety made simple (HSE)", "https://www.hse.gov.uk/simple-health-safety/"),
]

CHECKLIST = [
 "Decide which unit suits your stock, machines and how you will load and unload.",
 "Message us with what your business does, so we can approve the use before you commit.",
 "Register your business with HMRC as a sole trader or limited company if you have not already.",
 "Speak to an insurance broker about public liability, contents and stock cover, and employers' liability if you have staff.",
 "Ask us whether business rates apply, and check Small Business Rate Relief on GOV.UK.",
 "Plan your layout: shelving up the walls, benches near sockets, and a clear route to the door.",
 "Arrange one month's rent, the deposit, photo ID and a Direct Debit mandate for move-in day.",
]


def page(template, slug, title, desc, crumb, main, extra_graph):
    url = f"{SITE}/{slug}.html"
    s = template
    s = re.sub(r"<title>.*?</title>", f"<title>{title.replace('&', '&amp;')}</title>", s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title.replace("&", "&amp;"), s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:type" content=")[^"]*', lambda m: m.group(1) + "article", s, count=1)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    biz = next(x for x in json.loads(m.group(1))["@graph"] if x["@type"] == "LocalBusiness")
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
    for i, (n, u) in enumerate(crumb, start=2):
        crumbs.append({"@type": "ListItem", "position": i, "name": n, "item": u})
    graph = [biz,
             {"@type": "Article", "@id": url + "#article", "headline": title.split(" | ")[0], "description": desc, "url": url,
              "inLanguage": "en-GB", "dateModified": "2026-10-06", "author": {"@id": f"{SITE}/#business"},
              "publisher": {"@id": f"{SITE}/#business"}, "isPartOf": {"@id": f"{SITE}/#website"},
              "image": f"{SITE}/assets/share.jpg"},
             {"@type": "BreadcrumbList", "itemListElement": crumbs}] + extra_graph
    s = s[:m.start(1)] + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + s[m.end(1):]
    s = re.sub(r'<nav class="nav".*?</nav>', lambda n: n.group(0).replace(' aria-current="page"', ''), s, count=1, flags=re.S)
    return s[:s.find("<main")] + main + s[s.find("</main>") + 7:]


def lc(name):
    """Lower-case a name's first letter for mid-sentence use, keeping acronyms such as PC."""
    return name if len(name) > 1 and name[1].isupper() else name[0].lower() + name[1:]


def chips(items):
    """Bold metric chips: (label, value) or (label, value, note)."""
    out = ""
    for it in items:
        label, value, note = (list(it) + [None])[:3]
        lvl = f' data-level="{RANK[value]}"' if value in RANK else ""
        out += f'<li class="chip"{lvl}><span>{label}</span><strong>{value}</strong>{f"<small>{note}</small>" if note else ""}</li>'
    return f'<ul class="chips">{out}</ul>'


def faq_html(faqs):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)


def crumbs_html(items):
    parts = ['<a href="/">Home</a>']
    for n, u in items[:-1]:
        parts.append(f'<a href="{u}">{n}</a>')
    parts.append(f'<span aria-current="page">{items[-1][0]}</span>')
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(parts) + '</nav>'


def industry_page(t, ind):
    slug = ind["slug"]; url = f"{SITE}/{slug}.html"
    crumb = [("Business ideas", f"{SITE}/{HUB}.html"), (ind["short"], url)]
    prof = PROFILES.get(slug, {}); deep = prof.get("uses", {})
    toc = "".join(f'<li><a href="#{re.sub(r"[^a-z0-9]+", "-", u[0].lower()).strip("-")}">{u[0]}</a></li>' for u in ind["uses"])
    uses = ""
    for name, sizes, what, layout, tip in ind["uses"]:
        aid = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        d = deep.get(name)
        if not d:
            uses += (f'<article class="idea" id="{aid}"><h3>{name}</h3><p>{what}</p>'
                     f'<dl class="idea-facts"><div><dt>Best unit</dt><dd>{unit_links(sizes)}</dd></div>'
                     f'<div><dt>Layout</dt><dd>{layout}</dd></div><div><dt>Good to know</dt><dd>{tip}</dd></div></dl></article>')
            continue
        uses += (f'<article class="idea deep" id="{aid}"><h3>{name}</h3><p class="idea-answer"><strong>{d["answer"]}</strong></p>'
                 + chips([("Power need", d["power"]), ("Layout", d["layout"]), ("Set-up cost", d["cost"]), ("Best unit", " or ".join(f"{s} sq ft" for s in sizes))])
                 + f'<p>{what}</p>'
                 f'<h4>Technical profile</h4><div class="profile-grid">'
                 f'<section class="profile-card"><h5>Equipment that fits</h5><ul>{"".join(f"<li>{k}</li>" for k in d["kit"])}</ul></section>'
                 f'<section class="profile-card"><h5>Power and utilities</h5><p>{d["power_detail"]}</p></section>'
                 f'<section class="profile-card wide"><h5>Safety and site rules</h5><p>{d["safety"]}</p></section></div>'
                 f'<h4>Floor plan</h4><dl class="idea-facts">'
                 f'<div><dt>Vertical racking</dt><dd>{d["racking"]}</dd></div>'
                 f'<div><dt>Mobile benches</dt><dd>{d["benches"]}</dd></div>'
                 f'<div><dt>Flow of goods</dt><dd>{d["flow"]}</dd></div></dl>'
                 f'<h4>Launch checklist</h4><div class="profile-grid">'
                 f'<section class="profile-card"><h5>Start-up supplies</h5><ul class="check">{"".join(f"<li>{k}</li>" for k in d["supplies"])}</ul></section>'
                 f'<section class="profile-card"><h5>Insurance to discuss</h5><p>{d["cover"]}</p><p><a class="text-link" href="/small-business-insurance-guide.html">Small business insurance guide</a></p></section></div>'
                 f'<dl class="idea-facts"><div><dt>Best unit</dt><dd>{unit_links(sizes)}</dd></div><div><dt>Good to know</dt><dd>{tip}</dd></div></dl></article>')
    answer = ""
    if prof.get("answer"):
        r = prof["rating"]
        answer = (f'<div class="answer-box"><p><strong>{prof["answer"]}</strong></p>'
                  + chips([("Power need", r["power"], prof.get("power_note")), ("Layout", r["layout"], prof.get("layout_note")), ("Set-up cost", r["cost"], prof.get("cost_note"))])
                  + '</div>')
    plan = ""
    if deep:
        plan = ('<h2 id="plan">Planning a small unit floor</h2>'
                '<p><strong>Go up the walls, keep benches mobile and give goods one clear route from the door to the work area and back.</strong></p>'
                '<ul class="tick-list"><li><strong>Measure before you buy racking.</strong> Ask us for the height of the unit you are viewing, then choose shelving that uses it safely, fixed to the wall where the manufacturer says so.</li>'
                '<li><strong>Heavy low, light high.</strong> Keep heavy stock and machines at or below waist height and light, bulky items on the top shelves.</li>'
                '<li><strong>Lockable castors.</strong> Benches and rails on lockable wheels let one room switch between making, photographing and packing.</li>'
                '<li><strong>One-way flow.</strong> Goods in at the door, work in the middle, finished orders back by the door. The 150, 180 and 300 sq ft units have roller shutters; the 160 sq ft unit has a security door.</li>'
                '<li><strong>Sockets first.</strong> Put machines near sockets and avoid chaining extension leads.</li></ul>')
    srcs = ""
    if prof.get("sources"):
        srcs = '<h2 id="sources">Official guidance</h2><ul class="source-list">' + "".join(f'<li><a class="text-link" href="{u}" target="_blank" rel="noopener noreferrer">{n}</a></li>' for n, u in prof["sources"]) + '</ul>'
    others = " · ".join(f'<a class="text-link" href="/{x["slug"]}.html">{x["short"]}</a>' for x in INDUSTRIES if x is not ind)
    main = f'''<main id="main">
{crumbs_html([(n, u.replace(SITE, "")) for n, u in crumb])}
<section class="wrap guide-hero"><p class="eyebrow">Business ideas · {ind["short"]}</p><h1>{ind["h1"][0]}<br><em>{ind["h1"][1]}</em></h1>{answer}<p class="intro">{ind["lead"]}</p><p class="guide-meta">By The Rock Factory, Blackpool · Updated {UPDATED}</p><div class="actions"><a class="button" href="{WA_H}" target="_blank" rel="noopener noreferrer">Ask if your business suits a unit</a><a class="button secondary" href="/#prices">Units and prices</a></div></section>
<section class="section wrap guide-body"><div class="guide-grid"><aside class="guide-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}{'<li><a href="#plan">Planning the floor</a></li>' if plan else ''}<li><a href="#why">Why our units suit</a></li><li><a href="#checklist">Start-up checklist</a></li><li><a href="#faq">Questions</a></li>{'<li><a href="#sources">Official guidance</a></li>' if srcs else ''}</ol></aside>
<div class="guide-content"><h2>Ideas and how to set them up</h2>{uses}{plan}
<h2 id="why">Why our units suit {ind["short"].lower()}</h2><ul class="tick-list">{"".join(f"<li>{w}</li>" for w in ind["why"])}<li>Lighting, standard single-phase electricity and Wi-Fi are already connected in every unit (there is no three-phase power), with 24-hour access, free CCTV app access covering the entrance and the area outside the units, and shared facilities.</li></ul>
<div class="callout"><h3>Not allowed in our units</h3><p>Nothing that melts or heats combustible materials such as waxes, plastics, resins or oils, no flammable liquids or gases in bulk, and no car storage. Low-risk materials such as wood, paper, card, fabric and dry goods are fine. Every business use needs our approval first.</p></div>
<h2 id="checklist">Start-up checklist</h2><ol class="steps">{"".join(f"<li><span>{c}</span></li>" for c in CHECKLIST)}</ol>
<h2 id="faq">Questions</h2><div class="faq-list">{faq_html(ind["faqs"] + GENERAL_FAQS[1:5])}</div>{srcs}
<p class="fine-print">Prices are subject to availability. Minimum rental term: one month, then one month’s notice to leave. Swap to a bigger or smaller unit any time, subject to availability. Electricity usage is charged separately at the supplier rate, with no markup. This guide is general information, not legal, insurance or tax advice.</p>
<h2>More business ideas</h2><p><a class="text-link" href="/{HUB}.html">All business ideas</a> · {others}</p></div></div></section>
</main>'''
    return page(t, slug, ind["title"], ind["desc"], crumb, main, [])


def hub_page(t):
    url = f"{SITE}/{HUB}.html"
    cards = "".join(f'<a class="idea-card" href="/{x["slug"]}.html"><h3>{x["short"]}</h3><p>{", ".join(lc(u[0]) if i else u[0] for i, u in enumerate(x["uses"][:4]))} and more.</p><span class="row-more">{len(x["uses"])} ideas →</span></a>' for x in INDUSTRIES)
    rows = ""
    for x in INDUSTRIES:
        for name, sizes, *_ in x["uses"]:
            aid = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            rows += f'<tr><th scope="row"><a href="/{x["slug"]}.html#{aid}">{name}</a></th><td>{x["short"]}</td><td>{" or ".join(f"{s} sq ft" for s in sizes)}</td></tr>'
    unit_rows = "".join(f'<tr><th scope="row"><a href="{u[0]}">{s} sq ft</a></th><td>{u[1].split(" · ", 1)[1][0].upper() + u[1].split(" · ", 1)[1][1:]}</td></tr>' for s, u in UNITS.items())
    not_ok = "".join(f"<li><strong>{h}.</strong> {d}</li>" for h, d in NOT_SUITABLE)
    sources = "".join(f'<li><a class="text-link" href="{u}" target="_blank" rel="noopener noreferrer">{n}</a></li>' for n, u in SOURCES)
    n_ideas = sum(len(x["uses"]) for x in INDUSTRIES)
    mrows = ""
    for x in INDUSTRIES:
        p = PROFILES.get(x["slug"], {}); r = p.get("rating")
        if not r: continue
        from collections import Counter
        top = Counter(u[1][0] for u in x["uses"]).most_common(1)[0][0]
        cell = lambda v, note: f'<td data-sort="{RANK[v]}"><strong class="lvl" data-level="{RANK[v]}">{v}</strong>{f"<small>{note}</small>" if note else ""}</td>'
        mrows += (f'<tr data-power="{RANK[r["power"]]}" data-layout="{RANK[r["layout"]]}" data-cost="{RANK[r["cost"]]}">'
                  f'<th scope="row" data-sort="{x["short"]}"><a href="/{x["slug"]}.html">{x["short"]}</a>{"<small>Full technical profiles</small>" if p.get("uses") else ""}</th>'
                  + cell(r["power"], p.get("power_note")) + cell(r["layout"], p.get("layout_note")) + cell(r["cost"], p.get("cost_note"))
                  + f'<td data-sort="{top}" class="nowrap">{top} sq ft</td><td data-sort="{len(x["uses"])}">{len(x["uses"])}</td></tr>')
    help_html = "".join(f"<li><strong>{h}.</strong> {d}</li>" for h, d in RATING_HELP)
    matrix = f'''<section class="section wrap" id="compare"><div class="section-head"><h2>Compare industries<br><em>at a glance</em></h2><p><strong>The lowest-risk, lowest-cost starts are online selling, trade storage and market trading. Textiles, repair and making need more power and planning but still run on standard sockets.</strong></p></div>
<div class="matrix-tools" role="group" aria-label="Filter industries" hidden><button type="button" class="filter is-on" data-filter="all" aria-pressed="true">All industries</button><button type="button" class="filter" data-filter="power" aria-pressed="false">Low power</button><button type="button" class="filter" data-filter="layout" aria-pressed="false">Simple layout</button><button type="button" class="filter" data-filter="cost" aria-pressed="false">Low set-up cost</button></div>
<div class="table-wrap"><table class="matrix" id="matrix"><caption class="sr-only">Industries compared by power need, layout complexity and set-up cost</caption><thead><tr><th scope="col" aria-sort="none"><button type="button" data-col="0">Industry</button></th><th scope="col" aria-sort="none"><button type="button" data-col="1">Power need</button></th><th scope="col" aria-sort="none"><button type="button" data-col="2">Layout</button></th><th scope="col" aria-sort="none"><button type="button" data-col="3">Set-up cost</button></th><th scope="col" aria-sort="none"><button type="button" data-col="4">Usual unit</button></th><th scope="col" aria-sort="none"><button type="button" data-col="5">Ideas</button></th></tr></thead><tbody>{mrows}</tbody></table></div>
<ul class="tick-list rating-help">{help_html}</ul></section>
<script>(()=>{{const t=document.getElementById("matrix"),tools=document.querySelector(".matrix-tools");if(!t||!tools)return;tools.hidden=false;const body=t.tBodies[0];
tools.addEventListener("click",e=>{{const b=e.target.closest("button");if(!b)return;tools.querySelectorAll("button").forEach(x=>{{x.classList.toggle("is-on",x===b);x.setAttribute("aria-pressed",x===b)}});const f=b.dataset.filter;[...body.rows].forEach(r=>{{r.hidden=f!=="all"&&r.dataset[f]!=="1"}})}});
t.tHead.addEventListener("click",e=>{{const b=e.target.closest("button");if(!b)return;const th=b.parentElement,c=+b.dataset.col,asc=th.getAttribute("aria-sort")!=="ascending";t.tHead.querySelectorAll("th").forEach(h=>h.setAttribute("aria-sort","none"));th.setAttribute("aria-sort",asc?"ascending":"descending");
const v=r=>{{const s=r.cells[c].dataset.sort;return isNaN(s)?s:+s}};[...body.rows].sort((a,b)=>{{const x=v(a),y=v(b);return (x>y?1:x<y?-1:0)*(asc?1:-1)}}).forEach(r=>body.appendChild(r))}})}})();</script>'''
    main = f'''<main id="main">
{crumbs_html([("Business ideas", f"/{HUB}.html")])}
<section class="wrap guide-hero"><p class="eyebrow">Guide for small businesses · Blackpool</p><h1>{n_ideas} business ideas<br><em>for a small unit</em></h1><div class="answer-box"><p><strong>The best businesses for a 150 to 300 sq ft unit work with dry, low-risk materials and run on standard single-phase sockets: online selling, sewing and embroidery, repair benches, makers' studios, dry goods packing and trade storage.</strong></p></div><p class="intro">Ready to move your business out of the spare room or garage? A small unit gives you a proper base with lower costs than a shop or large warehouse. Here are {n_ideas} low-risk business ideas that suit our 150 to 300 sq ft units at The Old Rock Factory, Keswick Road, with how to set each one up.</p><p class="guide-meta">By The Rock Factory, Blackpool · Updated {UPDATED}</p><div class="actions"><a class="button" href="{WA_H}" target="_blank" rel="noopener noreferrer">Ask if your business suits a unit</a><a class="button secondary" href="#compare">Compare industries</a></div></section>
{matrix}
<section class="section wrap"><div class="section-head"><h2>Ideas by<br><em>industry</em></h2><p>Choose an industry for detailed set-up guides: the best unit, layout and things to know.</p></div><div class="idea-cards">{cards}</div></section>
<section class="section wrap guide-body"><div class="guide-content wide">
<h2>What a small unit is good for</h2><p>150 sq ft is roughly the floor area of a single garage. That is enough for an online shop's stock and packing bench, one or two sewing machines and a cutting table, a repair bench with secure storage, a photography studio or a tradesperson's tools and materials. The best businesses for a small unit keep stock compact, work with dry, low-risk materials and make the most of the walls with shelving.</p>
<p>Every unit at The Rock Factory has lighting, electricity and Wi-Fi already connected. Tenants get 24-hour access, free CCTV app access covering the entrance and the area outside the units, and shared facilities: a tea and coffee room, toilets and water. You can receive mail and clients at the unit.</p>
<h2 id="which-unit">Which unit fits your business?</h2><div class="table-wrap"><table class="price-table"><thead><tr><th scope="col">Unit</th><th scope="col">Access and price</th></tr></thead><tbody>{unit_rows}</tbody></table></div>
<ul class="tick-list"><li><strong>150 sq ft, roller shutter:</strong> the starter unit for online sellers, tradespeople, repair benches and small studios.</li><li><strong>160 sq ft, security door:</strong> for small, valuable stock or quiet work: jewellery, phone repairs, trading cards, a podcast booth.</li><li><strong>180 sq ft, roller shutter:</strong> extra room for bulky stock, long fabric rolls, framing or event props.</li><li><strong>300 sq ft, two storeys:</strong> workshop or stock downstairs with an upstairs office or storage area with a window.</li></ul>
<h2>Every idea and the unit that suits it</h2><div class="table-wrap"><table class="price-table"><thead><tr><th scope="col">Business</th><th scope="col">Industry</th><th scope="col">Unit size</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>What is not allowed</h2><p>To keep the building and everyone's stock safe, some activities are not suitable. Low-risk materials such as wood, paper, card, fabric and dry goods are fine.</p><ul class="tick-list cross">{not_ok}</ul>
<h2>Making the most of a small space</h2><ul class="tick-list"><li><strong>Go up the walls.</strong> Heavy-duty shelving and wall racks free up the floor for working.</li><li><strong>Put benches on wheels.</strong> Lockable mobile benches let you switch between making and packing.</li><li><strong>Plan the flow.</strong> Goods in at the door, work in the middle, finished orders back by the door.</li><li><strong>Label everything.</strong> Clear boxes and labels save time and make stock checks easy.</li><li><strong>Keep the floor clear.</strong> A clear route to the door is safer and makes deliveries quicker.</li></ul>
<h2>Start-up checklist</h2><ol class="steps">{"".join(f"<li><span>{c}</span></li>" for c in CHECKLIST)}</ol>
<h2 id="faq">Questions</h2><div class="faq-list">{faq_html(GENERAL_FAQS)}</div>
<h2>Useful official guidance</h2><ul class="source-list">{sources}</ul>
<p class="fine-print">This guide is general information, not legal, insurance or tax advice. Prices are subject to availability. Every business use needs our approval.</p>
</div></section>
</main>'''
    extra = [{"@type": "ItemList", "name": "Business ideas by industry", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": x["short"], "url": f"{SITE}/{x['slug']}.html"} for i, x in enumerate(INDUSTRIES)]}]
    title = "Small Business Unit Ideas, Blackpool | The Rock Factory"
    desc = f"{n_ideas} low-risk business ideas for a small unit in Blackpool, from online selling to repair workshops, with set-up guides, a unit size guide and FAQs."
    return page(t, HUB, title, desc, [("Business ideas", url)], main, extra)


if __name__ == "__main__":
    t = (PUB / "storage-units-blackpool.html").read_text()
    (PUB / f"{HUB}.html").write_text(hub_page(t))
    for ind in INDUSTRIES:
        (PUB / f"{ind['slug']}.html").write_text(industry_page(t, ind))
    sm = PUB / "sitemap.xml"; x = sm.read_text()
    for slug in [HUB] + [i["slug"] for i in INDUSTRIES]:
        loc = f"{SITE}/{slug}.html"
        if loc not in x:
            x = x.replace("</urlset>", f"  <url><loc>{loc}</loc></url>\n</urlset>")
    sm.write_text(x)
    print("built hub and", len(INDUSTRIES), "industry pages,", sum(len(i["uses"]) for i in INDUSTRIES), "ideas")
