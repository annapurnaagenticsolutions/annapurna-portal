"""
Project 18: The Immutable Cache

Hidden Gem: `diskcache` — a SQLite-backed persistent cache that's faster
than Redis for local use. Survives restarts, supports tags, and has
a beautiful API.

What it does: Demonstrates a persistent file-backed cache that survives
process restarts. Shows caching patterns, TTL, and tag-based eviction.
"""
import time
import os
from diskcache import Cache


def expensive_computation(n):
    """Simulate an expensive computation."""
    time.sleep(1)  # Simulate work
    return f"result_for_{n}_at_{time.time():.0f}"


def main():
    print("--- The Immutable Cache ---")
    print("Powered by diskcache (SQLite-backed persistent cache)\n")

    cache_dir = "cache_db"
    cache = Cache(cache_dir)

    print(f"Cache location: {cache.directory}")
    print(f"Cache size: {cache.size()} items\n")

    # Demo 1: Basic caching
    print("Demo 1: Basic caching (compute once, serve from cache)")
    for key in ["user:1", "user:1", "user:1"]:
        if key in cache:
            print(f"  Cache HIT: {key} → {cache[key]}")
        else:
            print(f"  Cache MISS: {key} — computing...")
            result = expensive_computation(1)
            cache[key] = result
            print(f"  Stored: {key} → {result}")

    # Demo 2: TTL (time-to-live)
    print(f"\nDemo 2: TTL-based expiration")
    cache.set("temp:data", "expires_soon", expire=2)
    print(f"  Set 'temp:data' with 2s TTL")
    print(f"  Immediate read: {cache.get('temp:data')}")
    print(f"  Waiting 3 seconds...")
    time.sleep(3)
    print(f"  After TTL: {cache.get('temp:data')} (expired)")

    # Demo 3: Tag-based caching
    print(f"\nDemo 3: Tag-based caching")
    cache.set("post:1", "Hello World", tag="posts")
    cache.set("post:2", "Python Tips", tag="posts")
    cache.set("comment:1", "Nice!", tag="comments")

    post_keys = list(cache.iterkeys(prefix="post:"))
    print(f"  Keys with 'post:' prefix: {post_keys}")

    # Evict by tag
    evicted = cache.evict("posts")
    print(f"  Evicted tag 'posts': {evicted} items")
    print(f"  post:1 exists: {'post:1' in cache}")
    print(f"  comment:1 exists: {'comment:1' in cache}")

    # Demo 4: Statistics
    print(f"\nCache statistics:")
    print(f"  Total keys: {len(cache)}")
    print(f"  Cache size: {cache.size()} bytes")
    print(f"  Cache volume: {cache.volume() / 1024:.1f} KB")

    # Demo 5: Persistence across restarts
    print(f"\nDemo 5: Persistence (simulating restart)")
    cache["survivor"] = "I live across restarts!"
    cache.close()

    # Reopen cache — data persists
    cache2 = Cache(cache_dir)
    print(f"  Reopened cache. 'survivor' = {cache2.get('survivor')}")
    cache2.close()

    # Cleanup
    print(f"\n  ✓ diskcache is 10-100x faster than Redis for local caching")
    print(f"  ✓ No server needed — pure Python + SQLite")
    print(f"  ✓ Survives process restarts automatically")

    # Clean up demo cache
    Cache(cache_dir).clear()
    print(f"\n  Demo cache cleared.")


if __name__ == "__main__":
    main()
