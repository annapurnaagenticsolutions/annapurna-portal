# Python Hidden Gems

![License](https://img.shields.io/badge/license-MIT-blue)
![Projects](https://img.shields.io/badge/projects-100-green)
![Status](https://img.shields.io/badge/status-Phase%201%20%2820%20done%29-orange)

100 Python mini-projects using interesting, lesser-known, and powerful packages from PyPI.

Each project is a self-contained script — clone, install requirements, run.

## Why?

Most Python tutorials use the same 10 packages. This collection explores the other 400,000+ packages on PyPI — the hidden gems that solve real problems elegantly but rarely get attention.

## Project Catalog

### Phase 1 — Working Now (01-20)

| # | Project | Hidden Gem Package | What It Does |
|---|---------|-------------------|--------------|
| 01 | The Glitch Art Generator | `pillow`, `numpy` | Corrupts image channels & spatial warps to create glitch art |
| 02 | Audio-Reactive Terminal | `soundcard`, `rich` | Real-time audio visualization in your terminal |
| 03 | Automated YouTube Shorts | `yt-dlp`, `moviepy` | Downloads videos and extracts short clips automatically |
| 04 | Facial Recognition Security Cam | `face-recognition` | Webcam face detection with logging and alerts |
| 05 | PDF Presentation Maker | `fpdf2` | Generates PDF slide decks from markdown-ish input |
| 06 | QR Code Art | `qrcode`, `pillow` | Generates stylized QR codes with embedded images |
| 07 | The Structured Output Enforcer | `pydantic`, `instructor` | Forces LLM outputs into validated JSON schemas |
| 08 | Local Vector Brain | `chromadb` | In-memory vector search without a server |
| 09 | Codebase Interrogator | `radon`, `ast` | Analyzes Python codebases for complexity & maintainability |
| 10 | The Aggressive Linter AI | `ruff` | Runs ruff with custom rules and AI-suggested fixes |
| 11 | Self-Healing Web Scraper | `httpx`, `tenacity`, `selectolax` | Scrapes with retry, fallback, and auto-repair |
| 12 | The Local Audio Transcriber | `faster-whisper` | Offline speech-to-text using Whisper models |
| 13 | Billion-Row Cruncher | `polars` | Processes 1M+ rows in seconds using Polars |
| 14 | The Ultimate JSON Parser | `orjson`, `msgspec` | Parses & validates JSON 10x faster than stdlib |
| 15 | Async Network Scanner | `asyncio` | Concurrent port scanner using raw asyncio |
| 16 | Log Anomaly Detector | `glom`, `regex` | Extracts & detects anomalies in structured logs |
| 17 | Memory Leak Hunter | `pympler`, `tracemalloc` | Tracks Python memory allocations & finds leaks |
| 18 | The Immutable Cache | `diskcache` | Persistent, fast, file-backed cache that survives restarts |
| 19 | Resilient Data Miner | `httpx`, `parsel` | Mines data from multiple sources with XPath resilience |
| 20 | Dark Web RSS Feed | `feedparser`, `httpx` | Aggregates RSS feeds from any source with filtering |

### Phase 2 — WIP (21-100)

Projects 21-100 are scaffolded with descriptions and suggested packages. They need code contributions.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to pick up a WIP project.

**Categories:**
- **21-40:** Agentic AI, Data Engineering, Compliance
- **41-60:** DevOps, Infrastructure, Database tools
- **61-80:** Security, Cloud Cost, LLM tools
- **81-100:** Media, Multimodal, Generative

## Quick Start

```bash
# Pick any project
cd 01_the-glitch-art-generator

# Install dependencies
pip install -r requirements.txt

# Run it
python main.py
```

## Project Structure

```
NN_project-name/
  main.py           # Self-contained script
  requirements.txt  # Pinned dependencies
  .env.example      # Environment variable template (if needed)
  Dockerfile        # Optional container
  Makefile          # run / build / test targets
```

## Contributing

Pick any WIP project (21-100), write working code, submit a PR. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Sibling Projects

| Project | Description |
|---------|-------------|
| [AXON](https://github.com/annapurna-agentics/axon) | Typed DSL for autonomous agents — compiles to Python + TypeScript |
| [AgentOps Mesh](https://github.com/annapurna-agentics/agentops-mesh) | Governance control plane for enterprise AI agents |
| [Audit Toolkit](https://github.com/annapurna-agentics/audit-toolkit) | Zero-dependency audit tools for AI IDE and browser configs |
| [Expert Evaluator Suite](https://github.com/annapurna-agentics/expert-evaluator-suite) | 23 expert evaluator prompts for Claude |
| [Agentic Patterns Cookbook](https://github.com/annapurna-agentics/agentic-patterns-cookbook) | Reusable agentic solution patterns with code examples |

## License

MIT — see [LICENSE](LICENSE). Built by [Annapurna Agentic Solutions](https://github.com/annapurna-agentics).
