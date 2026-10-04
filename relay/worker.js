// Cloudflare Worker: relay sghir l sites li kaybloquiw IPs dyal GitHub (MAP, Barlamane, Kech24, Goud).
// Settings → Variables and Secrets: zid secret RELAY_KEY (nafs l9ima li f GitHub).
const ALLOWED = ["mapexpress.ma", "mapnews.ma", "barlamane.com", "kech24.com", "goud.ma", "alyaoum24.com", "al3omk.com"];

export default {
  async fetch(request, env) {
    if (request.headers.get("X-Relay-Key") !== env.RELAY_KEY) {
      return new Response("forbidden", { status: 403 });
    }
    const target = new URL(request.url).searchParams.get("url");
    let host;
    try {
      host = new URL(target).hostname.replace(/^www\./, "");
    } catch {
      return new Response("bad url", { status: 400 });
    }
    if (!ALLOWED.some((d) => host === d || host.endsWith("." + d))) {
      return new Response("domain not allowed", { status: 403 });
    }
    const r = await fetch(target, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
        "Accept-Language": "ar,fr;q=0.8,en;q=0.5",
      },
      redirect: "follow",
    });
    return new Response(r.body, {
      status: r.status,
      headers: { "Content-Type": r.headers.get("Content-Type") || "application/octet-stream" },
    });
  },
};
