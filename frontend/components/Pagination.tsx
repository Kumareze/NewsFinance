import React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface PaginationProps {
  page: number;
  totalPages: number;
  onChange: (page: number) => void;
  /** untuk aria-label, mis. "Positive News" */
  label: string;
}

export default function Pagination({ page, totalPages, onChange, label }: PaginationProps) {
  if (totalPages <= 1) return null;

  const buttonClass =
    "inline-flex items-center gap-1.5 min-h-[44px] px-3.5 rounded-xl bg-card border border-border text-sm font-semibold text-foreground hover:bg-hover disabled:opacity-40 disabled:pointer-events-none transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground";

  return (
    <nav
      aria-label={`Halaman ${label}`}
      className="flex items-center justify-between gap-3 pt-2"
    >
      <button
        type="button"
        onClick={() => onChange(page - 1)}
        disabled={page <= 1}
        className={buttonClass}
      >
        <ChevronLeft className="w-4 h-4" aria-hidden="true" />
        Sebelumnya
      </button>
      <span className="text-sm text-text-secondary tabular-nums">
        Halaman {page} dari {totalPages}
      </span>
      <button
        type="button"
        onClick={() => onChange(page + 1)}
        disabled={page >= totalPages}
        className={buttonClass}
      >
        Berikutnya
        <ChevronRight className="w-4 h-4" aria-hidden="true" />
      </button>
    </nav>
  );
}
