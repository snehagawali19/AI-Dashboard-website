"use client";
import { useState, useEffect } from "react";
import { fetchFavorites } from "@/lib/api";
import { Favorite } from "@/types";
import NavBar from "@/components/NavBar";
import NewsCard from "@/components/NewsCard";
import { Heart } from "lucide-react";

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFavorites()
      .then((f: Favorite[]) => setFavorites(f))
      .catch((err: any) => console.error("Error fetching favorites:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleFavoriteToggle = (id: string) => {
    setFavorites((prev) => prev.filter((f) => f.news_item.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar activeTab="favorites" />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center gap-3 mb-6">
          <Heart className="text-rose-500" size={22} fill="currentColor" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Favorites</h1>
            <p className="text-sm text-gray-400">
              {favorites.length} saved article
              {favorites.length !== 1 ? "s" : ""}
            </p>
          </div>
        </div>

        {loading ? (
          <p className="text-gray-400">Loading…</p>
        ) : favorites.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
            <Heart size={48} className="mx-auto mb-3 opacity-30" />
            <p>
              No favorites yet. Heart articles from the feed to save them here.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {favorites.map((f) => (
              <NewsCard
                key={f.id}
                item={{ ...f.news_item, is_favorited: true }}
                onFavoriteToggle={() => handleFavoriteToggle(f.news_item.id)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
