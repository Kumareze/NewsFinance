"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, ExternalLink, Newspaper, Calendar } from "lucide-react";
import TopNavBar from "@/components/TopNavBar";
import Footer from "@/components/Footer";
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
      <div className="min-h-screen bg-[#09090B] text-white flex flex-col">
        <TopNavBar />
        <main className="flex-grow pt-24 pb-12 px-6 md:px-[24px] max-w-[1440px] mx-auto w-full">
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
        </main>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#09090B] text-white flex flex-col">
        <TopNavBar />
        <main className="flex-grow pt-24 pb-12 px-6 md:px-[24px] max-w-[1440px] mx-auto w-full">
          <div className="max-w-3xl mx-auto">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-sm text-[#71717A] hover:text-white mb-8 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to articles
            </Link>
            <ErrorState message={error} onRetry={() => window.location.reload()} />
          </div>
        </main>
        <Footer />
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
    <div className="min-h-screen bg-[#09090B] text-white flex flex-col">
      <TopNavBar />

      {/* Article */}
      <main className="flex-grow pt-24 pb-12 px-6 md:px-[24px] max-w-[1440px] mx-auto w-full">
        <article className="max-w-3xl mx-auto">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-[#71717A] hover:text-white mb-8 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to articles
          </Link>

          {/* Meta */}
          <div className="flex flex-wrap items-center gap-4 mb-6">
            <SentimentBadge sentiment={article.sentiment} confidence={article.confidence} />
            <div className="flex items-center gap-2 text-sm text-[#71717A]">
              <Newspaper className="w-4 h-4" />
              <span>{article.source_name}</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-[#71717A]">
              <Calendar className="w-4 h-4" />
              <time dateTime={article.published_at}>{publishedDate}</time>
            </div>
          </div>

          {/* Title */}
          <h1 className="font-headline text-3xl md:text-4xl font-bold leading-tight mb-6">
            {article.title}
          </h1>

          {/* Summary */}
          <div className="p-4 bg-[#27272A] border border-[#3F3F46] rounded-xl mb-8">
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
      </main>

      <Footer />
    </div>
  );
}