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
  featured?: boolean;
}

export default function NewsCard({
  article,
  showSentimentBadge = true,
  featured = false,
}: NewsCardProps) {
  return (
    <Link
      href={`/news/${article.slug}`}
      className="group block h-full rounded-card focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
    >
      <article className="h-full flex flex-col overflow-hidden rounded-card bg-card border border-border shadow-card transition-all duration-200 group-hover:-translate-y-1 group-hover:shadow-card-hover">
        <NewsCardImage
          src={article.thumbnail}
          alt={article.title}
          className={featured ? "w-full aspect-[16/10]" : "w-full aspect-video"}
        />
        <div className="p-5 flex flex-col flex-grow gap-3">
          {showSentimentBadge && (
            <div>
              <SentimentBadge sentiment={article.sentiment} />
            </div>
          )}
          <h3
            className={
              featured
                ? "font-headline text-xl md:text-2xl font-bold leading-snug text-foreground line-clamp-2"
                : "font-headline text-base font-semibold leading-snug text-foreground line-clamp-2"
            }
          >
            {article.title}
          </h3>
          {featured && article.summary && (
            <p className="text-sm text-text-secondary line-clamp-2">{article.summary}</p>
          )}
          <div className="mt-auto pt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-text-secondary">
            <span className="flex items-center gap-1.5 min-w-0">
              <Building2 className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
              <span className="truncate">{article.source_name}</span>
            </span>
            <span aria-hidden="true">•</span>
            <span className="flex items-center gap-1.5">
              <CalendarDays className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
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
