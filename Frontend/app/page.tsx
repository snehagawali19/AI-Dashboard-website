"use client";
import { useState, useEffect, useCallback } from "react";
import { fetchNews, triggerIngest } from "@/lib/api";
import { NewsItem, PaginatedNews } from "@/types";
import NewsCard from "@/components/NewsCard";
import NavBar from "@/components/NavBar";
import SkeletonCard from "@/components/SkeletonCard";
import { RefreshCw } from "lucide-react";

export default function HomePage() {
  const [data, setData] = useState<PaginatedNews | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [ingesting, setIngesting] = useState(false);
  const [tag, setTag] = useState<string | undefined>();

  const load = useCallback(async (p = 1, t?: string) => {
    setLoading(true);
    try {
      const res = await fetchNews({ page: p, page_size: 20, tag: t });
      setData(res);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load(1, tag);
  }, [tag]);

  const handleIngest = async () => {
    setIngesting(true);
    await triggerIngest().catch(console.error);
    await load(1, tag);
    setIngesting(false);
  };

  const handleFavoriteToggle = (id: string, nowFavorited: boolean) => {
    setData((prev) =>
      prev
        ? {
            ...prev,
            items: prev.items.map((item) =>
              item.id === id ? { ...item, is_favorited: nowFavorited } : item,
            ),
          }
        : prev,
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar activeTab="feed" />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AI News Feed</h1>
            <p className="text-sm text-gray-400 mt-0.5">
              {data ? `${data.total} articles from 20+ sources` : "Loading…"}
            </p>
          </div>
          <button
            onClick={handleIngest}
            disabled={ingesting}
            className="flex items-center gap-2 text-sm bg-indigo-600 text-white px-4 py-2 rounded-xl
                       hover:bg-indigo-700 disabled:opacity-60 transition-colors"
          >
            <RefreshCw size={14} className={ingesting ? "animate-spin" : ""} />
            {ingesting ? "Fetching…" : "Fetch latest"}
          </button>
        </div>

        {/* Tag filter pills */}
        {data && (
          <div className="flex gap-2 mb-6 flex-wrap">
            {[
              "llm",
              "openai",
              "robotics",
              "research",
              "benchmark",
              "agents",
            ].map((t) => (
              <button
                key={t}
                onClick={() => setTag(tag === t ? undefined : t)}
                className={`text-xs px-3 py-1 rounded-full border transition-all
                  ${
                    tag === t
                      ? "bg-indigo-600 text-white border-indigo-600"
                      : "bg-white text-gray-500 border-gray-200 hover:border-indigo-300"
                  }`}
              >
                #{t}
              </button>
            ))}
          </div>
        )}

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {loading
            ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
            : data?.items.map((item) => (
                <NewsCard
                  key={item.id}
                  item={item}
                  onFavoriteToggle={handleFavoriteToggle}
                />
              ))}
        </div>

        {/* Pagination */}
        {data && (
          <div className="flex justify-center gap-3 mt-10">
            <button
              disabled={page === 1 || loading}
              onClick={() => {
                setPage(page - 1);
                load(page - 1, tag);
              }}
              className="px-4 py-2 text-sm rounded-xl border border-gray-200 disabled:opacity-40 hover:bg-white transition"
            >
              ← Previous
            </button>
            <span className="px-4 py-2 text-sm text-gray-400">
              Page {data.page} of {Math.ceil(data.total / data.per_page)}
            </span>
            <button
              disabled={!data.has_more || loading}
              onClick={() => {
                setPage(page + 1);
                load(page + 1, tag);
              }}
              className="px-4 py-2 text-sm rounded-xl border border-gray-200 disabled:opacity-40 hover:bg-white transition"
            >
              Next →
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
