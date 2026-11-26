"use client";

import React, { useCallback, useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SearchBar from "@/components/SearchBar";
import NewsSection from "@/components/NewsSection";
import NewsCard from "@/components/NewsCard";
import EmptyState from "@/components/EmptyState";
import ErrorState from "@/components/ErrorState";
import { NewsCardSkeleton } from "@/components/Skeleton";
import { api, NewsArticle, NewsSearchResult } from "@/lib/api";

/** Jumlah card per grid section (1 hero + sisanya kartu kecil). */
const SECTION_SIZE = 9;

interface Feed {
  latest: NewsArticle[];
  positive: NewsSearchResult;
  negative: NewsSearchResult;
}

type SectionKey = "positive" | "negative";

const SECTIONS: {
  id: SectionKey;
  title: string;
  sentiment: NewsArticle["sentiment"];
  emptyMessage: string;
}[] = [
  { id: "positive", title: "Positive News", sentiment: "positive", emptyMessage: "Belum ada berita bersentimen positif." },
  { id: "negative", title: "Negative News", sentiment: "negative", emptyMessage: "Belum ada berita bersentimen negatif." },
];

type PageState = Record<SectionKey, number>;

export default function Home() {
  const [query, setQuery] = useState("");
  const [pages, setPages] = useState<PageState>({ positive: 1, negative: 1 });
  const [feed, setFeed] = useState<Feed | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFeed = useCallback(async (q: string, p: PageState) => {
    setLoading(true);
    setError(null);
    try {
      const [latest, positive, negative] = await Promise.all([
        api.getNews({ page: 1, page_size: 1, sort: "latest", q: q || undefined }),
        api.getNews({ page: p.positive, page_size: SECTION_SIZE, sentiment: "positive", sort: "latest", q: q || undefined }),
        api.getNews({ page: p.negative, page_size: SECTION_SIZE, sentiment: "negative", sort: "latest", q: q || undefined }),
      ]);
      setFeed({ latest: latest.items, positive, negative });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load news");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFeed(query, pages);
  }, [fetchFeed, query, pages]);

  /** Ganti halaman satu section, lalu bawa viewport ke judul section itu. */
  const changePage = useCallback((id: SectionKey, page: number) => {
    setPages((prev) => (prev[id] === page ? prev : { ...prev, [id]: page }));
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, []);

  const retry = () => fetchFeed(query, pages);
  const latest = feed?.latest[0] ?? null;

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />

      <main className="flex-grow w-full max-w-[1440px] mx-auto px-6 flex flex-col gap-8 pb-16">
        {/* Hero + Search */}
        <section className="flex flex-col items-center text-center pt-16 pb-10">
          <h1 className="font-display text-[48px] leading-[1.2] tracking-[-0.02em] font-bold text-foreground">
            FinPulse
          </h1>
          <p className="mt-3 text-lg text-text-secondary">Read Financial News by Sentiment</p>
          <div id="search" className="w-full mt-8 flex justify-center scroll-mt-24">
            <SearchBar
              onSearch={(q) => {
                setPages({ positive: 1, negative: 1 });
                setQuery(q);
              }}
              initialValue={query}
              placeholder="Search financial news..."
            />
          </div>
          {query && (
            <p className="mt-4 text-sm text-text-secondary">
              Hasil pencarian: <span className="text-foreground">&ldquo;{query}&rdquo;</span>
            </p>
          )}
        </section>

        {error ? (
          <div className="rounded-card border border-border bg-card">
            <ErrorState message={error} onRetry={retry} />
          </div>
        ) : (
          <>
            {/* Berita terbaru */}
            <section aria-label="Berita terbaru">
              {loading ? (
                <div className="max-w-2xl">
                  <NewsCardSkeleton featured />
                </div>
              ) : latest ? (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-0 rounded-card border border-border bg-card overflow-hidden">
                  <div className="lg:col-span-2">
                    <NewsCard article={latest} featured />
                  </div>
                  <div className="hidden lg:flex flex-col justify-center gap-4 p-8 border-l border-border">
                    <span className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
                      Latest
                    </span>
                    <p className="text-sm text-text-secondary leading-relaxed line-clamp-5">
                      {latest.summary}
                    </p>
                    <span className="inline-flex items-center gap-2 text-sm font-semibold text-foreground">
                      Baca berita
                      <ArrowRight className="w-4 h-4" aria-hidden="true" />
                    </span>
                  </div>
                </div>
              ) : (
                <div className="rounded-card border border-border bg-card">
                  <EmptyState message="Belum ada berita yang cocok dengan pencarian." onRefresh={retry} />
                </div>
              )}
            </section>

            <div className="flex flex-col gap-16 pt-4">
              {SECTIONS.map((section) => {
                const result = feed?.[section.id];
                return (
                  <NewsSection
                    key={section.id}
                    id={section.id}
                    title={section.title}
                    sentiment={section.sentiment}
                    articles={result?.items ?? []}
                    total={result?.total ?? 0}
                    page={pages[section.id]}
                    pageSize={SECTION_SIZE}
                    onPageChange={(page) => changePage(section.id, page)}
                    loading={loading}
                    emptyMessage={section.emptyMessage}
                  />
                );
              })}
            </div>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
