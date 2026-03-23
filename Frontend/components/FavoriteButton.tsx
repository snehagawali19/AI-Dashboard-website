"use client";
import { useState } from "react";
import { Heart } from "lucide-react";
import { toggleFavorite } from "@/lib/api";
import clsx from "clsx";

interface Props {
  itemId: string;
  isFavorited: boolean;
  onToggle?: (id: string, nowFavorited: boolean) => void;
}

export default function FavoriteButton({
  itemId,
  isFavorited,
  onToggle,
}: Props) {
  const [favorited, setFavorited] = useState(isFavorited);
  const [loading, setLoading] = useState(false);

  const toggle = async () => {
    if (loading) return;
    setLoading(true);
    try {
      if (favorited) {
        await toggleFavorite(itemId, true);
        setFavorited(false);
        onToggle?.(itemId, false);
      } else {
        await toggleFavorite(itemId, false);
        setFavorited(true);
        onToggle?.(itemId, true);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={toggle}
      disabled={loading}
      className={clsx(
        "p-1.5 rounded-lg transition-all duration-150",
        favorited
          ? "text-rose-500 bg-rose-50 hover:bg-rose-100"
          : "text-gray-300 hover:text-rose-400 hover:bg-rose-50",
      )}
      aria-label={favorited ? "Remove from favorites" : "Add to favorites"}
    >
      <Heart
        size={16}
        className={clsx("transition-all", loading && "opacity-50")}
        fill={favorited ? "currentColor" : "none"}
      />
    </button>
  );
}
