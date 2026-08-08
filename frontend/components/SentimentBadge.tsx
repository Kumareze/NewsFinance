"use client";

import React from "react";
import clsx from "clsx";

type Sentiment = "positive" | "negative" | "neutral";

interface SentimentBadgeProps {
  sentiment: Sentiment;
  confidence?: number;
}

const SENTIMENT_LABELS: Record<Sentiment, string> = {
  positive: "Positive",
  negative: "Negative",
  neutral: "Neutral",
};

const SENTIMENT_STYLES: Record<Sentiment, string> = {
  positive: "bg-[#22C55E]/10 text-[#22C55E] border-[#22C55E]/20",
  negative: "bg-[#EF4444]/10 text-[#EF4444] border-[#EF4444]/20",
  neutral: "bg-[#71717A]/10 text-[#A1A1AA] border-[#3F3F46]",
};

export default function SentimentBadge({ sentiment, confidence }: SentimentBadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[12px] font-semibold uppercase tracking-wider border",
        SENTIMENT_STYLES[sentiment]
      )}
    >
      <span
        className={clsx("w-1.5 h-1.5 rounded-full", {
          "bg-[#22C55E]": sentiment === "positive",
          "bg-[#EF4444]": sentiment === "negative",
          "bg-[#71717A]": sentiment === "neutral",
        })}
      />
      {SENTIMENT_LABELS[sentiment]}
      {confidence !== undefined && (
        <span className="opacity-60 ml-0.5 normal-case font-normal">
          ({(confidence * 100).toFixed(0)}%)
        </span>
      )}
    </span>
  );
}
