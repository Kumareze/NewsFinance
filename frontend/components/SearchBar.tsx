"use client";

import React, { useState, useCallback, useId } from "react";
import { Search, X } from "lucide-react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  initialValue?: string;
  placeholder?: string;
}

export default function SearchBar({
  onSearch,
  initialValue = "",
  placeholder = "Search financial news...",
}: SearchBarProps) {
  const [value, setValue] = useState(initialValue);
  const inputId = useId();

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      onSearch(value.trim());
    },
    [value, onSearch]
  );

  const handleClear = useCallback(() => {
    setValue("");
    onSearch("");
  }, [onSearch]);

  return (
    <form
      onSubmit={handleSubmit}
      role="search"
      className="relative w-full max-w-[720px] group"
    >
      <label htmlFor={inputId} className="sr-only">
        Cari berita keuangan
      </label>
      <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-muted group-focus-within:text-foreground transition-colors" />
      </div>
      <input
        id={inputId}
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-12 py-3.5 bg-secondary border border-border rounded-[14px] text-base text-foreground placeholder-muted hover:border-muted focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background transition-colors"
      />
      {value && (
        <button
          type="button"
          onClick={handleClear}
          aria-label="Hapus pencarian"
          className="absolute inset-y-0 right-2 my-auto h-9 w-9 flex items-center justify-center rounded-full text-muted hover:text-foreground hover:bg-hover transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </form>
  );
}
