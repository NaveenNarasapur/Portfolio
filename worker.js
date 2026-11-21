// Cloudflare Worker: serves the static site and a tiny visit-counter API backed by D1.
// Table: CREATE TABLE visits (id INTEGER PRIMARY KEY, count INTEGER NOT NULL DEFAULT 0);
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/visit") {
      if (request.method !== "GET") {
        return new Response("Method Not Allowed", { status: 405, headers: { Allow: "GET" } });
      }
      try {
        // ?read=1 returns the count without incrementing.
        const row = url.searchParams.has("read")
          ? await env.DB.prepare("SELECT count FROM visits WHERE id = 1").first()
          // Single atomic statement: no read-after-write race between concurrent visitors.
          : await env.DB.prepare("UPDATE visits SET count = count + 1 WHERE id = 1 RETURNING count").first();
        if (!row) return Response.json({ error: "counter not initialised" }, { status: 500 });
        return Response.json({ count: row.count }, { headers: { "Cache-Control": "no-store" } });
      } catch (err) {
        console.error("visit counter error", err);
        return Response.json({ error: "unavailable" }, { status: 503 });
      }
    }

    return env.ASSETS.fetch(request);
  },
};
