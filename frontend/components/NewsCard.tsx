"use client";

import React from "react";
import Link from "next/link";
import clsx from "clsx";
import { ExternalLink, Clock, Newspaper } from "lucide-react";
import SentimentBadge from "./SentimentBadge";
import type { NewsArticle } from "@/lib/api";

interface NewsCardProps {
  article: NewsArticle;
}

export default function NewsCard({ article }: NewsCardProps) {
  const publishedDate = new Date(article.published_at).toLocaleDateString("en-ID", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <Link href={`/news/${article.slug}`}>
      <article
        className={clsx(
          "group p-5 bg-[#18181B] rounded-2xl border border-[#3F3F46]",
          "hover:border-[#22C55E] transition-all duration-200 cursor-pointer",
          "flex flex-col gap-3 h-full"
        )}
      >
        {/* Header row */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 text-xs text-[#A1A1AA]">
            <Newspaper className="w-3.5 h-3.5" />
            <span>{article.source_name}</span>
          </div>
          <SentimentBadge sentiment={article.sentiment} confidence={article.confidence} />
        </div>

        {/* Title */}
        <h3 className="text-base font-semibold text-[#FAFAFA] leading-snug line-clamp-2 group-hover:text-[#22C55E] transition-colors">
          {article.title}
        </h3>

        {/* Summary */}
        <p className="text-sm text-[#A1A1AA] leading-relaxed line-clamp-3 flex-1">
          {article.summary}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between pt-2 border-t border-[#3F3F46]/50">
          <div className="flex items-center gap-1.5 text-xs text-[#71717A]">
            <Clock className="w-3 h-3" />
            <time dateTime={article.published_at}>{publishedDate}</time>
          </div>
          <ExternalLink className="w-3.5 h-3.5 text-[#71717A] group-hover:text-[#22C55E] transition-colors" />
        </div>
      </article>
    </Link>
  );
}