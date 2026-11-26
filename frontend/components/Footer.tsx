import { APP_VERSION } from "@/lib/version";

export default function Footer() {
  return (
    <footer className="border-t border-border mt-auto">
      <div className="max-w-[1440px] mx-auto px-6 py-8 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm text-text-secondary">
        <span className="font-display font-semibold text-foreground">FinPulse</span>
        <span className="flex flex-wrap items-center gap-x-3 gap-y-1">
          <span>v{APP_VERSION}</span>
          <span aria-hidden="true">•</span>
          <span>&copy; {new Date().getFullYear()} FinPulse</span>
        </span>
      </div>
    </footer>
  );
}