"""
Project 13: Billion-Row Cruncher

Hidden Gem: `polars` — a DataFrame library written in Rust that's 10-100x
faster than pandas for most operations. Lazy evaluation, zero-copy, multithreaded.

What it does: Generates and processes 1 million rows in seconds,
demonstrating Polars' speed advantage over traditional approaches.
"""
import time
import random
import string


def generate_data_polars(n=1_000_000):
    """Generate a large dataset using Polars."""
    import polars as pl
    import numpy as np

    start = time.time()
    df = pl.DataFrame({
        "id": range(n),
        "category": np.random.choice(["A", "B", "C", "D", "E"], n),
        "value": np.random.normal(100, 25, n),
        "flag": np.random.choice([True, False], n),
        "text": ["".join(random.choices(string.ascii_lowercase, k=5)) for _ in range(n)],
    })
    elapsed = time.time() - start
    print(f"  Generated {n:,} rows in {elapsed:.3f}s")
    return df


def benchmark_operations(df):
    """Run common DataFrame operations and time them."""
    import polars as pl

    operations = []

    # Filter
    start = time.time()
    filtered = df.filter(pl.col("value") > 100)
    operations.append(("Filter (value > 100)", time.time() - start, filtered.height))

    # Group by + aggregate
    start = time.time()
    grouped = df.group_by("category").agg([
        pl.col("value").mean().alias("avg_value"),
        pl.col("value").sum().alias("sum_value"),
        pl.col("value").min().alias("min_value"),
        pl.col("value").max().alias("max_value"),
        pl.col("id").count().alias("count"),
    ]).sort("category")
    operations.append(("Group by + 5 aggregations", time.time() - start, grouped.height))

    # Sort
    start = time.time()
    sorted_df = df.sort("value", descending=True)
    operations.append(("Sort by value (desc)", time.time() - start, sorted_df.height))

    # Join (self-join demo)
    start = time.time()
    small = df.head(1000).select(["id", "text"])
    joined = df.join(small, on="id", how="left")
    operations.append(("Left join (1M × 1K)", time.time() - start, joined.height))

    # Window function
    start = time.time()
    windowed = df.with_columns([
        pl.col("value").rank().over("category").alias("rank_in_category"),
        pl.col("value").cum_sum().alias("cumulative_sum"),
    ])
    operations.append(("Window + cumulative sum", time.time() - start, windowed.height))

    return operations, grouped


def main():
    print("--- Billion-Row Cruncher ---")
    print("Powered by Polars (Rust DataFrame engine)\n")

    try:
        n = 1_000_000
        print(f"Generating {n:,} rows...")
        df = generate_data_polars(n)

        print(f"\nSchema: {df.schema}")
        print(f"Memory: {df.estimated_size() / (1024*1024):.1f} MB")

        print(f"\nRunning benchmark operations:")
        print(f"  {'Operation':<35} {'Time':>8}  {'Rows':>10}")
        print(f"  {'-'*35} {'-'*8}  {'-'*10}")

        operations, grouped = benchmark_operations(df)

        for name, elapsed, rows in operations:
            print(f"  {name:<35} {elapsed:>7.3f}s  {rows:>10,}")

        print(f"\nGroup by results:")
        print(grouped)

    except ImportError:
        print("Polars not installed. Install with: pip install polars")
        print("\nPolars is 10-100x faster than pandas for most operations.")
        print("It's a DataFrame library written in Rust with a Python API.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
