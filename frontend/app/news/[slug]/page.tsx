"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, ExternalLink, Building2, CalendarDays } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SentimentBadge from "@/components/SentimentBadge";
import NewsCardImage from "@/components/NewsCardImage";
import { Skeleton } from "@/components/Skeleton";
import ErrorState from "@/components/ErrorState";
import { formatLongDate } from "@/lib/format";
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
        setArticle(await api.getNewsBySlug(slug));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load article");
      } finally {
        setLoading(false);
      }
    };

    fetchArticle();
  }, [slug]);

  const backLink = (
    <Link
      href="/"
      className="inline-flex items-center gap-2 text-sm text-text-secondary hover:text-foreground transition-colors rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
    >
      <ArrowLeft className="w-4 h-4" aria-hidden="true" />
      Kembali
    </Link>
  );

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />

      <main className="flex-grow w-full max-w-[1440px] mx-auto px-6 py-10">
        <div className="max-w-3xl mx-auto">
          {backLink}

          {loading ? (
            <div className="mt-8 flex flex-col gap-5" aria-busy="true">
              <Skeleton className="w-full aspect-video rounded-card" />
              <Skeleton className="h-9 w-full" />
              <Skeleton className="h-9 w-3/4" />
              <div className="flex gap-4">
                <Skeleton className="h-6 w-24 rounded-full" />
                <Skeleton className="h-6 w-32" />
              </div>
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-4/5" />
            </div>
          ) : error ? (
            <div className="mt-8 rounded-card border border-border bg-card">
              <ErrorState message={error} onRetry={() => window.location.reload()} />
            </div>
          ) : !article ? null : (
            <article className="mt-8 flex flex-col gap-6">
              <NewsCardImage
                src={article.thumbnail}
                alt={article.title}
                className="w-full aspect-video rounded-card border border-border"
              />

              <h1 className="font-headline text-3xl md:text-4xl font-bold leading-tight text-foreground">
                {article.title}
              </h1>

              <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-text-secondary">
                <span className="flex items-center gap-2">
                  <Building2 className="w-4 h-4" aria-hidden="true" />
                  {article.source_name}
                </span>
                <span className="flex items-center gap-2">
                  <CalendarDays className="w-4 h-4" aria-hidden="true" />
                  <time dateTime={article.published_at}>{formatLongDate(article.published_at)}</time>
                </span>
                <SentimentBadge sentiment={article.sentiment} />
              </div>

              {article.summary && (
                <p className="p-5 rounded-card bg-card border border-border text-text-secondary leading-relaxed">
                  {article.summary}
                </p>
              )}

              {article.content ? (
                <div className="text-text-secondary leading-relaxed whitespace-pre-wrap">
                  {article.content}
                </div>
              ) : (
                <p className="text-sm text-muted">
                  Isi lengkap tidak tersedia. Baca berita aslinya di {article.source_name}.
                </p>
              )}

              <div className="pt-6 border-t border-border">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm font-semibold text-foreground hover:text-text-secondary transition-colors rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
                >
                  <ExternalLink className="w-4 h-4" aria-hidden="true" />
                  Baca artikel asli
                </a>
              </div>
            </article>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
