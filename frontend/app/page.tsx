"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Search, TrendingUp, TrendingDown, BarChart3 } from "lucide-react";
import SearchBar from "@/components/SearchBar";
import FilterBar from "@/components/FilterBar";
import NewsCard from "@/components/NewsCard";
import { NewsCardSkeleton } from "@/components/Skeleton";
import EmptyState from "@/components/EmptyState";
import ErrorState from "@/components/ErrorState";
import { api, NewsSearchResult, NewsArticle } from "@/lib/api";

type SentimentFilter = "" | "positive" | "negative" | "neutral";
type SortOption = "latest" | "oldest" | "positive" | "negative";

export default function Home() {
  const [data, setData] = useState<NewsSearchResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [query, setQuery] = useState("");
  const [sentiment, setSentiment] = useState<SentimentFilter>("");
  const [sort, setSort] = useState<SortOption>("latest");
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

  return (
    <div className="flex flex-col min-h-screen bg-[#09090B] text-[#FAFAFA]">
      {/* Header */}
      <header className="border-b border-[#3F3F46] py-4 px-6 md:px-12 bg-[#18181B]">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="text-xl font-bold tracking-tight text-[#FAFAFA]">
            Fin<span className="text-[#22C55E]">Pulse</span>
          </div>
          <div className="text-sm text-[#A1A1AA]">
            {data ? `${data.total} articles` : "Loading..."}
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="flex-grow px-6 md:px-12 py-8">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Hero */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight leading-none">
              Fin<span className="text-[#22C55E]">Pulse</span> Aggregator
            </h1>
            <p className="text-lg text-[#A1A1AA] max-w-2xl mx-auto">
              High-performance Financial News Aggregator — Indonesian market intelligence classified by real-time sentiment analysis.
            </p>
          </div>

          {/* Search + Filters */}
          <div className="flex flex-col items-center gap-6">
            <SearchBar onSearch={setQuery} initialValue={query} />
            <FilterBar
              sentiment={sentiment}
              sort={sort}
              onSentimentChange={setSentiment}
              onSortChange={setSort}
            />
          </div>

          {/* Content */}
          {error ? (
            <ErrorState message={error} onRetry={fetchNews} />
          ) : loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <NewsCardSkeleton key={i} />
              ))}
            </div>
          ) : data && data.items.length > 0 ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.items.map((article: NewsArticle) => (
                  <NewsCard key={article.id} article={article} />
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2 pt-8">
                  <button
                    disabled={page <= 1}
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    className="px-4 py-2 rounded-lg bg-[#27272A] border border-[#3F3F46] text-sm disabled:opacity-40 hover:bg-[#3F3F46] transition-colors"
                  >
                    Previous
                  </button>
                  <span className="text-sm text-[#A1A1AA]">
                    Page {page} of {totalPages}
                  </span>
                  <button
                    disabled={page >= totalPages}
                    onClick={() => setPage((p) => p + 1)}
                    className="px-4 py-2 rounded-lg bg-[#27272A] border border-[#3F3F46] text-sm disabled:opacity-40 hover:bg-[#3F3F46] transition-colors"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          ) : (
            <EmptyState />
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-[#3F3F46] py-6 px-6 text-center text-sm text-[#71717A] bg-[#18181B]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div>&copy; {new Date().getFullYear()} FinPulse. All rights reserved.</div>
          <div className="flex items-center space-x-1">
            <span>Built for excellence by Lead Engineer</span>
          </div>
        </div>
      </footer>
    </div>
  );
}