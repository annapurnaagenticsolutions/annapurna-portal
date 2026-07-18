# Math Concepts Lab v2.0 — Stable Class 1–10 Release

Static GitHub Pages learning app for Class 1 to Class 10 math.

## v2.0 focus

This release stabilizes the learning product rather than adding a new subject. It keeps the full Class 1–10 structure and improves deployment readiness, learning flow, and usability.

Included:
- Class-first navigation for Class 1 to Class 10
- 106 visual lessons
- Class 1–5 Activity Mode
- Class 6–8 Bridge Mode
- Class 9–10 Exam Mode
- Chapter mini tests inside the app
- Practice with instant feedback
- Progress tracking using browser LocalStorage
- Learning maps
- Accessibility skip link and visible focus states
- GitHub Pages-ready static files

Not included in v2.0:
- Printable worksheet packs

Reason: this release is positioned as a free guided learning lab. Excluding printable worksheet packs avoids making the project feel like a downloadable/selling-oriented product.

## Deploy

Upload the contents of this folder to a GitHub repository root, then enable GitHub Pages:

`Settings → Pages → Deploy from branch → main → /root`

Main entry file: `index.html`

## Cache note

The service-worker cache name has been updated to `math-concepts-lab-v2-0-stable`. After deployment, hard refresh once if an older GitHub Pages version appears.
