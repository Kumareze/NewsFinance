"use client";

import React from "react";
import Link from "next/link";
import { Building2, CalendarDays } from "lucide-react";
import SentimentBadge from "./SentimentBadge";
import NewsCardImage from "./NewsCardImage";
import { formatRelativeTime } from "@/lib/format";
import type { NewsArticle } from "@/lib/api";

interface NewsCardProps {
  article: NewsArticle;
  showSentimentBadge?: boolean;
}

export default function NewsCard({ article, showSentimentBadge = true }: NewsCardProps) {
  return (
    <Link href={`/news/${article.slug}`} className="group block h-full">
      <article className="bg-[#27272A] border border-[#3F3F46] rounded-2xl overflow-hidden flex flex-col cursor-pointer transition-all duration-200 hover:-translate-y-1 hover:scale-[1.02] hover:shadow-lg hover:shadow-black/20 h-full">
        <NewsCardImage
          src={article.thumbnail}
          alt={article.title}
          className="w-full aspect-video"
        />
        <div className="p-5 flex flex-col flex-grow gap-3">
          {showSentimentBadge && (
            <div className="flex items-center">
              <SentimentBadge sentiment={article.sentiment} confidence={article.confidence} />
            </div>
          )}
          <h3 className="font-headline text-[20px] leading-snug font-semibold text-white line-clamp-2 group-hover:text-white transition-colors">
            {article.title}
          </h3>
          <div className="mt-auto pt-4 flex items-center gap-3 text-[#71717A] text-sm">
            <span className="flex items-center gap-1.5">
              <Building2 className="w-4 h-4" />
              {article.source_name}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1.5">
              <CalendarDays className="w-4 h-4" />
              <time dateTime={article.published_at}>
                {formatRelativeTime(article.published_at)}
              </time>
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}