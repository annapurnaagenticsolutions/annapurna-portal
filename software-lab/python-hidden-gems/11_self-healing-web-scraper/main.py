"""
Project 11: Self-Healing Web Scraper

Hidden Gem: `httpx` + `tenacity` + `selectolax` — modern HTTP client,
retry logic, and fast HTML parsing. A resilient scraping trio.

What it does: Scrapes a webpage with automatic retries, timeout handling,
and CSS selector-based extraction. Heals from network errors gracefully.
"""
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from selectolax.parser import HTMLParser
import time


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    reraise=True,
)
def fetch_page(url, timeout=15):
    """Fetch a URL with retry logic and proper error handling."""
    with httpx.Client(
        headers={"User-Agent": "Mozilla/5.0 (compatible; HiddenGemsBot/1.0)"},
        timeout=timeout,
        follow_redirects=True,
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def extract_links(html, base_url=""):
    """Extract all links from HTML using selectolax."""
    tree = HTMLParser(html)
    links = []

    for node in tree.css("a[href]"):
        href = node.attributes.get("href", "")
        text = node.text(strip=True)

        if href.startswith("http"):
            links.append({"url": href, "text": text})
        elif href.startswith("/") and base_url:
            links.append({"url": base_url + href, "text": text})

    return links


def extract_meta(html):
    """Extract page metadata."""
    tree = HTMLParser(html)

    title_node = tree.css_first("title")
    title = title_node.text(strip=True) if title_node else "No title"

    desc_node = tree.css_first('meta[name="description"]')
    description = desc_node.attributes.get("content", "") if desc_node else ""

    h1_nodes = tree.css("h1")
    headings = [h.text(strip=True) for h in h1_nodes]

    return {"title": title, "description": description, "h1_count": len(headings)}


def main():
    print("--- Self-Healing Web Scraper ---")

    # Use a stable, scraping-friendly site for demo
    url = "https://quotes.toscrape.com/"
    print(f"Target: {url}\n")

    try:
        print("Fetching page (with retry logic)...")
        start = time.time()
        html = fetch_page(url)
        elapsed = time.time() - start
        print(f"✓ Fetched in {elapsed:.2f}s ({len(html)} bytes)\n")

        # Extract metadata
        meta = extract_meta(html)
        print(f"Title:       {meta['title']}")
        print(f"Description: {meta['description'][:80]}...")
        print(f"H1 count:    {meta['h1_count']}")

        # Extract links
        links = extract_links(html, base_url="https://quotes.toscrape.com")
        print(f"\nLinks found: {len(links)}")
        for link in links[:10]:
            print(f"  • {link['text'][:40]:40s} → {link['url'][:60]}")

        # Extract quotes
        tree = HTMLParser(html)
        quotes = tree.css(".quote")
        print(f"\nQuotes found: {len(quotes)}")
        for q in quotes[:5]:
            text_node = q.css_first(".text")
            author_node = q.css_first(".author")
            if text_node and author_node:
                print(f"  \"{text_node.text(strip=True)[:60]}...\"")
                print(f"   — {author_node.text(strip=True)}\n")

    except httpx.HTTPError as e:
        print(f"✗ Network error after retries: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
