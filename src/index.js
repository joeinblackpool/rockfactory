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

async function rockFactory(request, env) {
  const url = new URL(request.url);
  if (url.hostname !== RF_DOMAIN || url.protocol === "http:") {
    return Response.redirect(`https://${RF_DOMAIN}${url.pathname}${url.search}`, 301);
  }
  if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405, headers: { allow: "GET, HEAD" } });
  if (url.pathname === "/index.html" || url.pathname === "/index") return Response.redirect(`https://${RF_DOMAIN}/`, 301);
  if (!env || !env.ASSETS) return new Response("Site files unavailable", { status: 503 });
  const path = url.pathname === "/" ? "/index.html" : url.pathname;
  const res = await env.ASSETS.fetch(new Request(new URL(path, url.origin), request));
  if (res.ok) return withHeaders(res);
  const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url.origin), request));
  return withHeaders(nf, 404);
}

export default { fetch: (request, env) => rockFactory(request, env) };
