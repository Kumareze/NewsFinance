/**
 * Formatting helpers for FinPulse UI.
 */

/**
 * Format a date as a relative time string in the style of the Stitch design,
 * e.g. "2 hours ago", "5 minutes ago", "3 days ago".
 */
export function formatRelativeTime(dateInput: string | Date): string {
  const date = typeof dateInput === "string" ? new Date(dateInput) : dateInput;
  const now = Date.now();
  const diffMs = now - date.getTime();

  if (Number.isNaN(date.getTime()) || diffMs < 0) {
    return date.toLocaleDateString("en-ID", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const weeks = Math.floor(days / 7);

  if (seconds < 60) return "just now";
  if (minutes < 60) return `${minutes} ${minutes === 1 ? "minute" : "minutes"} ago`;
  if (hours < 24) return `${hours} ${hours === 1 ? "hour" : "hours"} ago`;
  if (days < 7) return `${days} ${days === 1 ? "day" : "days"} ago`;
  if (weeks < 5) return `${weeks} ${weeks === 1 ? "week" : "weeks"} ago`;

  return date.toLocaleDateString("en-ID", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/**
 * Format a date as a long, readable date string for the article detail page.
 */
export function formatLongDate(dateInput: string | Date): string {
  const date = typeof dateInput === "string" ? new Date(dateInput) : dateInput;
  return date.toLocaleDateString("en-ID", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}