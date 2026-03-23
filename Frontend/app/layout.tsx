import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI NewsPulse — Aggregated AI News Dashboard",
  description:
    "Real-time AI news from 20+ sources with AI summaries and broadcasting.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
<html lang="en">
    <body className="antialiased">{children}</body>
    </html>
  );
}
