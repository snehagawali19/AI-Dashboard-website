"use client";
import { useState } from "react";
import {
  Send,
  X,
  Mail,
  Linkedin,
  MessageCircle,
  CheckCircle,
} 
from "lucide-react";
import { broadcastArticle } from "@/lib/api";
import { NewsItem, BroadcastResult } from "@/types";

const CHANNELS = [
  {
    id: "email",
    label: "Email",
    icon: Mail,
    color: "text-blue-600 bg-blue-50",
  },
  {
    id: "linkedin",
    label: "LinkedIn",
    icon: Linkedin,
    color: "text-sky-600 bg-sky-50",
  },
  {
    id: "whatsapp",
    label: "WhatsApp",
    icon: MessageCircle,
    color: "text-green-600 bg-green-50",
  },
] as const;

export default function BroadcastModal({ item }: { item: NewsItem }) {
  const [open, setOpen] = useState(false);
  const [channel, setChannel] = useState<"email" | "linkedin" | "whatsapp">(
    "email",
  );
  const [recipient, setRecipient] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BroadcastResult | null>(null);

  const handleSend = async () => {
    setLoading(true);
    try {
      const res = await broadcastArticle(item.id, channel, recipient || undefined);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setOpen(false);
    setResult(null);
    setRecipient("");
  };

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="p-1.5 rounded-lg text-gray-300 hover:text-indigo-500 hover:bg-indigo-50 transition-all"
        aria-label="Broadcast"
      >
        <Send size={15} />
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
          <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 p-6">
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
            >
              <X size={18} />
            </button>

            {result ? (
              <div className="text-center py-6">
                <CheckCircle
                  className="mx-auto text-green-500 mb-3"
                  size={40}
                />
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {result.message}
                </h3>
                <p className="text-sm text-gray-500 mb-4">
                  Sent via {result.channel}
                </p>
                {result.preview && (
                  <div className="bg-gray-50 rounded-xl p-4 text-left text-sm text-gray-600 max-h-40 overflow-y-auto">
                    <p className="text-xs text-gray-400 uppercase font-medium mb-2">
                      Preview
                    </p>
                    {result.preview}
                  </div>
                )}
                <button
                  onClick={handleClose}
                  className="mt-4 text-sm text-indigo-600 hover:underline"
                >
                  Close
                </button>
              </div>
            ) : (
              <>
                <h3 className="text-base font-semibold text-gray-900 mb-1">
                  Broadcast article
                </h3>
                <p className="text-sm text-gray-400 mb-5 line-clamp-1">
                  {item.title}
                </p>

                {/* Channel picker */}
                <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                  Channel
                </p>
                <div className="grid grid-cols-3 gap-2 mb-5">
                  {CHANNELS.map(({ id, label, icon: Icon, color }) => (
                    <button
                      key={id}
                      onClick={() => setChannel(id)}
                      className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border-2 transition-all text-sm font-medium
                        ${
                          channel === id
                            ? `border-indigo-400 ${color}`
                            : "border-gray-100 text-gray-400 hover:border-gray-200"
                        }`}
                    >
                      <Icon size={18} />
                      {label}
                    </button>
                  ))}
                </div>

                {/* Recipient (optional for email/whatsapp) */}
                {channel !== "linkedin" && (
                  <>
                    <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                      {channel === "email"
                        ? "Recipient email"
                        : "WhatsApp number"}
                    </p>
                    <input
                      type={channel === "email" ? "email" : "tel"}
                      placeholder={
                        channel === "email"
                          ? "you@example.com"
                          : "+91xxxxxxxxxx"
                      }
                      value={recipient}
                      onChange={(e) => setRecipient(e.target.value)}
                      className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-700 mb-5
                                 focus:outline-none focus:ring-2 focus:ring-indigo-300"
                    />
                  </>
                )}

                <button
                  onClick={handleSend}
                  disabled={loading}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60
                             text-white font-medium py-2.5 rounded-xl transition-colors text-sm"
                >
                  {loading ? "Sending…" : `Send via ${channel}`}
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
}
