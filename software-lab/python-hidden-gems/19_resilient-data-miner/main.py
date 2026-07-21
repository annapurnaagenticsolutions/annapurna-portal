"""
Project 19: Resilient Data Miner

Hidden Gem: `parsel` — XPath and CSS selectors with a clean API,
built on lxml. More powerful than BeautifulSoup for complex extraction.

What it does: Mines data from multiple simulated sources using XPath
selectors, with fallback strategies and data normalization.
"""
import time
import json
from parsel import Selector


# Simulated HTML pages from different sources
SOURCE_A = """
<html>
<body>
  <div class="product-list">
    <div class="product" data-id="101">
      <h2 class="title">Wireless Headphones</h2>
      <span class="price">$99.99</span>
      <span class="rating">4.5</span>
      <p class="desc">Premium wireless headphones with noise cancellation.</p>
    </div>
    <div class="product" data-id="102">
      <h2 class="title">USB-C Hub</h2>
      <span class="price">$49.99</span>
      <span class="rating">4.2</span>
      <p class="desc">7-in-1 USB-C hub with HDMI and SD card reader.</p>
    </div>
  </div>
</body>
</html>
"""

SOURCE_B = """
<html>
<body>
  <table id="items">
    <tr class="item-row" data-sku="201">
      <td class="name">Mechanical Keyboard</td>
      <td class="cost">$129.00</td>
      <td class="stars">★★★★☆</td>
    </tr>
    <tr class="item-row" data-sku="202">
      <td class="name">Gaming Mouse</td>
      <td class="cost">$59.00</td>
      <td class="stars">★★★★★</td>
    </tr>
  </table>
</body>
</html>
"""


def mine_source_a(html):
    """Extract products from Source A using CSS selectors."""
    sel = Selector(text=html)
    products = []

    for product in sel.css(".product"):
        products.append({
            "source": "A",
            "id": product.attrib.get("data-id", ""),
            "title": product.css(".title::text").get("").strip(),
            "price": product.css(".price::text").get("").strip(),
            "rating": product.css(".rating::text").get("0").strip(),
            "description": product.css(".desc::text").get("").strip(),
        })

    return products


def mine_source_b(html):
    """Extract products from Source B using XPath — different structure."""
    sel = Selector(text=html)
    products = []

    for row in sel.xpath('//tr[@class="item-row"]'):
        stars = row.xpath('.//td[@class="stars"]/text()').get("")
        star_count = stars.count("★")

        products.append({
            "source": "B",
            "id": row.attrib.get("data-sku", ""),
            "title": row.xpath('.//td[@class="name"]/text()').get("").strip(),
            "price": row.xpath('.//td[@class="cost"]/text()').get("").strip(),
            "rating": str(star_count),
            "description": "",
        })

    return products


def normalize_price(price_str):
    """Normalize price strings to float."""
    try:
        return float(price_str.replace("$", "").replace(",", "").strip())
    except (ValueError, AttributeError):
        return 0.0


def merge_and_normalize(all_products):
    """Merge products from different sources into a unified format."""
    normalized = []
    for p in all_products:
        normalized.append({
            "id": p["id"],
            "source": p["source"],
            "title": p["title"],
            "price_usd": normalize_price(p["price"]),
            "rating": float(p["rating"]) if p["rating"] else 0.0,
            "description": p.get("description", ""),
        })

    # Sort by price descending
    normalized.sort(key=lambda x: x["price_usd"], reverse=True)
    return normalized


def main():
    print("--- Resilient Data Miner ---")
    print("Using parsel for XPath + CSS extraction\n")

    start = time.time()

    # Mine from multiple sources
    print("Mining Source A (CSS selectors)...")
    products_a = mine_source_a(SOURCE_A)
    print(f"  Extracted {len(products_a)} products")

    print("Mining Source B (XPath selectors)...")
    products_b = mine_source_b(SOURCE_B)
    print(f"  Extracted {len(products_b)} products")

    # Merge
    all_products = products_a + products_b
    normalized = merge_and_normalize(all_products)

    elapsed = time.time() - start

    print(f"\nMerged & normalized {len(normalized)} products in {elapsed:.3f}s\n")

    print(f"{'ID':>5}  {'Source':>6}  {'Title':<25}  {'Price':>8}  {'Rating':>6}")
    print(f"{'-'*5}  {'-'*6}  {'-'*25}  {'-'*8}  {'-'*6}")

    for p in normalized:
        print(f"{p['id']:>5}  {p['source']:>6}  {p['title']:<25}  "
              f"${p['price_usd']:>7.2f}  {p['rating']:>5.1f}★")

    print(f"\n  ✓ parsel handles both CSS and XPath in one clean API")
    print(f"  ✓ Fallback defaults prevent extraction failures")
    print(f"  ✓ Different source structures → unified normalized format")


if __name__ == "__main__":
    main()
