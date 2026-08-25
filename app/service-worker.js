// JA-GALI — Service Worker (Faz 1.9)
//
// Objektif: fè app la "enstalab" (Add to Home Screen mache san sa).
// PA mete API backend la (/chat, /pwoje/fini) an kachèt — done yo dwe
// toujou fre. Sèlman fichye estatik yo (HTML/CSS/JS/ikòn) mete an kachèt.

const NON_KACHÈ = "ja-gali-v1";

const FICHYE_POU_KACHE = [
  "/index.html",
  "/style.css",
  "/app.js",
  "/manifest.json",
  "/ikon/ikon-192.png",
  "/ikon/ikon-512.png",
];

// ── Enstalasyon: mete fichye estatik yo an kachèt ────────────────────
self.addEventListener("install", (evenman) => {
  evenman.waitUntil(
    caches.open(NON_KACHÈ).then((kachè) => kachè.addAll(FICHYE_POU_KACHE))
  );
  self.skipWaiting();
});

// ── Aktivasyon: netwaye ansyen vèsyon kachè yo ───────────────────────
self.addEventListener("activate", (evenman) => {
  evenman.waitUntil(
    caches.keys().then((non_yo) =>
      Promise.all(
        non_yo
          .filter((non) => non !== NON_KACHÈ)
          .map((non) => caches.delete(non))
      )
    )
  );
  self.clients.claim();
});

// ── Fetch: estrateji "network-first" pou API, "cache-first" pou estatik
self.addEventListener("fetch", (evenman) => {
  const url = new URL(evenman.request.url);

  // JANM kache woutt API yo — done yo dwe toujou fre.
  const se_yon_woutt_api =
    url.pathname.startsWith("/chat") ||
    url.pathname.startsWith("/pwoje") ||
    url.pathname.startsWith("/sante");

  if (se_yon_woutt_api) {
    evenman.respondWith(fetch(evenman.request));
    return;
  }

  // Pou fichye estatik: eseye kachè a dabò, apre rezo a si pa jwenn.
  evenman.respondWith(
    caches.match(evenman.request).then((repons_kachè) => {
      return repons_kachè || fetch(evenman.request);
    })
  );
});
