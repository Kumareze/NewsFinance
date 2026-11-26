"use client";

import React from "react";
import { Newspaper, RefreshCw } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  message?: string;
  onRefresh?: () => void;
}

export default function EmptyState({
  title = "No News Available",
  message = "Belum ada berita untuk kriteria ini.",
  onRefresh,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
      <Newspaper className="w-10 h-10 text-muted mb-4" aria-hidden="true" />
      <h3 className="font-headline text-lg font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-text-secondary max-w-md">{message}</p>
      {onRefresh && (
        <button
          onClick={onRefresh}
          className="mt-6 inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-card border border-border text-sm font-semibold text-foreground hover:bg-hover transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
        >
          <RefreshCw className="w-4 h-4" aria-hidden="true" />
          Refresh
        </button>
      )}
    </div>
  );
}