import Link from "next/link";
import { Search } from "lucide-react";

/**
 * Header: logo + search saja (tanpa menu, login, atau navbar kompleks).
 * Tombol search adalah anchor ke form pencarian di hero, bukan tombol mati.
 */
export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-background/90 backdrop-blur border-b border-border">
      <div className="max-w-[1440px] mx-auto h-16 px-6 flex items-center justify-between">
        <Link
          href="/"
          className="font-display text-2xl font-bold tracking-tight text-foreground rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
        >
          FinPulse
        </Link>
        <a
          href="#search"
          aria-label="Cari berita"
          className="p-2 rounded-full text-text-secondary hover:text-foreground hover:bg-hover transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-foreground"
        >
          <Search className="w-5 h-5" />
        </a>
      </div>
    </header>
  );
}
