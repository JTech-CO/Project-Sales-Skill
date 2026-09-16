# Project Sales Skill | Introduction page

The repository-root `index.html` is the whole website. CSS, JavaScript, both translations, sample views, and both complete LITE documents are embedded. There is no build command, dependency installation, remote font, CDN, analytics, backend, or external runtime asset.

## Open and publish

Open the file directly for local reading, or serve the repository root, for example with `python -m http.server 8000`. To host on GitHub Pages, publish the repository root containing `index.html`. This package does not configure repository settings or confirm a public deployment. The repository CTA is `https://github.com/JTech-CO/Project-Sales-Skill/`.

The filename can be moved alone to another directory without breaking page interactions. Repository documentation links require connectivity; local LITE copying and downloads do not. No other package files are fetched by the page.

## Interactions

English is the first-visit default. EN/KR changes text and relevant metadata; `?lang=en` and `?lang=ko` override a stored preference. Only the language preference is stored, with a guarded fallback when storage is blocked. Task examples are fixed illustrations, not live model inference. Web/app/CLI tabs explain the actual package entry routes. Copy LITE uses the clipboard when available, then a selection-based fallback. If copying is blocked, the page selects the text and explicitly asks for manual copying. Download creates a local `.md` file with the exact active LITE text.

The site uses system fonts with Korean fallbacks, visible keyboard focus, semantic headings, native disclosure controls, reduced-motion support, and responsive reflow. JavaScript-disabled viewing retains the English introduction, LITE text, and repository links; interactive controls are hidden. It does not silently claim a copy succeeded.

## Maintenance

When either LITE document changes, synchronize the embedded JSON and initial textarea in `index.html`; the site-source tests reject drift. Update `package-info.json`, displayed version, schema versions, and SKILL metadata together for releases. Run the documented tests and regenerate `dist/` and `CHECKSUMS.sha256` after editing. Browser results and limitations are in [VALIDATION.md](VALIDATION.md).

The root `.nojekyll` marker is included for static-file publishing on GitHub Pages. No repository setting or deployment is changed by this package.
