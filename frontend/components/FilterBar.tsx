"use client";

import React from "react";
import clsx from "clsx";

type SentimentFilter = "" | "positive" | "negative" | "neutral";
type SortOption = "latest" | "oldest" | "positive" | "negative";

interface FilterBarProps {
  sentiment: SentimentFilter;
  sort: SortOption;
  onSentimentChange: (s: SentimentFilter) => void;
  onSortChange: (s: SortOption) => void;
}

const SENTIMENT_OPTIONS: { label: string; value: SentimentFilter }[] = [
  { label: "All", value: "" },
  { label: "Positive", value: "positive" },
  { label: "Negative", value: "negative" },
  { label: "Neutral", value: "neutral" },
];

const SORT_OPTIONS: { label: string; value: SortOption }[] = [
  { label: "Latest", value: "latest" },
  { label: "Oldest", value: "oldest" },
  { label: "Most Positive", value: "positive" },
  { label: "Most Negative", value: "negative" },
];

export default function FilterBar({
  sentiment,
  sort,
  onSentimentChange,
  onSortChange,
}: FilterBarProps) {
  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 w-full">
      {/* Sentiment filters */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs text-[#71717A] font-medium mr-1">Sentiment:</span>
        {SENTIMENT_OPTIONS.map((opt) => (
          <button
            key={opt.value}
            onClick={() => onSentimentChange(opt.value)}
            className={clsx(
              "px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors",
              sentiment === opt.value
                ? "bg-[#22C55E]/10 text-[#22C55E] border-[#22C55E]/30"
                : "bg-[#27272A] text-[#A1A1AA] border-[#3F3F46] hover:border-[#22C55E]/50"
            )}
          >
            {opt.label}
          </button>
        ))}
      </div>

      {/* Sort */}
      <div className="flex items-center gap-2 flex-wrap sm:ml-auto">
        <span className="text-xs text-[#71717A] font-medium mr-1">Sort:</span>
        <select
          value={sort}
          onChange={(e) => onSortChange(e.target.value as SortOption)}
          className="bg-[#27272A] border border-[#3F3F46] rounded-lg px-3 py-1.5 text-xs text-[#FAFAFA] focus:outline-none focus:border-[#22C55E] cursor-pointer"
        >
          {SORT_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}