# The Rock Factory Blackpool – rockfactory.uk

Storage units, offices, workshops and artist studios at The Old Rock Factory, Keswick Road, Blackpool FY1 5PB.

- `public/` – the website (plain HTML, CSS and images). Edit these files directly.
- `public/motion.js` – optional motion (scroll reveals, footer marquee, mouse cursor, magnetic buttons). Added to every page by `source/layout.py`. It never changes page text, the headline or the hero photo, uses transform/opacity only (no layout shift) and switches off for reduced motion.
- `src/index.js` – small Cloudflare Worker: https and www → apex redirects, security headers, caching, 404 page.
- `wrangler.jsonc` – Worker `rockfactory`, serving rockfactory.uk and www.rockfactory.uk.
- `test/check.mjs` – pre-deploy checks: `node test/check.mjs`.
- `SITE-NOTES.md`, `START-HERE-BUILDER.txt` – original handover notes (content, prices, design).

Deploys: connect this repo in Cloudflare (Workers & Pages → Create → Import a repository, deploy command `npx wrangler deploy`). Every push to `main` then goes live in about 2 minutes.

## Page generators (run from the repo root)

- `python3 source/units.py` – one page per unit (photos in public/assets), links homepage price rows and storage cards.
- `python3 source/ideas.py` – business ideas guide and industry pages.
- `python3 source/community.py` – Our businesses directory and IceWork profile.
- `python3 source/pods.py` – first-floor storage pods page and guide prices.
- `python3 source/guides.py` – storage guides, business guides, Fylde coast area pages and core pages (about, find us,
  rental terms, FAQs, glossary, compare units, prices explained, rock history) from `source/content/*.json`.
  `source/content/BRIEF.md` lists the only business facts the copy may state. New industries go in `content/industries.json` (read by ideas.py).
- `python3 source/layout.py` – run LAST after any generator: one nav and footer on every page, speculation rules,
  and rebuilds `sitemap.xml` and `llms.txt` from the pages.
- `python3 source/compare.py` – Blackpool storage price comparison. Only built when `SHOW_COMPARISON = True` in pods.py,
  after every competitor price has been confirmed on the provider's own site (keep dated screenshots; recheck every 3 months).

## Storage pod photos

Save the three pod pictures as WebP in `public/assets/` (optionally with an `-800.webp` phone-size copy):
`storage-pods-blackpool-row.webp`, `storage-pod-fitting-blackpool.webp`, `storage-pod-interior-blackpool.webp`.
Then run `python3 source/pods.py && python3 source/layout.py`. The gallery, alt text, captions and image sitemap
entries appear automatically (descriptions live in `POD_PHOTOS` in `source/pods.py`).

## Photo SEO

Each photo gets alt text written for the page it appears on (`IMAGE_ALT` in `source/layout.py`), the page's main
photo is declared as `primaryImageOfPage`, and every content photo is listed in `sitemap.xml` as an image entry.
If a page's photos change, the build prints a warning until `IMAGE_ALT` is updated for that page.
