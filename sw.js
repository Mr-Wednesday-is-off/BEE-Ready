// Bee Ready service worker: keeps the app usable with no internet.
// The page itself is fetched fresh whenever there's a connection, so updates
// pushed to GitHub show up on the next open. Icons and fonts rarely change;
// bump ASSET_CACHE if you replace them.
const ASSET_CACHE = "bee-ready-assets-v1";
const PAGE_CACHE = "bee-ready-page";
const ASSETS = [
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  "icons/apple-touch-icon.png",
  "fonts/baloo-2-latin-600-normal.woff2",
  "fonts/baloo-2-latin-700-normal.woff2",
  "fonts/baloo-2-latin-800-normal.woff2",
  "fonts/atkinson-hyperlegible-latin-400-normal.woff2",
  "fonts/atkinson-hyperlegible-latin-700-normal.woff2",
  "fonts/atkinson-hyperlegible-latin-400-italic.woff2"
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const assets = await caches.open(ASSET_CACHE);
    await assets.addAll(ASSETS);
    const page = await caches.open(PAGE_CACHE);
    await page.add("./");
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key !== ASSET_CACHE && key !== PAGE_CACHE) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});

// Fresh page when online (gives up after 3 seconds on a weak signal), cached page otherwise
async function pageRequest(request) {
  const cache = await caches.open(PAGE_CACHE);
  try {
    const fresh = await Promise.race([
      fetch(request),
      new Promise((_, reject) => setTimeout(() => reject(new Error("slow")), 3000))
    ]);
    if (fresh.ok) cache.put("./", fresh.clone());
    return fresh;
  } catch (e) {
    return (await cache.match("./")) || Response.error();
  }
}

async function assetRequest(request) {
  const hit = await caches.match(request);
  if (hit) return hit;
  const res = await fetch(request);
  if (res.ok) (await caches.open(ASSET_CACHE)).put(request, res.clone());
  return res;
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET" || new URL(request.url).origin !== location.origin) return;
  event.respondWith(request.mode === "navigate" ? pageRequest(request) : assetRequest(request));
});
