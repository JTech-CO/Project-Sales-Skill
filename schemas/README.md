# Exchange schemas

JSON Schema draft 2020-12 records for optional machine handoffs. They are not mandatory output formats and do not implement a state machine, verify provenance, or grant authorization. They are not automatically valid input definitions for every model vendor's structured-output subset; adapt and validate against that vendor before binding.

- `action-proposal.schema.json`: fixed proposal-only, unauthorized action data.
- `evidence.schema.json`: a narrow claim and its provenance classification.
- `handoff.schema.json`: conversation status, unknowns, and proposed next action.

Matching examples are in `../assets/`. Drafts with placeholders remain incomplete. `observed_at: null` means unknown, not today's observation. The fixed false fields express a contract and can be checked structurally, but an untrusted JSON document is never an approval token. JSON Schema validates shape, not truth; use a validator with date-time format checking for timestamp checks.
