# STEM Concepts Lab — Unified GitHub Pages Suite

This package combines the three subject labs under one static home page.

## Open locally

Open `index.html` in a browser.

## GitHub Pages deployment

Upload all files and folders in this package to the root of a GitHub repository. Then enable GitHub Pages from the repository settings.

Expected root layout:

```text
stem-lab/
├── index.html
├── math_concepts_lab_stable.html
├── physics_concepts_lab_stable.html
├── chemistry_concepts_lab_stable.html
├── math-concepts-lab-v2_0-stable/
└── physics_concepts_lab_class1_10/
```

## Subject links

- Math opens through `math_concepts_lab_stable.html`, which redirects to the Math package folder.
- Physics opens through `physics_concepts_lab_stable.html`, which redirects to the Physics package folder.
- Chemistry opens directly through `chemistry_concepts_lab_stable.html`.

## Notes

- The Math package includes its own assets, manifest, and service worker.
- The Physics package is preserved as uploaded.
- The Chemistry stable page is based on the latest Chemistry v1.8 cross-subject consistency build.
- All labs remain static and suitable for GitHub Pages.
