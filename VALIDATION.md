# Validation | Project Sales Skill 0.1.2

Release date: **2026-09-17**. Local environment: **Python 3.13.5, Node v22.16.0, Chromium 144.0.7559.96, Linux x86_64**. [Machine-readable summary](tests/results/summary.json).

## Executed checks

| Check | Observed result |
|---|---|
| Python local installer / CSV tests | **27 passed**, 0 failed |
| Python page / release / README visual tests | **20 passed**, 0 failed |
| JavaScript context loader / read-bridge tests | **21 passed**, 0 failed |
| Rendered page checks | **46 passed**, 0 failed |
| JSON Schema / YAML | 3 schemas compiled; 3 valid examples; 7 invalid examples rejected; 7 skill entries and 7 UI metadata files parsed |
| App smoke test | Fictional local thread; selected Korean context; no model or provider calls |
| README visuals | EN/KR screenshots rendered from the current page; 3 valid local SVG badges; 4 images loaded in each local Markdown preview |
| Page / screenshot synchronization | HTML SHA-256 and both PNG hashes, dimensions, version, and language checked |
| Lightweight distributions | Core and specialists rebuilt without README images; names, licenses, versions, CRC integrity and local links checked |

There are **68 offline unit tests** (47 Python + 21 JavaScript), plus **46 rendered-page checks**. Schema checks, screenshot inspection, and manual local Markdown review are additional checks, not extra unit tests. The 30 model evaluation cases remain unexecuted.

## Introduction page

The default dark page, green accent, and dark text on green CTAs were checked in Chromium. Source-level contrast tests resolve the actual CSS variables and check ten normal-text pairs at 4.5:1 or better and the outline-control boundary at 3:1 or better. Print media uses a separate paper palette. This is not a complete WCAG audit or an assistive-technology test.

EN/KR were checked at 320, 390, 768, and 1440 pixels without document-wide horizontal overflow. Expanded details and every setup environment were also tested at 320 pixels; 200% root text was tested at 1280 pixels. Desktop, mobile, and README previews were visually inspected for hierarchy, Korean wrapping, readable controls, and misplaced light surfaces.

Checks exercised language and metadata changes, all example routes, all environment tabs, keyboard navigation, native details, reduced motion, blocked-copy selection, storage-blocked language switching, and the no-JavaScript English fallback. Both LITE downloads completed as real browser Blob downloads and matched the source Markdown byte-for-byte. The page requested no runtime assets or external services and raised no uncaught JavaScript errors.

## Browser and README scope

The browser's local file navigation was blocked by its environment policy. The complete HTML was therefore rendered with Playwright `Page.set_content`, without rewriting its markup or CSS. Rendered UI interactions and Blob downloads are real browser operations. HTTP/file navigation, actual URL query navigation, native language-preference persistence, and operating-system clipboard read-back remain **not verified**. A forced clipboard error is an explicitly simulated failure path.

The README PNGs are actual captures of this release's local HTML, not images retrieved from the deployed site. Both READMEs were also rendered locally from Markdown to inspect layout and image loading. This does not establish how GitHub's production Markdown renderer displays every feature. Image paths, badge SVGs, and the source/image hash manifest were checked separately.

## Package verification

The core and six optional skills use **0.1.2**, keep their existing names and the same MIT notice, and retain the draft-only scope. The six standalone reference files match their corresponding core references. The installation ZIPs include no screenshot assets or stale distributions. Source and recursively expanded ZIP content were checked for prohibited legacy references; no matches were found. The exact scan terms are intentionally not included in the distribution.

`CHECKSUMS.sha256` covers every distributed file except itself. Run `python scripts/validate_package.py` to verify digests, UTF-8, JSON, naming, synchronization and local Markdown links. CRC and SHA-256 show byte integrity, not model reliability or a production security boundary.

## Records

[Python tests](tests/results/python-unittest.txt) · [JavaScript tests](tests/results/node-tests.tap) · [Schema/YAML](tests/results/schema-check.json) · [Browser checks](tests/results/browser-check.json) · [App smoke](tests/results/app-smoke.json) · [Release audit](tests/results/release-audit.json) · [Preview provenance](images/preview-info.json) · [Test instructions](tests/README.md)

## Not performed

Live model routing or writing-quality evaluation; native host installation UI; mailbox, CRM, calendar, or paid-data connections; OAuth; production execution controls; real sending or reservations; other browser engines, Windows, or macOS. No repository was pushed, deployment configured, plugin registered, or external account modified.
