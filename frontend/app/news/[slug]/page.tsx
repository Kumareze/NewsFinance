"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, ExternalLink, Clock, Newspaper, Calendar } from "lucide-react";
import SentimentBadge from "@/components/SentimentBadge";
import { Skeleton } from "@/components/Skeleton";
import ErrorState from "@/components/ErrorState";
import { api, NewsArticle } from "@/lib/api";

export default function ArticleDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [article, setArticle] = useState<NewsArticle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;

    const fetchArticle = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await api.getNewsBySlug(slug);
        setArticle(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load article");
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#09090B] text-[#FAFAFA] px-6 md:px-12 py-8">
        <div className="max-w-3xl mx-auto space-y-6">
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-3/4" />
          <div className="flex gap-4">
            <Skeleton className="h-5 w-24 rounded-full" />
            <Skeleton className="h-5 w-32" />
          </div>
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-4/5" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#09090B] text-[#FAFAFA] px-6 md:px-12 py-8">
        <div className="max-w-3xl mx-auto">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-[#A1A1AA] hover:text-[#FAFAFA] mb-8 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to articles
          </Link>
          <ErrorState message={error} onRetry={() => window.location.reload()} />
        </div>
      </div>
    );
  }

  if (!article) return null;

  const publishedDate = new Date(article.published_at).toLocaleDateString("en-ID", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="min-h-screen bg-[#09090B] text-[#FAFAFA]">
      {/* Nav */}
      <div className="border-b border-[#3F3F46] py-4 px-6 md:px-12 bg-[#18181B]">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-[#A1A1AA] hover:text-[#FAFAFA] transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to articles
          </Link>
          <div className="text-sm font-bold tracking-tight">
            Fin<span className="text-[#22C55E]">Pulse</span>
          </div>
        </div>
      </div>

      {/* Article */}
      <article className="max-w-3xl mx-auto px-6 md:px-12 py-12">
        {/* Meta */}
        <div className="flex flex-wrap items-center gap-4 mb-6">
          <SentimentBadge sentiment={article.sentiment} confidence={article.confidence} />
          <div className="flex items-center gap-2 text-sm text-[#A1A1AA]">
            <Newspaper className="w-4 h-4" />
            <span>{article.source_name}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-[#A1A1AA]">
            <Calendar className="w-4 h-4" />
            <time dateTime={article.published_at}>{publishedDate}</time>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-3xl md:text-4xl font-extrabold leading-tight mb-6">
          {article.title}
        </h1>

        {/* Summary */}
        <div className="p-4 bg-[#18181B] border border-[#3F3F46] rounded-xl mb-8">
          <p className="text-sm text-[#A1A1AA] italic leading-relaxed">
            {article.summary}
          </p>
        </div>

        {/* Content */}
        {article.content ? (
          <div className="prose prose-invert prose-sm max-w-none text-[#D4D4D8] leading-relaxed whitespace-pre-wrap">
            {article.content}
          </div>
        ) : (
          <p className="text-[#71717A] text-sm italic">
            Full content is not available for this article.
          </p>
        )}

        {/* Source link */}
        <div className="mt-12 pt-6 border-t border-[#3F3F46]">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm text-[#22C55E] hover:text-[#4ADE80] transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            Read original article
          </a>
        </div>
      </article>

      {/* Footer */}
      <footer className="border-t border-[#3F3F46] py-6 px-6 text-center text-sm text-[#71717A] bg-[#18181B]">
        <div className="max-w-3xl mx-auto">
          &copy; {new Date().getFullYear()} FinPulse. All rights reserved.
        </div>
      </footer>
    </div>
  );
}