"use client";

import React from "react";
import { SearchX } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  message?: string;
}

export default function EmptyState({
  title = "No articles found",
  message = "Try adjusting your filters or search query.",
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <SearchX className="w-12 h-12 text-[#71717A] mb-4" />
      <h3 className="text-lg font-semibold text-[#FAFAFA] mb-1">{title}</h3>
      <p className="text-sm text-[#A1A1AA] max-w-md">{message}</p>
    </div>
  );
}