const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const SESSION = "default";

export async function fetchNews(params?: {
  page?: number;
  page_size?: number;
  category?: string;
  tag?: string;
  search?: string;
}) {
  const url = new URL(`${BASE_URL}/api/news/`);
  url.searchParams.append("page", String(params?.page || 1));
  url.searchParams.append("page_size", String(params?.page_size || 30));
  url.searchParams.append("user_session", SESSION);
  if (params?.category) url.searchParams.append("category", params.category);
  if (params?.tag) url.searchParams.append("tag", params.tag);
  if (params?.search) url.searchParams.append("search", params.search);

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error("Failed to fetch news");
  return res.json();
}

export async function fetchStats() {
  const res = await fetch(`${BASE_URL}/api/news/stats`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

export async function fetchFavorites() {
  const res = await fetch(`${BASE_URL}/api/favorites/?user_session=${SESSION}`);
  if (!res.ok) throw new Error("Failed to fetch favorites");
  return res.json();
}

export async function toggleFavorite(newsItemId: string, isFavorited: boolean) {
  if (isFavorited) {
    const res = await fetch(
      `${BASE_URL}/api/favorites/${newsItemId}?user_session=${SESSION}`,
      { method: "DELETE" }
    );
    return res.ok;
  } else {
    const res = await fetch(`${BASE_URL}/api/favorites/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ news_item_id: newsItemId, user_session: SESSION }),
    });
    return res.ok;
  }
}

export async function broadcastArticle(
  newsItemId: string,
  platform: string,
  recipient?: string
) {
  const res = await fetch(`${BASE_URL}/api/broadcast/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      news_item_id: newsItemId,
      platform,
      recipient: recipient || null,
      user_session: SESSION,
    }),
  });
  if (!res.ok) throw new Error("Broadcast failed");
  return res.json();
}

export async function generateCaption(newsItemId: string, platform: string) {
  const res = await fetch(`${BASE_URL}/api/ai/caption`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ news_item_id: newsItemId, platform }),
  });
  if (!res.ok) throw new Error("Caption generation failed");
  return res.json();
}

export async function triggerIngest() {
  const res = await fetch(`${BASE_URL}/api/ingest`, { method: "POST" });
  return res.json();
}

export async function fetchBroadcastLogs() {
  const res = await fetch(`${BASE_URL}/api/broadcast/?limit=50`);
  if (!res.ok) throw new Error("Failed to fetch broadcast logs");
  return res.json();
}