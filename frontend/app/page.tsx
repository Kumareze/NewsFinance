"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import { FileText } from "lucide-react";
import TopNavBar from "@/components/TopNavBar";
import Footer from "@/components/Footer";
import SearchBar from "@/components/SearchBar";
import FilterBar from "@/components/FilterBar";
import NewsSection from "@/components/NewsSection";
import EmptyState from "@/components/EmptyState";
import ErrorState from "@/components/ErrorState";
import { api, NewsSearchResult } from "@/lib/api";

type SentimentFilter = "" | "positive" | "negative" | "neutral";
type SortOption = "latest" | "oldest" | "positive" | "negative" | "mixed";

export default function Home() {
  const [data, setData] = useState<NewsSearchResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [query, setQuery] = useState("");
  const [sentiment, setSentiment] = useState<SentimentFilter>("");
  const [sort, setSort] = useState<SortOption>("mixed");
  const [page, setPage] = useState(1);

  const fetchNews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.getNews({
        page,
        page_size: 20,
        sentiment: sentiment || undefined,
        sort,
        q: query || undefined,
      });
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch news");
    } finally {
      setLoading(false);
    }
  }, [page, sentiment, sort, query]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  // Reset to page 1 when filters change
  useEffect(() => {
    setPage(1);
  }, [query, sentiment, sort]);

  // Stats
  const totalPages = data ? Math.ceil(data.total / data.page_size) : 0;

  // Split fetched page into sentiment sections for the Stitch layout
  const positiveArticles = useMemo(
    () => (data?.items ?? []).filter((a) => a.sentiment === "positive"),
    [data]
  );
  const negativeArticles = useMemo(
    () => (data?.items ?? []).filter((a) => a.sentiment === "negative"),
    [data]
  );

  return (
    <div className="flex flex-col min-h-screen bg-[#09090B] text-white">
      <TopNavBar />

      {/* Main */}
      <main className="flex-grow pt-24 pb-12 px-6 md:px-[24px] max-w-[1440px] mx-auto w-full flex flex-col gap-[32px]">
        {/* Hero Section */}
        <section className="flex flex-col items-center text-center pt-12 pb-16">
          <h1 className="font-display text-[48px] leading-[1.2] tracking-[-0.02em] font-bold text-white mb-4">
            FinPulse
          </h1>
          <p className="text-[18px] leading-[28px] text-[#71717A] max-w-2xl mb-4">
            Read Financial News by Sentiment
          </p>
          <div className="flex items-center gap-2 px-3 py-1 bg-[#1c1b1b] border border-[#3F3F46] rounded-full mb-6 text-[14px] font-semibold text-[#71717A]">
            <FileText className="w-4 h-4" />
            <span>Total Articles: {data ? data.total : "..."}</span>
          </div>
          <div className="w-full max-w-[720px]">
            <SearchBar onSearch={setQuery} initialValue={query} placeholder="Search financial news..." />
          </div>
          <div className="mt-6 flex flex-col items-center gap-6">
            <FilterBar
              sentiment={sentiment}
              sort={sort}
              onSentimentChange={setSentiment}
              onSortChange={setSort}
            />
          </div>
        </section>

        {/* Content */}
        {error ? (
          <ErrorState message={error} onRetry={fetchNews} />
        ) : loading ? (
          <div className="flex flex-col gap-[32px]">
            <NewsSection
              title="Positive News"
              dotColor="bg-[#22C55E]"
              dotShadowClass="shadow-[0_0_8px_rgba(34,197,94,0.4)]"
              articles={[]}
              loading
            />
            <NewsSection
              title="Negative News"
              dotColor="bg-[#EF4444]"
              dotShadowClass="shadow-[0_0_8px_rgba(239,68,68,0.4)]"
              articles={[]}
              loading
            />
          </div>
        ) : data && data.items.length > 0 ? (
          <div className="flex flex-col gap-[32px]">
            <NewsSection
              title="Positive News"
              dotColor="bg-[#22C55E]"
              dotShadowClass="shadow-[0_0_8px_rgba(34,197,94,0.4)]"
              articles={positiveArticles}
              loading={false}
            />
            <NewsSection
              title="Negative News"
              dotColor="bg-[#EF4444]"
              dotShadowClass="shadow-[0_0_8px_rgba(239,68,68,0.4)]"
              articles={negativeArticles}
              loading={false}
            />
            <NewsSection
              title="All News"
              dotColor="bg-white"
              dotShadowClass="shadow-[0_0_8px_rgba(255,255,255,0.4)]"
              articles={data.items}
              loading={false}
            />

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 pt-8">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="px-4 py-2 rounded-lg bg-[#27272A] border border-[#3F3F46] text-sm text-white disabled:opacity-40 hover:bg-[#3F3F46] transition-colors"
                >
                  Previous
                </button>
                <span className="text-sm text-[#71717A]">
                  Page {page} of {totalPages}
                </span>
                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                  className="px-4 py-2 rounded-lg bg-[#27272A] border border-[#3F3F46] text-sm text-white disabled:opacity-40 hover:bg-[#3F3F46] transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        ) : (
          <EmptyState />
        )}
      </main>

      <Footer />
    </div>
  );
}
