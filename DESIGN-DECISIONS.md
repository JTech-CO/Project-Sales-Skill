# Project Sales Skill | Release decisions 0.1.1

This is a maintenance record, not required runtime context.

| Decision | Current implementation |
|---|---|
| Public identity | Project Sales Skill; stable core slug `project-sales` |
| Minimal entry route | Standalone LITE in English and Korean |
| Default native installation | One compact router plus focused references |
| Optional specialists | Six self-contained skill folders; install only the needed subset |
| Execution | Analysis, drafts, proposals, and host-authorized reads; no bundled remote writer |
| Tool connections | A JavaScript context loader and host-bound read bridge; no assumed account or provider |
| Introduction | One responsive `index.html` containing CSS, JavaScript, EN/KR copy, and LITE texts |
| Website design | SANE task hierarchy, readable text, restrained light theme, working controls |
| Integration guidance | Web, app, CLI, and MCP mapping notes; MCP is documentation rather than a server |
| Data exchange | Three optional JSON Schemas, not compulsory output formats |
| Local helpers | Installer, CSV normalizer, distribution builder, package and test checks |
| License | MIT; copied from the project repository LICENSE, checked 2026-09-17 |

## Runtime context

The router loads only relevant references. LITE works without other files. Development notes, schemas, test fixtures, and the introduction page are not automatically injected into model context. Each standalone specialist contains its own focus reference.

## Release compatibility

The core and specialist names, installation commands, and JavaScript function signatures are unchanged. Package metadata, skill metadata, module output, JSON Schema identifiers, and example `schema_version` values are updated to 0.1.1. When importing an older structured record, explicitly validate or migrate it to the current schema; a version update does not verify its contents.

## Execution boundary

Instructions describe intent. The included bridge exposes only registered read capabilities and calls a trusted host authorization callback for every request. The host remains responsible for actual handler behavior, credentials, account isolation, and any separate write path. The static introduction never connects to accounts or executes sales operations.
