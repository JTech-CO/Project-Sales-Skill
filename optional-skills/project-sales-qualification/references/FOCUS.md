# Prospect qualification

Use for a supplied list, a named company, or requested company discovery. Use authorized business sources, user-provided CSV, existing CRM reads, or explicitly approved data providers. Limit each lookup to the requested business task and the access granted by the host.

## Keep four questions separate

1. Is the company a plausible fit for the product? Include positive and negative evidence.
2. Is this the relevant person or role, and is the employment information current?
3. Where did the contact data come from, and what did any address check actually verify?
4. Has the responsible operator established a reviewed basis to make this contact?

None of these answers substitutes for another. Syntax checks do not establish mailbox existence. A provider's validity result does not establish current employment, deliverability, or contact permission. A public address, CSV row, or role title does not prove consent.

## Work proportionately

Preserve useful existing research. Fill only material gaps, subject to approved costs and data destinations. Do not silently buy enrichment or use another account. Record source, retrieved/checked time, and whether evidence is user-supplied, observed, or inferred.

Rank by explained fit, not manufactured buying probabilities. A simple `fit / possible / exclude / insufficient_evidence` label is enough. A requested numerical rubric must have explicit criteria and cannot be presented as calibrated purchase likelihood.

Preserve conflicting records. Flag exact duplicates and likely duplicates without merging different identities or deleting evidence. Do not strip plus tags, collapse Gmail dots, or assume shared domain means the same person. No-address candidates may still be useful companies; do not invent addresses from a naming pattern.

## Output

`candidate | disposition | evidence for/against | contact source | verification status | contact-policy status | next step`

Use `unknown` for missing verification and permission. Mark opted-out, paused, or excluded candidates as not suitable for outreach. In this release, propose suppression changes rather than claiming to persist them.

## Stop condition

When a candidate is excluded or there is no credible fit, explain why. Research completeness is not an obligation to draft. Support useful company-level research even when an individual contact record is unavailable or outside the task scope.
