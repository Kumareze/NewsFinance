import React from "react";
import NewsCard from "./NewsCard";
import Pagination from "./Pagination";
import { NewsCardSkeleton } from "./Skeleton";
import EmptyState from "./EmptyState";
import clsx from "clsx";
import type { NewsArticle } from "@/lib/api";

type Sentiment = NewsArticle["sentiment"];

interface NewsSectionProps {
  id?: string;
  title: string;
  sentiment: Sentiment;
  articles: NewsArticle[];
  loading: boolean;
  /** Total artikel di backend untuk sentiment ini (bukan jumlah di halaman ini). */
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  emptyMessage?: string;
}

/** Dot penanda sentiment, dengan label teks di sebelahnya (bukan warna saja). */
const DOT_STYLES: Record<Sentiment, string> = {
  positive: "bg-positive",
  negative: "bg-negative",
  neutral: "bg-muted",
};

export default function NewsSection({
  id,
  title,
  sentiment,
  articles,
  loading,
  total,
  page,
  pageSize,
  onPageChange,
  emptyMessage,
}: NewsSectionProps) {
  const [featured, ...rest] = articles;
  const headingId = `${id ?? sentiment}-heading`;
  const totalPages = Math.ceil(total / pageSize);

  return (
    <section id={id} aria-labelledby={headingId} className="flex flex-col gap-6">
      <div className="flex items-baseline justify-between gap-4 border-b border-border pb-4">
        <h2 id={headingId} className="flex items-center gap-3 font-headline text-2xl font-bold text-foreground">
          <span className={clsx("w-2.5 h-2.5 rounded-full shrink-0", DOT_STYLES[sentiment])} aria-hidden="true" />
          {title}
        </h2>
        <span className="text-sm text-text-secondary tabular-nums">
          {loading ? "Loading..." : `${total} articles`}
        </span>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <NewsCardSkeleton key={i} featured={i === 0} />
          ))}
        </div>
      ) : !featured ? (
        <div className="rounded-card border border-border bg-card">
          <EmptyState message={emptyMessage} />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="md:col-span-2 md:row-span-2">
            <NewsCard article={featured} featured />
          </div>
          {rest.map((article) => (
            <NewsCard key={article.id} article={article} />
          ))}
        </div>
      )}

      {!loading && featured && (
        <Pagination
          label={title}
          page={page}
          totalPages={totalPages}
          onChange={onPageChange}
        />
      )}
    </section>
  );
}
