# Validation | Project Sales 0.1.0

Date: **2026-09-16**. Environment: **Python 3.13.5, v22.16.0, Linux x86_64**.

## Executed checks

| Check | Observed result |
|---|---|
| Local Python installer/CSV tests | **27 passed, 0 failed** |
| JavaScript context/read-bridge tests | **21 passed, 0 failed** |
| JSON Schemas | 3 compiled; 3 valid examples accepted; 7 deliberate invalid examples rejected |
| YAML metadata | 7 skill entrypoints and 7 optional OpenAI UI metadata files parsed and checked |
| Offline app smoke example | Only Korean LITE + triage reference loaded; 2 fictional messages read; no model/network/remote write |
| Installable ZIPs | Both CRC-checked, extracted, and independently checked for naming and self-contained local links |
| Python compatibility | 6 files parsed with Python 3.10 syntax settings; actual runtime tests used 3.13.5 |
| Source package | UTF-8, JSON syntax, known frontmatter fields, local Markdown links, and synchronized specialist references checked |

There are **48 executed offline unit tests**. This number does not include the additional schema/YAML checks or the unexecuted model evaluation cases. Tests used fictional data and temporary local directories.

## Reproducible logs

[Python tests](tests/results/python-unittest.txt), [Node tests](tests/results/node-tests.tap), [schema/YAML results](tests/results/schema-check.json), [app smoke output](tests/results/app-smoke.json), and [structured summary](tests/results/summary.json).

Run `python scripts/validate_package.py` from the package root to check local structure and the release checksum manifest. `CHECKSUMS.sha256` covers distributed package files except itself; byte changes invalidate the corresponding digest. Archive CRC and SHA-256 integrity do not prove model safety or source trust.

## Not verified

Native host installation/activation UI; Windows/macOS execution; real model output/routing; live mailbox, CRM, calendar or paid-data connections; account authentication; production approval/suppression/budget controls; live sending, deliverability, or reservations.

The app example does not call a model or provider. The capability map is not a running MCP server. No public plugin was registered, no repository was pushed, and no user account was modified by packaging.

`evals/cases.json` provides **30 model behavior cases**, and `evals/results-template.json` remains **not_run**. Checking fixture shape is not a successful model evaluation. The skill's draft-only instruction is not an independent security boundary for unrelated tools in a host.

## Release boundary

This is a completed portable **skill package**, not a deployed sales execution platform. License selection remains pending, as the planning input required. The two installable ZIPs omit development-only scripts/tests and load only skill content; the full release archive also contains the development and integration materials.
