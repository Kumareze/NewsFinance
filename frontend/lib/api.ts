/**
 * FinPulse API Client
 *
 * Lightweight fetch-based client for the FinPulse backend.
 * All requests go through NEXT_PUBLIC_API_URL.
 */

const DEFAULT_API_BASE = "http://localhost:8000/api/v1";

function normalizeApiBase(raw?: string): string {
  if (!raw) return DEFAULT_API_BASE;

  // Defensive cleanup for accidental spaces/quotes in env var values.
  const cleaned = raw.trim().replace(/^['"]|['"]$/g, "").replace(/\/+$/, "");
  if (!cleaned) return DEFAULT_API_BASE;

  // Accept both:
  // - https://your-backend.onrender.com
  // - https://your-backend.onrender.com/api/v1
  return cleaned.endsWith("/api/v1") ? cleaned : `${cleaned}/api/v1`;
}

const API_BASE = normalizeApiBase(process.env.NEXT_PUBLIC_API_URL);

export interface NewsArticle {
  id: string;
  title: string;
  slug: string;
  url: string;
  source_name: string;
  summary: string;
  content: string | null;
  thumbnail: string | null;
  sentiment: "positive" | "negative" | "neutral";
  confidence: number;
  published_at: string;
  created_at: string;
  updated_at: string;
}

export interface NewsSearchResult {
  items: NewsArticle[];
  total: number;
  page: number;
  page_size: number;
}

export interface NewsSource {
  id: string;
  name: string;
  base_url: string;
  is_active: boolean;
  scrape_interval: number;
  created_at: string;
  updated_at: string;
}

export interface FetchNewsParams {
  page?: number;
  page_size?: number;
  sentiment?: string;
  source?: string;
  sort?: string;
  q?: string;
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(`API Error ${res.status}: ${errorBody}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  /** Fetch paginated, filterable news articles */
  getNews(params: FetchNewsParams = {}): Promise<NewsSearchResult> {
    const qs = new URLSearchParams();
    if (params.page) qs.set("page", String(params.page));
    if (params.page_size) qs.set("page_size", String(params.page_size));
    if (params.sentiment) qs.set("sentiment", params.sentiment);
    if (params.source) qs.set("source", params.source);
    if (params.sort) qs.set("sort", params.sort);
    if (params.q) qs.set("q", params.q);
    const queryString = qs.toString();
    return request<NewsSearchResult>(`/news/${queryString ? `?${queryString}` : ""}`);
  },

  /** Fetch a single article by slug */
  getNewsBySlug(slug: string): Promise<NewsArticle> {
    return request<NewsArticle>(`/news/${slug}`);
  },

  /** Fetch all active sources */
  getActiveSources(): Promise<NewsSource[]> {
    return request<NewsSource[]>("/sources/active");
  },
};