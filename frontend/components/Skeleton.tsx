"use client";

import React from "react";
import clsx from "clsx";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={clsx(
        "animate-pulse rounded-md bg-[#27272A]",
        className
      )}
    />
  );
}

export function NewsCardSkeleton() {
  return (
    <div className="p-5 bg-[#18181B] rounded-2xl border border-[#3F3F46] flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-5 w-20 rounded-full" />
      </div>
      <Skeleton className="h-5 w-full" />
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <div className="flex items-center justify-between pt-2 border-t border-[#3F3F46]/50">
        <Skeleton className="h-3 w-32" />
        <Skeleton className="h-4 w-4 rounded-full" />
      </div>
    </div>
  );
}