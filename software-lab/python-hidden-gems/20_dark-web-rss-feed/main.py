"""
Project 20: Dark Web RSS Feed

Hidden Gem: `feedparser` — the universal RSS/Atom feed parser.
Handles every feed format, broken XML, and weird encodings gracefully.

What it does: Aggregates RSS feeds from multiple sources, filters by
keywords, and presents a unified feed. Uses public tech news feeds for demo.
"""
import feedparser
import time
from datetime import datetime


FEEDS = [
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "category": "Tech",
    },
    {
        "name": "Python Insider",
        "url": "https://feeds.feedburner.com/PythonInsider",
        "category": "Python",
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "category": "General Tech",
    },
]

KEYWORDS = ["python", "ai", "security", "rust", "open source", "privacy", "llm"]


def fetch_feed(url, timeout=10):
    """Fetch and parse an RSS feed."""
    try:
        feed = feedparser.parse(url, request_headers={
            "User-Agent": "HiddenGemsFeedAggregator/1.0"
        })
        return feed
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def filter_entries(entries, keywords=None):
    """Filter feed entries by keywords (case-insensitive)."""
    if not keywords:
        return entries

    filtered = []
    for entry in entries:
        text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
        if any(kw in text for kw in keywords):
            filtered.append(entry)

    return filtered


def format_entry(entry, source_name, category):
    """Format a feed entry for display."""
    title = entry.get("title", "No title")
    link = entry.get("link", "")
    published = entry.get("published", "Unknown date")
    summary = entry.get("summary", "")

    # Clean summary (strip HTML tags crudely)
    if summary:
        import re
        summary = re.sub(r'<[^>]+>', '', summary)[:150]

    return {
        "title": title,
        "link": link,
        "published": published,
        "summary": summary,
        "source": source_name,
        "category": category,
    }


def main():
    print("--- Dark Web RSS Feed ---")
    print("Aggregating RSS feeds with feedparser\n")

    all_entries = []
    total_fetched = 0

    for feed_info in FEEDS:
        print(f"Fetching: {feed_info['name']}...")
        feed = fetch_feed(feed_info["url"])

        if feed and feed.entries:
            count = len(feed.entries)
            total_fetched += count
            print(f"  ✓ {count} entries")

            for entry in feed.entries[:20]:  # Top 20 per feed
                formatted = format_entry(entry, feed_info["name"], feed_info["category"])
                all_entries.append(formatted)
        else:
            print(f"  ✗ No entries (feed may be offline)")

    print(f"\nTotal entries fetched: {total_fetched}")

    # Filter by keywords
    print(f"\nFiltering by keywords: {', '.join(KEYWORDS)}")
    filtered = [e for e in all_entries if
                any(kw in (e["title"] + " " + e["summary"]).lower()
                    for kw in KEYWORDS)]

    print(f"Matching entries: {len(filtered)}\n")

    print(f"{'Source':<15} {'Title':<60}")
    print(f"{'-'*15} {'-'*60}")

    for entry in filtered[:15]:
        title = entry["title"][:58]
        print(f"{entry['source']:<15} {title}")

    if not filtered:
        print("(No entries matched keywords. Showing top entries instead:)")
        for entry in all_entries[:10]:
            print(f"{entry['source']:<15} {entry['title'][:58]}")

    print(f"\n  ✓ feedparser handles RSS 2.0, Atom 1.0, RSS 1.0, and broken XML")
    print(f"  ✓ Aggregated from {len(FEEDS)} sources")


if __name__ == "__main__":
    main()
