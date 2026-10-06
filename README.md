# The Rock Factory Blackpool – rockfactory.uk

Storage units, offices, workshops and artist studios at The Old Rock Factory, Keswick Road, Blackpool FY1 5PB.

- `public/` – the website (plain HTML, CSS and images). Edit these files directly.
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
- `python3 source/compare.py` – Blackpool storage price comparison. Only built when `SHOW_COMPARISON = True` in pods.py,
  after every competitor price has been confirmed on the provider's own site (keep dated screenshots; recheck every 3 months).
