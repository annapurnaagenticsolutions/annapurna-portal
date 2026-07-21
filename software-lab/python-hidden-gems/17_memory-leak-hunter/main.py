"""
Project 17: Memory Leak Hunter

Hidden Gem: `tracemalloc` — Python's built-in memory allocation tracker.
No external dependencies. Shows exactly which lines allocate the most memory.

What it does: Runs code that intentionally leaks memory, then uses
tracemalloc to identify the exact source of the leak.
"""
import tracemalloc
import time
import sys
import gc


# Simulate a memory leak — a global cache that grows unbounded
_LEAK_CACHE = []


def leaky_function(n=10000):
    """Simulate a function that leaks memory by accumulating objects."""
    for i in range(n):
        _LEAK_CACHE.append({
            "id": i,
            "data": list(range(100)),
            "text": f"leaked_object_{i}" * 10,
        })


def clean_function(n=10000):
    """A properly written function that cleans up."""
    local_data = []
    for i in range(n):
        local_data.append({
            "id": i,
            "data": list(range(100)),
            "text": f"clean_object_{i}" * 10,
        })
    # Process and release
    result = sum(len(d["data"]) for d in local_data)
    del local_data
    return result


def take_snapshot(label):
    """Take a memory snapshot and print top allocations."""
    snapshot = tracemalloc.take_snapshot()
    top = snapshot.statistics("lineno")

    print(f"\n  Memory snapshot: {label}")
    print(f"  {'File':<40} {'Size':>10}")
    print(f"  {'-'*40} {'-'*10}")

    for stat in top[:10]:
        frame = stat.traceback[0]
        filename = f"{frame.filename.split('/')[-1]}:{frame.lineno}"
        size_kb = stat.size / 1024
        print(f"  {filename:<40} {size_kb:>8.1f} KB")

    return snapshot


def main():
    print("--- Memory Leak Hunter ---")
    print("Using tracemalloc to track Python memory allocations\n")

    tracemalloc.start()

    # Baseline
    print("Phase 1: Baseline")
    snapshot1 = take_snapshot("Before any work")

    # Run leaky function
    print(f"\nPhase 2: Running leaky_function (accumulating objects in global cache)")
    leaky_function(5000)
    snapshot2 = take_snapshot("After leaky_function")

    # Compare
    print(f"\nPhase 3: Memory diff (what grew the most)")
    diff = snapshot2.compare_to(snapshot1, "lineno")
    print(f"  {'File':<40} {'Growth':>10}")
    print(f"  {'-'*40} {'-'*10}")
    for stat in diff[:10]:
        frame = stat.traceback[0]
        filename = f"{frame.filename.split('/')[-1]}:{frame.lineno}"
        growth_kb = stat.size_diff / 1024
        print(f"  {filename:<40} {growth_kb:>+8.1f} KB")

    # Run clean function
    print(f"\nPhase 4: Running clean_function (local scope, no leak)")
    result = clean_function(5000)
    gc.collect()
    snapshot3 = take_snapshot("After clean_function + gc.collect()")

    # Final comparison
    print(f"\nPhase 5: Total diff (baseline → final)")
    total_diff = snapshot3.compare_to(snapshot1, "lineno")
    print(f"  {'File':<40} {'Growth':>10}")
    print(f"  {'-'*40} {'-'*10}")
    for stat in total_diff[:5]:
        frame = stat.traceback[0]
        filename = f"{frame.filename.split('/')[-1]}:{frame.lineno}"
        growth_kb = stat.size_diff / 1024
        print(f"  {filename:<40} {growth_kb:>+8.1f} KB")

    print(f"\n  ✓ The leak is in the global _LEAK_CACHE — it never gets cleared.")
    print(f"  Fix: use a bounded cache (e.g., functools.lru_cache or a dict with max size)")

    tracemalloc.stop()


if __name__ == "__main__":
    main()
