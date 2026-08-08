import { Newspaper } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-[#09090B] border-t border-[#3F3F46] w-full py-[32px] px-6 md:px-[24px] mt-auto">
      <div className="max-w-[1440px] mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-2">
          <Newspaper className="w-5 h-5 text-[#71717A]" />
          <span className="text-white font-semibold tracking-tight">FinPulse</span>
        </div>
        <div className="flex flex-col md:flex-row items-center gap-4 text-[#71717A] text-sm">
          <span>&copy; {new Date().getFullYear()} FinPulse. All rights reserved.</span>
          <div className="hidden md:block w-1 h-1 bg-[#3F3F46] rounded-full"></div>
          <span>Read Financial News by Sentiment</span>
        </div>
      </div>
    </footer>
  );
}