"use client";
import Link from "next/link";
import { Zap, Heart, BarChart2 } from "lucide-react";
import clsx from "clsx";

export default function NavBar({
  activeTab,
}: {
  activeTab: "feed" | "favorites";
}) {
  return (
    <nav className="sticky top-0 z-40 bg-white/80 backdrop-blur border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Zap size={20} className="text-indigo-600" />
          <span className="font-bold text-gray-900 text-base tracking-tight">
            AI News<span className="text-indigo-600">Pulse</span>
          </span>
        </div>
        <div className="flex items-center gap-1">
          <Link
            href="/"
            className={clsx(
              "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition",
              activeTab === "feed"
                ? "text-indigo-600 bg-indigo-50"
                : "text-gray-500 hover:text-gray-900 hover:bg-gray-50",
            )}
          >
            <BarChart2 size={15} /> Feed
          </Link>
          <Link
            href="/favorites"
            className={clsx(
              "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition",
              activeTab === "favorites"
                ? "text-rose-500 bg-rose-50"
                : "text-gray-500 hover:text-gray-900 hover:bg-gray-50",
            )}
          >
            <Heart size={15} /> Favorites
          </Link>
        </div>
      </div>
    </nav>
  );
}
