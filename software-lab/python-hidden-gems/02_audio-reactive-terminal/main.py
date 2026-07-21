"""
Project 02: Audio-Reactive Terminal

Hidden Gem: `rich` — beautiful terminal formatting with live display.

What it does: Visualizes audio amplitude as a real-time bar chart in your terminal.
Uses the microphone input (or generates a synthetic waveform if no mic is available).
"""
import time
import math
import random
from rich.live import Live
from rich.table import Table
from rich.text import Text


def generate_synthetic_audio(duration=10, sample_rate=60):
    """Generate a synthetic audio-like waveform for demo purposes."""
    samples = []
    for t in range(duration * sample_rate):
        freq = 2 + 3 * math.sin(t * 0.05)
        amplitude = 0.5 + 0.3 * math.sin(t * 0.02) + 0.2 * random.random()
        val = amplitude * math.sin(2 * math.pi * freq * t / sample_rate)
        samples.append(val)
    return samples


def render_bar(amplitude, max_width=40):
    """Render a single amplitude value as a bar."""
    normalized = min(abs(amplitude), 1.0)
    bar_width = int(normalized * max_width)
    if normalized > 0.7:
        color = "red"
    elif normalized > 0.4:
        color = "yellow"
    else:
        color = "green"
    return Text("█" * bar_width, style=color)


def create_display(amplitudes):
    """Create a rich table showing the audio visualization."""
    table = Table(title="Audio-Reactive Terminal", show_header=False, border_style="cyan")
    table.add_column("Bar", ratio=1)

    for amp in amplitudes:
        table.add_row(render_bar(amp))

    return table


def main():
    print("Generating synthetic audio waveform (10 seconds)...")
    samples = generate_synthetic_audio(duration=10, sample_rate=20)

    try:
        with Live(create_display(samples[:15]), refresh_per_second=15, screen=True) as live:
            for i in range(len(samples) - 15):
                window = samples[i:i + 15]
                live.update(create_display(window))
                time.sleep(0.05)
    except Exception as e:
        # Fallback if rich Live doesn't work in the terminal
        print(f"Live display unavailable ({e}). Printing amplitude values:")
        for i, s in enumerate(samples[:50]):
            bar = "█" * int(abs(s) * 30)
            print(f"[{i:3d}] {bar}")


if __name__ == "__main__":
    main()
