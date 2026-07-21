"""
Project 16: Log Anomaly Detector

Hidden Gem: `glom` — a declarative data extraction library that makes
nested data access safe and readable. Perfect for structured log parsing.

What it does: Parses structured log entries, extracts fields using glom,
and detects anomalies (error spikes, unusual patterns, timing irregularities).
"""
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from glom import glom, Coalesce, Path


SAMPLE_LOGS = """
2024-01-15 09:00:01 INFO  [auth] User login: user_id=42 ip=10.0.0.1
2024-01-15 09:00:05 INFO  [api] GET /api/users 200 45ms
2024-01-15 09:00:12 INFO  [api] GET /api/orders 200 120ms
2024-01-15 09:00:30 INFO  [auth] User login: user_id=42 ip=10.0.0.1
2024-01-15 09:00:35 WARN  [api] GET /api/search 200 2500ms
2024-01-15 09:01:00 ERROR [api] POST /api/orders 500 30ms
2024-01-15 09:01:05 ERROR [api] POST /api/orders 500 28ms
2024-01-15 09:01:10 ERROR [api] POST /api/orders 500 35ms
2024-01-15 09:01:15 ERROR [api] POST /api/orders 503 30ms
2024-01-15 09:01:20 INFO  [api] GET /api/users 200 50ms
2024-01-15 09:02:00 INFO  [auth] User login: user_id=99 ip=10.0.0.2
2024-01-15 09:02:05 WARN  [api] GET /api/search 200 3000ms
2024-01-15 09:02:10 ERROR [db] Connection timeout after 5000ms
2024-01-15 09:02:15 ERROR [db] Connection timeout after 5000ms
2024-01-15 09:03:00 INFO  [api] GET /api/users 200 45ms
2024-01-15 09:03:30 INFO  [api] GET /health 200 5ms
2024-01-15 09:04:00 WARN  [api] GET /api/search 200 2800ms
2024-01-15 09:04:30 ERROR [api] POST /api/orders 500 30ms
2024-01-15 09:05:00 INFO  [api] GET /api/users 200 48ms
""".strip()


LOG_PATTERN = re.compile(
    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(INFO|WARN|ERROR|DEBUG) '
    r'\[(\w+)\] '
    r'(.+)'
)


def parse_logs(log_text):
    """Parse log text into structured records."""
    records = []
    for line in log_text.strip().split('\n'):
        match = LOG_PATTERN.match(line)
        if match:
            timestamp_str, level, component, message = match.groups()
            records.append({
                "timestamp": timestamp_str,
                "level": level,
                "component": component,
                "message": message,
                "raw": line,
            })
    return records


def detect_anomalies(records):
    """Detect anomalies in log records."""
    anomalies = []

    # 1. Error spike detection — 3+ errors in 60 seconds
    error_times = []
    for r in records:
        if r["level"] == "ERROR":
            ts = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
            error_times.append((ts, r))

    window = timedelta(seconds=60)
    for i, (ts, rec) in enumerate(error_times):
        nearby = [e for t, e in error_times if abs((t - ts).total_seconds()) <= 60]
        if len(nearby) >= 3:
            anomalies.append({
                "type": "Error Spike",
                "severity": "HIGH",
                "count": len(nearby),
                "window": "60s",
                "first_seen": nearby[0]["timestamp"],
                "components": list(set(r["component"] for r in nearby)),
            })

    # 2. Slow response detection — response time > 2000ms
    for r in records:
        time_match = re.search(r'(\d+)ms', r["message"])
        if time_match:
            ms = int(time_match.group(1))
            if ms > 2000:
                anomalies.append({
                    "type": "Slow Response",
                    "severity": "MEDIUM",
                    "response_ms": ms,
                    "timestamp": r["timestamp"],
                    "message": r["message"][:80],
                })

    # 3. Repeated identical errors
    error_msgs = Counter(r["message"] for r in records if r["level"] == "ERROR")
    for msg, count in error_msgs.items():
        if count >= 3:
            anomalies.append({
                "type": "Repeated Error",
                "severity": "HIGH",
                "count": count,
                "message": msg[:80],
            })

    return anomalies


def summarize(records):
    """Summarize log statistics using glom for safe extraction."""
    spec = {
        "total": len(records),
        "by_level": lambda x: Counter(glom(r, "level") for r in x),
        "by_component": lambda x: Counter(glom(r, "component") for r in x),
        "error_count": lambda x: sum(1 for r in x if glom(r, Coalesce("level")) == "ERROR"),
        "warn_count": lambda x: sum(1 for r in x if glom(r, Coalesce("level")) == "WARN"),
    }
    return glom(records, spec)


def main():
    print("--- Log Anomaly Detector ---")
    print("Parsing structured logs with glom\n")

    records = parse_logs(SAMPLE_LOGS)
    print(f"Parsed {len(records)} log entries\n")

    # Summary
    stats = summarize(records)
    print("Log Summary:")
    print(f"  Total entries:  {stats['total']}")
    print(f"  By level:       {dict(stats['by_level'])}")
    print(f"  By component:   {dict(stats['by_component'])}")
    print(f"  Errors:         {stats['error_count']}")
    print(f"  Warnings:       {stats['warn_count']}")

    # Anomalies
    anomalies = detect_anomalies(records)
    print(f"\nAnomalies detected: {len(anomalies)}")
    for a in anomalies:
        print(f"\n  ⚠ {a['type']} [{a['severity']}]")
        for k, v in a.items():
            if k not in ("type", "severity"):
                print(f"    {k}: {v}")


if __name__ == "__main__":
    main()
