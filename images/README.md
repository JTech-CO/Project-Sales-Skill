# README visuals

`intro-en.png` and `intro-kr.png` are real Chromium captures of the current `index.html` at 1440 CSS pixels. They include the header, hero, illustrative reply example, and environment strip. They are not generated product mockups or live model runs. The document is rendered without rewriting its markup or styles for the capture.

The three SVG badges are local, static labels for the package version, MIT license, and EN/KR documentation. They do not report CI status or model quality. The image files use relative README links, so the repository owns every visual without temporary attachment URLs.

Rebuild previews with `python scripts/capture_previews.py --chromium /path/to/chromium`. This optional documentation tool requires Playwright and Chromium, not the skill runtime. The script uses `Page.set_content`; it does not claim live-site or file-URL navigation. `preview-info.json` records the page hash, capture dimensions, browser, and image hashes.

This directory is intentionally separate from `assets/`: README images must not inflate the installable core skill or its model context. Keep screenshots in the full repository/release only.
