# CLI integration

The agent skill itself requires no Python or Node runtime. The optional installer and normalizer use Python 3.10+ standard library. The app smoke example and bridge tests use Node 18+.

## Install one portable core

Run from this package's root, targeting a **different project directory**:

```sh
python scripts/install.py --dest ../my-project/.agents/skills --dry-run
python scripts/install.py --dest ../my-project/.agents/skills
```

For Claude Code, replace the destination with `../my-project/.claude/skills`. These documented host paths were checked on 2026-09-16; consult [the source notes](../../SOURCES.md) for host documentation. On Windows, `py -3` may be used instead of `python` when that is the installed launcher.

The default installs only `project-sales`. It copies the entrypoint, language guide, LITE files, references, assets, metadata, and license note. The helpers, tests, examples, and app bridge remain in the development package; they are not required by the installed prompt skill.

## Narrow agents / specialists

```sh
python scripts/install.py --dest ../my-project/.agents/skills --select triage handoff --dry-run
python scripts/install.py --dest ../my-project/.agents/skills --select triage handoff
```

Each selected skill is standalone. Do not install the core and every specialist by default. The installer refuses existing targets and symlinked destinations; it never overwrites `AGENTS.md`, `CLAUDE.md`, host settings, accounts, or existing skills. To upgrade, back up and remove or relocate the exact older skill folder yourself, then install again. A dry run creates nothing.

## Local CSV review helper

```sh
python scripts/normalize_leads.py examples/leads.csv local-output/leads.json
```

The UTF-8/UTF-8-BOM CSV needs a `company` header. Other recognized columns are `domain`, `contact_name`, `role`, `email`, `source_url`, and `collected_at`; extra fields are preserved as inert strings in `raw`. Duplicate headers or malformed field counts fail explicitly. Existing output files are not overwritten.

The helper preserves all nonblank rows, flags exact email duplicates without merging, flags local-part case variations, and preserves plus tags. Lowercasing the domain is normalization, not verification. ASCII-style email syntax is only a conservative plausibility check; international or unusual valid addresses may require specialist validation. Imported consent/approval claims remain untrusted and do not become permission. No DNS, SMTP, enrichment, CRM, or mail API is called.

Limits of 8 MiB and 10,000 records are local helper defaults, not marketing benchmarks or legal thresholds. Formula-like CSV text is exported as JSON data, never executed. Output contains the imported raw data: keep real records out of Git and apply your own retention policy.

## Validation

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/bridge.test.mjs
node adapters/app/example.mjs
```

The validation command checks package structure and local links, not native host behavior. JSON Schema checks are an additional optional developer check described in [the testing guide](../../tests/README.md).
