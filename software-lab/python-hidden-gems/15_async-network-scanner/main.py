"""
Project 15: Async Network Scanner

Hidden Gem: `asyncio` — Python's built-in async I/O for concurrent
network operations without threads.

What it does: Scans ports on a host concurrently using asyncio.
Demonstrates connection pooling, timeouts, and async patterns.
"""
import asyncio
import socket
import time
from datetime import datetime


async def scan_port(host, port, timeout=1.0):
    """Scan a single port asynchronously."""
    try:
        future = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(future, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return port, False


async def scan_host(host, ports, concurrency=100):
    """Scan multiple ports concurrently with a semaphore."""
    semaphore = asyncio.Semaphore(concurrency)
    results = []

    async def limited_scan(port):
        async with semaphore:
            return await scan_port(host, port)

    tasks = [limited_scan(p) for p in ports]
    completed = await asyncio.gather(*tasks)

    for port, is_open in completed:
        if is_open:
            results.append(port)

    return results


COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
    27017: "MongoDB",
}


def main():
    print("--- Async Network Scanner ---")
    print("Using asyncio for concurrent port scanning\n")

    # Scan localhost (safe target)
    host = "127.0.0.1"
    ports = list(COMMON_PORTS.keys())

    print(f"Target: {host}")
    print(f"Ports:  {len(ports)} common ports")
    print(f"Time:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    start = time.time()

    try:
        open_ports = asyncio.run(scan_host(host, ports, concurrency=50))
    except RuntimeError:
        # Fallback for environments where asyncio.run doesn't work
        loop = asyncio.new_event_loop()
        open_ports = loop.run_until_complete(scan_host(host, ports, concurrency=50))
        loop.close()

    elapsed = time.time() - start

    print(f"Scan completed in {elapsed:.2f}s\n")

    if open_ports:
        print(f"Open ports ({len(open_ports)}):")
        for port in sorted(open_ports):
            service = COMMON_PORTS.get(port, "Unknown")
            print(f"  {port:>5}  {service}")
    else:
        print("No open ports found on common ports.")
        print("(This is normal for a basic local machine.)")

    print(f"\nScanned {len(ports)} ports in {elapsed:.2f}s "
          f"({len(ports)/elapsed:.0f} ports/sec)")


if __name__ == "__main__":
    main()
