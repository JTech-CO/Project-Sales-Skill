# Validation | Project Sales Skill 0.1.1

Release date: **2026-09-17**. Executed locally on Linux with Python 3.13.5, Node v22.16.0, and Chromium through Playwright. Exact environment strings are in the [structured summary](tests/results/summary.json).

## Executed checks

| Check | Observed result |
|---|---|
| Existing local installer / CSV Python unit tests | 27 passed, 0 failed |
| New site / release source Python unit tests | 14 passed, 0 failed |
| Existing JavaScript context / read-bridge tests | 21 passed, 0 failed |
| Rendered introduction-page checks | 42 passed, 0 failed |
| JSON Schema / YAML | 3 schemas compiled; 3 valid examples accepted; 7 deliberate invalid examples rejected; 7 skill entries and 7 UI metadata files parsed |
| App smoke example | Local fictional thread, Korean LITE plus the selected triage reference; no model or external account |
| Page text | Both complete LITE texts match their Markdown source byte-for-byte |
| Page layout | EN/KR at 320, 390, 768, and 1440 pixels; no document-wide horizontal overflow; 200% root-text enlargement at 1280 pixels; expanded details and each setup tab checked at 320 pixels |
| Page interaction | Language and metadata switching; all task examples and setup tabs; keyboard tab navigation and details; blocked-copy fallback; reduced motion; no-JavaScript English fallback |
| Download | Both language variants downloaded by the browser as local Blob files, with the expected filenames and exact source bytes |
| Runtime resources | No external font, CSS, script, image or API request observed during page rendering and interaction |
| Introduction source | Unique IDs, real local anchors, correct repository links, six capabilities, accessible source hooks, and normal-text palette pairs above 4.5:1 checked |

There are **62 offline unit tests** (41 Python + 21 JavaScript) and **42 additional rendered-page checks**. Schema/metadata checks and manual screenshot review are not counted as unit tests. Model behavior fixtures are not counted as successful model evaluations.

## Browser scope

The local managed Chromium blocks HTTP/file URL navigation. For these checks the complete, unmodified `index.html` was loaded using Playwright `Page.set_content`. Rendering, click/keyboard events, native details, responsive layout, and the completed Blob downloads are real browser operations. The blocked-copy case deliberately simulates a denied copy command. Clipboard fallback was exercised, but OS clipboard read-back was not verified.

EN/KR desktop and mobile screenshots were inspected, including text hierarchy, wrapping, LITE controls, and the relationship of the sample task to its output. No full WCAG conformance audit or assistive-technology session was performed.

Native localStorage persistence, actual URL query navigation, HTTP/file loading, other browser engines, Windows/macOS execution, and live repository navigation remain **not verified** here. The implementation catches storage/history errors, and manual language switching was checked with storage blocked. Single-file resource independence is supported by source checks and the asset-free rendered run, not by a successful file-URL test in this environment.

## Package verification

The core and six specialist entries retain their names, use version **0.1.1**, and include the same MIT notice. All six standalone references match their corresponding core reference. Both installation ZIPs are regenerated, extracted and checked for CRC integrity, self-contained Markdown links, metadata, and license presence. Source identity/provenance review and recursive archive-content checks found no prohibited legacy references. The specific cleanup search terms are not embedded in the release.

`CHECKSUMS.sha256` covers distributed files except itself. Run `python scripts/validate_package.py` to verify content digests, UTF-8, JSON, naming, reference synchronization and local links. CRC and SHA-256 verify byte integrity, not model behavior or a production security boundary.

## Reproducible records

[Python unit tests](tests/results/python-unittest.txt), [JavaScript unit tests](tests/results/node-tests.tap), [schema/YAML checks](tests/results/schema-check.json), [browser checks](tests/results/browser-check.json), [app smoke output](tests/results/app-smoke.json), [structured summary](tests/results/summary.json), [release-content audit](tests/results/release-audit.json), and [test instructions](tests/README.md).

## Outside this release validation

Live model routing or writing quality; host installation UI; mailbox/CRM/calendar or paid-data connections; OAuth; production approval/budget/suppression controls; actual sending, deliverability or reservations. The 30 cases in `evals/cases.json` remain evaluation material; `evals/results-template.json` remains `not_run`.

No repository was pushed, no deployment was configured, no public plugin was registered, and no user account was modified. This release is a portable draft-only skill package and an introduction page, not a hosted sales execution platform.
