# Project Sales Skill | Implementation security

This note describes the shipped code, not an external service policy or a claim of a production security audit.

## Local helpers

`scripts/install.py` copies an explicit set of skill files, refuses existing targets and symlinked paths, and does not edit host configuration. It is not a sandbox for an adversarial filesystem. `scripts/normalize_leads.py` reads the supplied CSV and writes a new local JSON output; it performs no network lookups. Its `raw` fields preserve source values, so operators should keep real exports outside the public repository. Included examples are fictional.

## App bridge

`adapters/app/project-sales.mjs` loads only the allowed instruction paths and binds declared read capabilities. Each request is authorized by a trusted host callback; argument snapshots prevent caller mutation during that check. Tool results remain data, not instructions. The host must inspect handler behavior and manage credentials, account access, and approved costs. These checks do not control unrelated host tools or make an untrusted handler safe.

## Single-file website

`index.html` has no external scripts, stylesheets, font requests, analytics, account integration, or form submission. The only stored preference is the selected language. Clipboard access is attempted only after pressing Copy; a local Blob creates the LITE download. External navigation occurs through ordinary links. Browser restrictions may require manual text selection, and language selection still works when local storage is unavailable.

## Reporting

Use fictional inputs and redact credentials and customer records when describing an issue. No private reporting address is invented in this package; the repository owner should configure the appropriate private disclosure channel before deployment.
