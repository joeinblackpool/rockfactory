// Pre-deploy checks against the Worker with public/ as its assets: every sitemap page 200,
// unique titles, one <h1>, valid JSON-LD, no broken internal links or images, redirects behave.
// Run: node test/check.mjs
import { readFile } from "node:fs/promises";
import { extname, join } from "node:path";
import worker from "../src/index.js";

const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".webp": "image/webp", ".svg": "image/svg+xml", ".xml": "application/xml", ".txt": "text/plain" };
const ASSETS = {
  async fetch(req) {
    const p = decodeURIComponent(new URL(req.url).pathname);
    try { return new Response(await readFile(join("public", p)), { headers: { "content-type": TYPES[extname(p)] || "application/octet-stream" } }); }
    catch { return new Response("not found", { status: 404 }); }
  },
};
const get = (u) => worker.fetch(new Request(u, { redirect: "manual" }), { ASSETS });
let bad = 0; const fail = (m) => { bad++; console.log("FAIL", m); };
const site = "https://rockfactory.uk";

const sm = await (await get(`${site}/sitemap.xml`)).text();
const locs = [...sm.matchAll(/<loc>(.*?)<\/loc>/g)].map((m) => m[1]);
if (new Set(locs).size !== locs.length) fail("duplicate sitemap URLs");
const titles = new Set(); const refs = new Set();
for (const loc of locs) {
  const r = await get(loc); const html = await r.text();
  if (r.status !== 200) { fail(`${loc} status ${r.status}`); continue; }
  const title = html.match(/<title>(.*?)<\/title>/)[1];
  if (titles.has(title)) fail(`duplicate title ${title}`); titles.add(title);
  if ((html.match(/<h1/g) || []).length !== 1) fail(`${loc} h1 count`);
  const canon = html.match(/rel="canonical" href="(.*?)"/)?.[1];
  if (canon !== loc) fail(`${loc} canonical ${canon}`);
  for (const m of html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)) { try { JSON.parse(m[1]); } catch { fail(`${loc} JSON-LD`); } }
  for (const m of html.matchAll(/(?:href|src)="([^"#:]+?)(?:\?[^"]*)?"/g)) refs.add(new URL(m[1], loc).href);
  console.log(`${r.status} ${new URL(loc).pathname.padEnd(36)} ${title}`);
}
for (const u of refs) { const r = await get(u); if (r.status !== 200) fail(`link ${u} -> ${r.status}`); }
const expect = async (u, status, loc) => { const r = await get(u); if (r.status !== status || (loc && r.headers.get("location") !== loc)) fail(`${u} -> ${r.status} ${r.headers.get("location")}`); };
await expect("http://rockfactory.uk/offices-to-let-blackpool.html", 301, `${site}/offices-to-let-blackpool.html`);
await expect("https://www.rockfactory.uk/", 301, `${site}/`);
await expect(`${site}/index.html`, 301, `${site}/`);
await expect(`${site}/nope`, 404);
await expect(`${site}/a/b/c`, 404);
await expect(`${site}/robots.txt`, 200);
const home = await get(`${site}/`);
if (!home.headers.get("strict-transport-security")) fail("no HSTS");
console.log(`\n${locs.length} pages, ${refs.size} links and images checked, ${bad} problems`);
process.exit(bad ? 1 : 0);
