# Project Sales Skill | Introduction page

[Open the introduction](https://jtech-co.github.io/Project-Sales-Skill/) · [한국어](SITE-NOTES-KR.md)

The repository-root `index.html` contains the complete page: CSS, JavaScript, EN/KR copy, illustrative task routes, and both full LITE texts. It needs no build, external font, CDN, analytics script, or backend. The screenshots and badges in `images/` belong to the README; the introduction never fetches them.

## Theme and links

Version 0.1.2 uses a dark theme by default, including when the operating system prefers light. There is no new theme toggle. The green accent is `#76dba3`, page background is `#101613`, panel background is `#171f1a`, body text is `#e7eee9`, and secondary text is `#a7b7ac`. Prominent green controls use dark text. Print output uses a paper palette; forced-color and reduced-motion preferences remain supported.

The canonical page URL is `https://jtech-co.github.io/Project-Sales-Skill/`. The repository CTA remains `https://github.com/JTech-CO/Project-Sales-Skill/`. Both README headers link to the published introduction; their screenshots are clickable. Korean screenshot links use `?lang=ko`.

## Open and publish

Open the file directly in a browser that permits local files, or run `python -m http.server 8000` from the repository root. For GitHub Pages, serve the repository root with `index.html` and `.nojekyll`. This release does not change repository settings, push a commit, or redeploy the live site. Local browser-navigation limitations during validation are documented in [VALIDATION.md](VALIDATION.md).

The HTML may be moved by itself. External documentation and repository links still require internet access; the page's own interactions require no remote assets. Metadata links are descriptive, not runtime dependencies.

## Interaction

English is the first-visit default. EN/KR switches the page, examples, LITE, and related metadata. `?lang=en` or `?lang=ko` takes priority over a saved language. Storage errors do not block manual switching. Language selection is the only locally stored preference.

The examples are explanatory samples, not model runs. Web/app/CLI tabs expose real usage paths. LITE copying tries the Clipboard API and then selection-based copying. When neither works, the interface selects the text and reports the need for a manual copy. Downloads contain the active LITE source exactly. Without JavaScript, English content, LITE text, and links remain available while inactive controls stay hidden.

## README images and maintenance

The EN/KR previews are actual local Chromium captures of the current HTML, not screenshots retrieved from the live deployment. The three local SVG badges report only version, license, and documentation languages, not test or model quality. All image paths are repository-relative; no temporary attachment or invented image-host URLs are used.

To refresh previews after changing the page, run `python scripts/capture_previews.py --chromium /path/to/chromium`. The optional tool requires Playwright. Its source/image hashes and capture dimensions are written to `images/preview-info.json`; regression tests detect stale previews. The `images/` folder is excluded from the lightweight core and specialist distributions.

Keep LITE source files, the embedded JSON, and initial textarea synchronized. Update release metadata, all skill versions, schemas and examples together. Run the tests, regenerate `dist/`, and regenerate `CHECKSUMS.sha256` last. See [test instructions](tests/README.md).
