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
    <div className="bg-[#27272A] rounded-2xl border border-[#3F3F46] overflow-hidden flex flex-col">
      <Skeleton className="w-full aspect-video" />
      <div className="p-5 flex flex-col gap-3">
        <Skeleton className="h-6 w-24 rounded-full" />
        <Skeleton className="h-5 w-full" />
        <Skeleton className="h-5 w-4/5" />
        <div className="pt-4 flex items-center gap-3">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-1" />
          <Skeleton className="h-4 w-28" />
        </div>
      </div>
    </div>
  );
}