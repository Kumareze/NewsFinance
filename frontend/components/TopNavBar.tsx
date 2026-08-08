import Link from "next/link";
import { Search, Bell, User } from "lucide-react";

export default function TopNavBar() {
  return (
    <header className="bg-[#09090B] border-b border-[#3F3F46] fixed top-0 left-0 w-full z-50 flex justify-center items-center h-16 px-6 md:px-[24px] transition-all duration-200">
      <div className="w-full max-w-[1440px] flex items-center justify-between">
        <Link href="/" className="flex items-center">
          <span className="font-display text-2xl font-bold tracking-tighter text-white">
            FinPulse
          </span>
        </Link>
        <div className="flex items-center gap-2">
          <Link
            href="/"
            aria-label="Search"
            className="text-white hover:bg-[#3F3F46] p-2 rounded-full transition-colors duration-200 active:scale-95"
          >
            <Search className="w-5 h-5" />
          </Link>
          <button
            aria-label="Notifications"
            className="text-white hover:bg-[#3F3F46] p-2 rounded-full transition-colors duration-200 active:scale-95"
            type="button"
          >
            <Bell className="w-5 h-5" />
          </button>
          <button
            aria-label="Account"
            className="text-white hover:bg-[#3F3F46] p-2 rounded-full transition-colors duration-200 active:scale-95"
            type="button"
          >
            <User className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}