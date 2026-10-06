# The Rock Factory Blackpool – rockfactory.uk

Storage units, offices, workshops and artist studios on Keswick Road, off Park Road, Blackpool.

- `public/` – the website (plain HTML, CSS and images). Edit these files directly.
- `src/index.js` – small Cloudflare Worker: https and www → apex redirects, security headers, caching, 404 page.
- `wrangler.jsonc` – Worker `rockfactory`, serving rockfactory.uk and www.rockfactory.uk.
- `test/check.mjs` – pre-deploy checks: `node test/check.mjs`.
- `SITE-NOTES.md`, `START-HERE-BUILDER.txt` – original handover notes (content, prices, design).

Deploys: connect this repo in Cloudflare (Workers & Pages → Create → Import a repository, deploy command `npx wrangler deploy`). Every push to `main` then goes live in about 2 minutes.
