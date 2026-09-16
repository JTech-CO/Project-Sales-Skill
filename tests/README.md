# Tests

## Standard-library offline tests

```sh
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/bridge.test.mjs
python scripts/validate_package.py
node adapters/app/example.mjs
```

Python tests cover dry-run installation, self-contained selection, no-overwrite checks, symlink refusal, CSV provenance, duplicates, formula-like text, missing fields, and errors. Node tests cover minimal context loading, module/path restrictions, per-call read authorization, absent tools, argument snapshots, and untrusted results.

`validate_package.py` checks the known package's required frontmatter fields, JSON syntax, UTF-8 text, local Markdown targets, synchronized standalone references, evaluation IDs, and optional checksum manifest. It is not a general YAML or Agent Skills certification tool.

## Additional schema/YAML check

```sh
python tests/validate_schemas.py
```

This optional developer check requires `jsonschema` (draft 2020-12 support) and `PyYAML`. They are not runtime dependencies of the skills, installer, normalizer, or app bridge. The release validation environment already had both installed; the script exits with a clear error when missing. It checks valid examples, deliberate invalid records, all SKILL frontmatter, and all OpenAI UI metadata.

## Model and integration limits

See [the evaluation rubric](../evals/RUBRIC.md). No included offline test sends real mail, calls a model, authenticates a live provider, proves native-host UI installation, or validates production governance. The app bridge requires trusted application callbacks. These boundaries must remain visible in release claims.
