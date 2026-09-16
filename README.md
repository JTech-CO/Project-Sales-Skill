# Project Sales

**Evidence-led B2B sales skills. Research what matters. Draft honestly. Hand off clearly.**

[한국어](README-KR.md) · [Quick start](QUICKSTART.md) · [LITE](LITE.md) · [Core skill](SKILL.md)

Project Sales is a provider-independent skill package for product/ICP discovery, prospect qualification, outreach drafting, reply triage, meeting handoff, and performance review. It is not an Explee client, a contact database, a mass-mail sender, or a promise of meetings.

**Version 0.1.0: usable, draft-only skill release.** The instructions work with the host's existing capabilities; the included local helpers and app context/read bridge are executable. No live sending, remote draft saves, CRM writes, calendar invitations, scheduler, account authentication, or published plugin is bundled. Distribution license remains [unselected](LICENSE-NOTE.md), as in the planning input.

## Choose one entry route

| Route | Start here | Use when |
|---|---|---|
| Paste-anywhere | [LITE.md](LITE.md) / [LITE-KR.md](LITE-KR.md) | A web, app, or CLI agent accepts text instructions |
| Native skill | [SKILL.md](SKILL.md) and its supporting folders | A host loads SKILL.md directories |
| Focused specialists | [Optional skills](optional-skills/README.md) | A narrow or multi-agent host needs individual capabilities |
| Custom app | [App bridge](adapters/app/README.md) | You want to load guidance and bind authorized read functions |

Start with **one core skill**, not all seven. The core is a small router and reads only relevant reference material. Each of the six optional specialist folders is independently installable. There is no mandatory sales sequence, fixed agent team, model API, or whole-repository context load.

## Capabilities

| Capability | Result | Does not imply |
|---|---|---|
| Discovery | Product facts, ICP hypotheses, exclusions | The prospect needs or will buy the product |
| Qualification | Fit evidence, provenance, verification gaps | A valid address grants permission to contact |
| Outreach | First-message or follow-up draft with supported personalization | A draft is sent or saved remotely |
| Triage | Actual reply intent, evidence, next action | Courtesy or OOO is a hot lead |
| Handoff | Conversation context, commitments, owner/action, booking state | A link or unilateral invitation is a confirmed meeting |
| Review | Cohort-aware outcomes and costs | Missing data is zero or send volume is success |

The ten PS01-PS10 rules in LITE establish scope, evidence, fit, capability fallback, draft-only behavior, approval boundaries, stop/suppression, honest reply classification, truthful metrics, and data/authority separation. Detailed guidance is optional, not an additional mandatory harness.

## Fast start

Paste LITE and a task, or use the local installer from this repository:

```sh
python scripts/install.py --dest ../my-project/.agents/skills --dry-run
python scripts/install.py --dest ../my-project/.agents/skills
```

For a different native host, select that host's actual skill directory. Claude Code commonly uses `.claude/skills`; dated official references and host-specific caveats are in [SOURCES.md](SOURCES.md) and the [CLI guide](adapters/cli/README.md). No installer changes account permissions or existing configuration.

Only need reply triage and handoff?

```sh
python scripts/install.py --dest ../my-project/.agents/skills --select triage handoff
```

The installer refuses existing targets. It does not overwrite host files or install anything unless run explicitly. Generic ZIP upload is not native skill installation; use LITE on hosts without a suitable loader.

## What is in the ZIP

```text
project-sales/
  LITE.md, LITE-KR.md             Copyable minimum contract
  SKILL.md, SKILL-KR.md           Core router and Korean guide
  references/                    Six capabilities + shared optional detail
  optional-skills/               Six self-contained specialist skills
  adapters/                      Web, app, CLI, and MCP integration guidance
  assets/, schemas/              Optional evidence/proposal/handoff contracts
  scripts/                       Local installer, CSV normalizer, validators
  examples/                      Fictional inputs and copyable tasks
  evals/                         Model evaluation prompts and rubric
  tests/                         Executed local utility/bridge checks
  dist/                          Small core and specialist installation ZIPs
```

The full release ZIP is a development/distribution package. [Core ZIP](dist/project-sales-core.zip) contains just the self-contained core skill; [specialist ZIP](dist/project-sales-specialists.zip) contains six independent skill folders. Use the appropriate one for your host rather than attaching every development file.

## Connect to tools without assuming tools

The [ES module](adapters/app/project-sales.mjs) loads LITE plus selected references and maps only reviewed read handlers. Its authorization callback belongs to the host, is checked every call, and must cover account, request, data disclosure, and cost. Returned tool content remains untrusted data. There is no automatic provider fallback.

```sh
node adapters/app/example.mjs
```

This smoke example reads a **fictional local thread** and reports what was loaded. It does not call a model or external account. The [MCP directory](adapters/mcp/README.md) is a mapping contract, not a running server. LITE itself supplies no browsing, mailbox, or calendar capabilities.

## Safety boundary and validation

This route returns drafts or proposals even when an input contains an approval flag or asks for a send. A separate executor would need trusted approvals, current suppression/stop checks, budget reservation, idempotency/reconciliation, and current contact-policy review. Those controls are [specified, not implemented](references/EXECUTION-BOUNDARY.md). Prompts and exchange schemas are not security boundaries or legal clearance.

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/bridge.test.mjs
```

See [validation results](VALIDATION.md) and [testing instructions](tests/README.md). Offline code tests are separate from model behavior evaluations, native-host installation, live-provider tests, and production security reviews. The evaluation prompts are included; model quality results are not fabricated.

## Development and provenance

[Decisions](DESIGN-DECISIONS.md) records the release choices and remaining boundaries. [Sources](SOURCES.md) distinguishes the supplied handoff, the agreed planning direction, SANE's packaging reference, and verified format/host documentation. No vendor conversion claims or contact datasets are redistributed.

Before public open-source distribution, select a license and update [LICENSE-NOTE.md](LICENSE-NOTE.md). The missing license decision does not prevent using the supplied files for the requested project, but this package does not make an unapproved open-source license claim.
