// rockfactory.uk – The Rock Factory, Blackpool (storage units, offices, workshops).
// Static site in public/, served by this Worker so it can add redirects,
// security headers, caching and a real 404 status.
const RF_DOMAIN = "rockfactory.uk";

const SECURITY = {
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "strict-origin-when-cross-origin",
  "permissions-policy": "camera=(), microphone=(), geolocation=()",
};

const withHeaders = (res, status = res.status) => {
  const h = new Headers(res.headers);
  for (const [k, v] of Object.entries(SECURITY)) h.set(k, v);
  const type = h.get("content-type") || "";
  h.set("cache-control", type.startsWith("text/html") ? "public, max-age=300" : /image|font|css/.test(type) ? "public, max-age=2592000" : "public, max-age=3600");
  return new Response(res.body, { status, headers: h });
};

// Old page addresses that moved: 301 so links and search results keep working.
const REDIRECTS = { "/storage-units-blackpool-spring-2027.html": "/storage-pods-blackpool.html" };

async function rockFactory(request, env) {
  const url = new URL(request.url);
  if (url.hostname !== RF_DOMAIN || url.protocol === "http:") {
    return Response.redirect(`https://${RF_DOMAIN}${url.pathname}${url.search}`, 301);
  }
  if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405, headers: { allow: "GET, HEAD" } });
  if (REDIRECTS[url.pathname]) return Response.redirect(`https://${RF_DOMAIN}${REDIRECTS[url.pathname]}`, 301);
  if (url.pathname === "/index.html" || url.pathname === "/index") return Response.redirect(`https://${RF_DOMAIN}/`, 301);
  if (!env || !env.ASSETS) return new Response("Site files unavailable", { status: 503 });
  const path = url.pathname === "/" ? "/index.html" : url.pathname;
  const res = await env.ASSETS.fetch(new Request(new URL(path, url.origin), request));
  if (res.ok) return withHeaders(res);
  const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin), request));
  return withHeaders(nf, 404);
}

// IndexNow: tell Bing (and other IndexNow engines) about every sitemap URL once per deployed
// version. The hourly cron compares this version's id with the last one submitted (KV STATE).
const INDEXNOW_KEY = "ab2e9527cde882f3c42f6dacb1fe418b";
async function submitIndexNow(env) {
  const version = env.CF_VERSION_METADATA && env.CF_VERSION_METADATA.id;
  if (!version || !env.STATE || !env.ASSETS) return;
  if ((await env.STATE.get("indexnow-version")) === version) return;
  const sm = await (await env.ASSETS.fetch(new Request(`https://${RF_DOMAIN}/sitemap.xml`))).text();
  const urlList = [...sm.matchAll(/<loc>(.*?)<\/loc>/g)].map((m) => m[1]);
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST",
    headers: { "content-type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: RF_DOMAIN, key: INDEXNOW_KEY, keyLocation: `https://${RF_DOMAIN}/${INDEXNOW_KEY}.txt`, urlList }),
  });
  console.log("IndexNow", res.status, urlList.length);
  if (res.ok) await env.STATE.put("indexnow-version", version);
}

export default {
  fetch: (request, env) => rockFactory(request, env),
  scheduled: (event, env, ctx) => ctx.waitUntil(submitIndexNow(env)),
};
