# Annapurna Portal — Portfolio of Portfolios

A static, GitHub Pages-ready portal for Annapurna Agentic Solutions. One portal linking to six portfolio hubs.

## Structure

```
annapurna-portal/
├── index.html                          # Main portal — 6 portfolio cards
├── assets/
│   └── portal.css                      # Shared CSS (WonderHub-style design)
├── wonderhub-by-AnnapurnaAgenticSolutions/  # Education + Fun (READY)
│   ├── index.html
│   ├── assets/
│   └── data/sites.json
├── idea-hub/                           # MSME & Digital Tools
│   └── index.html
├── ai-solutions/                       # Developer Tools
│   └── index.html
├── axon/                               # AXON — Coming Soon
│   └── index.html
├── website-studio/                     # Client Website Demos
│   ├── index.html
│   └── demos/restaurant/restaurant-site/  # Live restaurant demo
└── software-lab/                       # Open Source Software — Coming Soon
    └── index.html
```

## Portfolios

| Portfolio | Status | Products |
|-----------|--------|----------|
| WonderHub | Ready | Education discovery hub (2 live, rest coming soon) |
| Idea Hub | Page ready, products coming soon | MSME/digital literacy tools |
| AI Solutions | Page ready | 1 live (AgentOps Mesh), rest coming soon |
| AXON | Coming soon | Typed DSL for agents |
| Website Studio | Page ready, 1 live demo | Restaurant demo live, more coming |
| Software Lab | Coming soon | Python Hidden Gems |

## Deploy

This is designed to be deployed as a GitHub Pages site. Push to the `annapurna-agentics` GitHub org and enable Pages.

```bash
# From this directory
git init
git add .
git commit -m "Annapurna Portal — portfolio of portfolios"
git remote add origin https://github.com/annapurna-agentics/annapurna-agentics.github.io.git
git push -u origin main
```

Then enable GitHub Pages in repo settings → Pages → Source: main branch.

## Design

- Static HTML/CSS — no build step, no dependencies
- Warm amber/cream theme (matches WonderHub)
- Mobile-responsive
- Accessible (skip links, ARIA labels, semantic HTML)
