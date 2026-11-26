"use client";

import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export default function ErrorState({
  title = "Unable to Load News",
  message = "Gagal memuat berita. Periksa koneksi lalu coba lagi.",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
      <AlertTriangle className="w-10 h-10 text-negative mb-4" aria-hidden="true" />
      <h3 className="font-headline text-lg font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-text-secondary max-w-md mb-6">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-card border border-border text-sm font-semibold text-foreground hover:bg-hover transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
        >
          <RefreshCw className="w-4 h-4" aria-hidden="true" />
          Retry
        </button>
      )}
    </div>
  );
}