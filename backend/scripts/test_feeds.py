"""
Test available RSS feeds and find working URLs.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
import asyncio
import feedparser

TEST_URLS = [
    ("CNBC Indonesia RSS", "https://www.cnbcindonesia.com/rss"),
    ("CNBC US Top News", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("CNBC US Markets", "https://www.cnbc.com/id/10000664/device/rss/rss.html"),
    ("Reuters Agency Feed", "https://www.reutersagency.com/feed/"),
    ("Reuters Newsletter Picks", "https://www.reuters.com/arc/outboundfeeds/newsletter-picks/?outputType=xml"),
    ("MarketWatch Top", "https://feeds.marketwatch.com/marketwatch/topstories"),
    ("Financial Times World", "https://www.ft.com/world?format=rss"),
    ("WSJ Markets", "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"),
    ("WSJ US Business", "https://feeds.a.dj.com/rss/RSSWSJD.xml"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("Investing.com News", "https://www.investing.com/rss/news.rss"),
    ("Seeking Alpha", "https://seekingalpha.com/feed.xml"),
]


async def test_url(label: str, url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15, headers=headers) as client:
            resp = await client.get(url)
            content_type = resp.headers.get("content-type", "?")
            feed = feedparser.parse(resp.text)
            entry_count = len(feed.get("entries", []))
            if resp.status_code == 200 and entry_count > 0:
                status = f"OK ({entry_count} entries)"
            elif resp.status_code == 200:
                status = f"OK but no entries"
            else:
                status = f"HTTP {resp.status_code}"
            print(f"  [{status}] {label}")
            print(f"     URL: {url}")
            print(f"     Content-Type: {content_type}")
            if entry_count > 0 and feed.entries:
                print(f"     First: {feed.entries[0].get('title', 'N/A')[:80]}")
    except Exception as e:
        print(f"  [ERROR] {label}: {e}")
        print(f"     URL: {url}")


async def main():
    print("Testing RSS feed URLs...\n")
    for label, url in TEST_URLS:
        print(f"--- {label} ---")
        print(f"  URL: {url}")
        await test_url(label, url)
        print()


if __name__ == "__main__":
    asyncio.run(main())