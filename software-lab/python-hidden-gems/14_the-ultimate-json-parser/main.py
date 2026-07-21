"""
Project 14: The Ultimate JSON Parser

Hidden Gem: `orjson` — the fastest JSON library for Python.
3-10x faster than the stdlib json module, with native support for
datetime, numpy, and UUID serialization.

What it does: Benchmarks orjson against stdlib json, demonstrates
advanced features like serialization of complex types.
"""
import json
import time
import uuid
import random
import string
from datetime import datetime, timezone


def generate_large_json(n=100_000):
    """Generate a large JSON-serializable data structure."""
    records = []
    for i in range(n):
        records.append({
            "id": i,
            "uuid": str(uuid.uuid4()),
            "name": "".join(random.choices(string.ascii_letters, k=20)),
            "email": f"user{i}@example.com",
            "score": random.uniform(0, 100),
            "tags": random.sample(["python", "rust", "json", "fast", "async", "api"], 3),
            "active": random.choice([True, False]),
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    return records


def benchmark_serialize(data, iterations=5):
    """Benchmark JSON serialization."""
    # stdlib json
    start = time.time()
    for _ in range(iterations):
        json.dumps(data)
    stdlib_time = (time.time() - start) / iterations

    try:
        import orjson
        start = time.time()
        for _ in range(iterations):
            orjson.dumps(data)
        orjson_time = (time.time() - start) / iterations
        speedup = stdlib_time / orjson_time
    except ImportError:
        orjson_time = None
        speedup = None

    return stdlib_time, orjson_time, speedup


def benchmark_deserialize(data, iterations=5):
    """Benchmark JSON deserialization."""
    serialized = json.dumps(data)

    start = time.time()
    for _ in range(iterations):
        json.loads(serialized)
    stdlib_time = (time.time() - start) / iterations

    try:
        import orjson
        orjson_serialized = orjson.dumps(data)
        start = time.time()
        for _ in range(iterations):
            orjson.loads(orjson_serialized)
        orjson_time = (time.time() - start) / iterations
        speedup = stdlib_time / orjson_time
    except ImportError:
        orjson_time = None
        speedup = None

    return stdlib_time, orjson_time, speedup


def main():
    print("--- Ultimate JSON Parser ---")
    print("Benchmarking orjson vs stdlib json\n")

    n = 50_000
    print(f"Generating {n:,} records...")
    data = generate_large_json(n)

    serialized_size = len(json.dumps(data)) / (1024 * 1024)
    print(f"Serialized size: {serialized_size:.1f} MB\n")

    # Serialize benchmark
    print("Serialization (dict → bytes):")
    std_time, orj_time, speedup = benchmark_serialize(data)
    print(f"  stdlib json: {std_time*1000:.1f} ms")
    if orj_time:
        print(f"  orjson:      {orj_time*1000:.1f} ms")
        print(f"  Speedup:     {speedup:.1f}x faster")
    else:
        print("  orjson:      not installed (pip install orjson)")

    # Deserialize benchmark
    print(f"\nDeserialization (bytes → dict):")
    std_time, orj_time, speedup = benchmark_deserialize(data)
    print(f"  stdlib json: {std_time*1000:.1f} ms")
    if orj_time:
        print(f"  orjson:      {orj_time*1000:.1f} ms")
        print(f"  Speedup:     {speedup:.1f}x faster")
    else:
        print("  orjson:      not installed (pip install orjson)")

    # Feature demo
    if orj_time:
        import orjson
        print(f"\norjson extra features:")
        print(f"  • Native datetime serialization (no default= handler needed)")
        print(f"  • Native UUID serialization")
        print(f"  • Native numpy array serialization (with OPT_SERIALIZE_NUMPY)")
        print(f"  • Returns bytes (not str) — skip encoding step")
        print(f"  • Thread-safe and zero-copy where possible")


if __name__ == "__main__":
    main()
