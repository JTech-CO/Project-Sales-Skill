# Optional standalone specialists

Install **either** the core `project-sales` skill **or** the specialists relevant to the agent. Do not install all seven by default: this increases routing overlap without adding capabilities.

Each specialist is self-contained. Its SKILL.md carries the shared minimum boundaries and its own `references/FOCUS.md`. No relative dependency on a sibling skill or the repository root is required. The installer can select several specialists for a multi-agent host, or one for a narrow agent. Use explicit skill selection if core and specialist installations coexist intentionally.

| Folder suffix | Scope |
|---|---|
| discovery | Product, offer, ICP and exclusions |
| qualification | Candidate fit and provenance |
| outreach | First-touch and follow-up drafts |
| triage | Existing reply interpretation |
| handoff | Interested-conversation and meeting handoff |
| review | Supplied campaign outcomes and cost |

The focused reference is a synchronized copy of the canonical reference in the root package. Package validation checks equality; edit the canonical reference and update its specialist copy together. This duplication exists for standalone portability, not to load all references at once.
