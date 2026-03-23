"use client";
import { useState } from "react";
import {
  Heart,
  Mail,
  Linkedin,
  MessageCircle,
  ExternalLink,
  Tag,
  ChevronDown,
  ChevronUp,
  Bot,
  Loader2,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { NewsItem } from "@/types";
import { toggleFavorite, broadcastArticle } from "@/lib/api";
import clsx from "clsx";

interface Props {
  item: NewsItem;
  onFavoriteToggle?: (id: string, nowFavorited: boolean) => void;
}

const CATEGORY_COLORS: Record<string, string> = {
  tech: "bg-blue-100 text-blue-700",
  research: "bg-purple-100 text-purple-700",
  news: "bg-orange-100 text-orange-700",
  education: "bg-green-100 text-green-700",
  newsletter: "bg-pink-100 text-pink-700",
  general: "bg-gray-100 text-gray-600",
};

const PLATFORMS = [
  { key: "email", Icon: Mail, label: "Email", idle: "text-gray-400 hover:text-blue-600 hover:bg-blue-50" },
  { key: "linkedin", Icon: Linkedin, label: "LinkedIn", idle: "text-gray-400 hover:text-blue-700 hover:bg-blue-50" },
  { key: "whatsapp", Icon: MessageCircle, label: "WhatsApp", idle: "text-gray-400 hover:text-green-600 hover:bg-green-50" },
] as const;

type Platform = (typeof PLATFORMS)[number]["key"];

export default function NewsCard({ item, onFavoriteToggle }: Props) {
  const [favorited, setFavorited] = useState(item.is_favorited);
  const [favLoading, setFavLoading] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [broadcasting, setBroadcasting] = useState<Platform | null>(null);
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const [toastError, setToastError] = useState(false);

  const handleFavorite = async () => {
    setFavLoading(true);
    try {
      const ok = await toggleFavorite(item.id, favorited);
      if (ok) {
        setFavorited(!favorited);
        onFavoriteToggle?.(item.id, !favorited);
      }
    } finally {
      setFavLoading(false);
    }
  };

  const handleQuickBroadcast = async (platform: Platform) => {
    if (broadcasting) return;
    setBroadcasting(platform);
    setToastMsg(null);
    try {
      await broadcastArticle(item.id, platform);
      setToastError(false);
      setToastMsg(`✓ Broadcast via ${platform}`);
    } catch {
      setToastError(true);
      setToastMsg("Broadcast failed — try again");
    } finally {
      setBroadcasting(null);
      setTimeout(() => setToastMsg(null), 3000);
    }
  };

  const catColor = CATEGORY_COLORS[item.category ?? "general"] ?? CATEGORY_COLORS.general;
  const timeAgo = formatDistanceToNow(new Date(item.published_at ?? item.created_at ?? new Date()), { addSuffix: true });

  return (
    <article className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow flex flex-col">

      {item.image_url && (
        <div className="h-40 bg-gray-100 overflow-hidden flex-shrink-0">
          <img
            src={item.image_url}
            alt={item.title}
            className="w-full h-full object-cover"
            onError={(e) => ((e.currentTarget as HTMLImageElement).style.display = "none")}
          />
        </div>
      )}

      <div className="p-4 flex flex-col flex-1">

        <div className="flex items-center justify-between mb-2 flex-wrap gap-1">
          <div className="flex items-center gap-2 min-w-0">
            {item.category && (
              <span className={clsx("text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0", catColor)}>
                {item.category}
              </span>
            )}
            {item.source && (
              <span className="text-xs text-gray-400 truncate">{item.source.name}</span>
            )}
          </div>
          <span className="text-xs text-gray-400 flex-shrink-0">{timeAgo}</span>
        </div>

        <a href={item.url} target="_blank" rel="noopener noreferrer" className="group block mb-2">
          <h2 className="text-sm font-semibold text-gray-900 leading-snug group-hover:text-indigo-600 transition-colors line-clamp-3">
            {item.title}
          </h2>
        </a>

        {item.summary && (
          <div className="mb-3">
            <button
              onClick={() => setShowSummary((v) => !v)}
              className="flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-700 font-medium"
            >
              <Bot className="w-3 h-3" />
              AI Summary
              {showSummary ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </button>
            {showSummary && (
              <p className="mt-1.5 text-xs text-gray-600 leading-relaxed bg-indigo-50 rounded-lg p-2.5 border border-indigo-100">
                {item.summary}
              </p>
            )}
          </div>
        )}

        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {item.tags.slice(0, 4).map((tag) => (
              <span key={tag} className="flex items-center gap-0.5 text-xs bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded">
                <Tag className="w-2.5 h-2.5" />
                {tag}
              </span>
            ))}
          </div>
        )}

        <div className="flex-1" />

        {toastMsg && (
          <div className={clsx(
            "mb-2 text-xs text-center rounded-lg py-1.5 px-2 border",
            toastError
              ? "bg-red-50 text-red-700 border-red-100"
              : "bg-green-50 text-green-700 border-green-100"
          )}>
            {toastMsg}
          </div>
        )}

        <div className="flex items-center justify-between pt-2 border-t border-gray-100">


          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-indigo-600 transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            Read article
          </a>

        <div className="flex items-center gap-1">
          {PLATFORMS.map(({ key, Icon, label, idle }) => (
            <button
              key={key}
              onClick={() => handleQuickBroadcast(key)}
              disabled={!!broadcasting}
              title={`Broadcast via ${label}`}
              className={clsx("p-1.5 rounded-lg transition-colors disabled:opacity-40", broadcasting === key ? "opacity-60" : idle)}
            >
              {broadcasting === key
                ? <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
                : <Icon className="w-4 h-4" />}
            </button>
          ))}

          <span className="w-px h-4 bg-gray-200 mx-0.5" />

          <button
            onClick={handleFavorite}
            disabled={favLoading}
            title={favorited ? "Remove from favorites" : "Save to favorites"}
            className={clsx(
              "p-1.5 rounded-lg transition-colors",
              favorited ? "text-red-500 bg-red-50 hover:bg-red-100" : "text-gray-400 hover:text-red-400 hover:bg-red-50"
            )}
          >
            {favLoading
              ? <Loader2 className="w-4 h-4 animate-spin" />
              : <Heart className={clsx("w-4 h-4", favorited && "fill-current")} />}
          </button>
        </div>

      </div>
    </div>
    </article >
  );
}