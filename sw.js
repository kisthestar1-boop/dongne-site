/* 동네미팅 앱 설치·오프라인용 서비스 워커 */
const V = "dm-v4";
const FILES = ["./", "./index.html", "./match.html", "./game.html", "./td.html", "./td-manifest.json", "./game-manifest.json", "./game-icon-192.png", "./game-icon-512.png", "./config.js", "./manifest.json", "./icon-192.png", "./icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(V).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || (u.origin !== location.origin && u.host !== "cdn.jsdelivr.net")) return; // 신청 저장 등은 항상 인터넷으로
  // 새 내용 먼저, 인터넷이 없으면 저장본
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(V).then(x => x.put(e.request, c)); return r; })
    .catch(() => caches.match(e.request)));
});
