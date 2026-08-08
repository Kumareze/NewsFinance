import React from "react";
import NewsCard from "./NewsCard";
import { NewsCardSkeleton } from "./Skeleton";
import EmptyState from "./EmptyState";
import clsx from "clsx";
import type { NewsArticle } from "@/lib/api";

interface NewsSectionProps {
  title: string;
  dotColor: string;
  dotShadowClass?: string;
  articles: NewsArticle[];
  loading: boolean;
  error?: string | null;
  showSentimentBadge?: boolean;
}

export default function NewsSection({
  title,
  dotColor,
  dotShadowClass,
  articles,
  loading,
  error,
  showSentimentBadge = true,
}: NewsSectionProps) {
  return (
    <section className="flex flex-col gap-6">
      <div className="flex items-center gap-3">
        <div className={clsx("w-3 h-3 rounded-full", dotColor, dotShadowClass)} />
        <h2 className="font-headline text-2xl md:text-[32px] font-bold text-white">
          {title}
        </h2>
      </div>

      {error ? (
        <p className="text-sm text-[#71717A]">Failed to load {title.toLowerCase()}.</p>
      ) : loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-[24px]">
          {Array.from({ length: 4 }).map((_, i) => (
            <NewsCardSkeleton key={i} />
          ))}
        </div>
      ) : articles.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-[24px]">
          {articles.map((article) => (
            <NewsCard
              key={article.id}
              article={article}
              showSentimentBadge={showSentimentBadge}
            />
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-[#3F3F46] bg-[#27272A]">
          <EmptyState />
        </div>
      )}
    </section>
  );
}