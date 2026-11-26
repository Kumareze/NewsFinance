"use client";

import React, { useState } from "react";
import { Newspaper } from "lucide-react";
import clsx from "clsx";

interface NewsCardImageProps {
  src?: string | null;
  alt: string;
  className?: string;
}

export default function NewsCardImage({ src, alt, className }: NewsCardImageProps) {
  const [error, setError] = useState(false);

  const showFallback = !src || error;

  return (
    <div
      className={clsx(
        "relative bg-hover overflow-hidden",
        className
      )}
    >
      {showFallback ? (
        <div className="absolute inset-0 flex items-center justify-center">
          <Newspaper className="w-10 h-10 text-muted" aria-hidden="true" />
        </div>
      ) : (
        <img
          src={src}
          alt={alt}
          loading="lazy"
          onError={() => setError(true)}
          className="object-cover w-full h-full"
        />
      )}
    </div>
  );
}