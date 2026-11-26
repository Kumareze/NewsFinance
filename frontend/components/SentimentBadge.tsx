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
  positive: "bg-positive/10 text-positive border-positive/20",
  negative: "bg-negative/10 text-negative border-negative/20",
  neutral: "bg-muted/10 text-text-secondary border-border",
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
          "bg-positive": sentiment === "positive",
          "bg-negative": sentiment === "negative",
          "bg-muted": sentiment === "neutral",
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
