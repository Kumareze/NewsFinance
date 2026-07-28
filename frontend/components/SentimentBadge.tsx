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
  positive: "bg-green-900/50 text-green-400 border-green-700",
  negative: "bg-red-900/50 text-red-400 border-red-700",
  neutral: "bg-gray-700/50 text-gray-300 border-gray-600",
};

export default function SentimentBadge({ sentiment, confidence }: SentimentBadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border",
        SENTIMENT_STYLES[sentiment]
      )}
    >
      <span
        className={clsx("w-1.5 h-1.5 rounded-full", {
          "bg-green-400": sentiment === "positive",
          "bg-red-400": sentiment === "negative",
          "bg-gray-400": sentiment === "neutral",
        })}
      />
      {SENTIMENT_LABELS[sentiment]}
      {confidence !== undefined && (
        <span className="opacity-60 ml-0.5">({(confidence * 100).toFixed(0)}%)</span>
      )}
    </span>
  );
}