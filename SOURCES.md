# Sources and provenance

Reviewed for packaging on **2026-09-16**. External documentation can change. Source-derived requirements, the prior planning decisions, and newly authored implementation choices are separated below.

## Supplied material

**AutoGTM-class Outbound Agent.md**, supplied in the conversation. Relevant source sections: 0 (pipeline rather than vendor clone), 7-8 (capabilities and open-source boundaries), 10 (control failures to avoid), 11-12 (review dimensions and honest outcomes), 13 (undecided items), and 14 (handoff guidance). The original is not redistributed in this ZIP.

The immediately preceding Project Sales planning answer supplied the six-capability layout, minimal router, optional host adapters, portable evidence/state, draft-only initial release, and separation between instruction text and host-enforced execution. The current user request authorizes building the skill ZIP, names Project Sales, requests SANE-style LITE, and requires web/app/CLI applicability.

This package does not adopt the vendor's marketing statistics, reproduce contact databases, repeat user-review allegations, or claim a new vendor audit. Contact-policy material is a review checklist, not an updated legal summary.

## Inspected packaging reference

- [JTech-CO/SANE LITE.md](https://github.com/JTech-CO/SANE/blob/main/LITE.md), inspected blob `90e69598aa19e5586d12c8287ba35ced79dd7fc6`.
- [JTech-CO/SANE SKILL.md](https://github.com/JTech-CO/SANE/blob/main/SKILL.md), inspected blob `b581fa1c8e8873861ce06cb2e9dc6523550ae3df`.

Adopted the separation of copyable LITE, a bounded native SKILL, and optional references. Project Sales wording, rules, fixtures, and helper code were newly authored; SANE's UI-design rules and visual assets are not copied.

## Format and host documentation

- [Agent Skills specification](https://agentskills.io/specification): directory structure, required name/description frontmatter, naming constraints, optional resources, progressive loading.
- [OpenAI Build skills](https://developers.openai.com/codex/skills/) (redirects to ChatGPT Learn): local skill directories, optional `agents/openai.yaml`, and distinction between standalone skills and plugin distribution.
- [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): concise task descriptions and a minimal root router for multi-workflow skills. This package makes no model-performance benchmark claim.
- [Claude Code skills](https://code.claude.com/docs/en/skills): local `.claude/skills` placement and the distinction between local and other host environments.

These sources informed file layout and usage notes. Native host installation, account connectivity, plugin publication, and model behavior were not proven by reading documentation or running local tests. See VALIDATION.md for the actual test boundary.
