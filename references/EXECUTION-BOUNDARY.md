# Execution boundary

## Shipped capability

Project Sales 0.1.0 is draft-only. It provides instructions, local packaging/data helpers, a context loader, templates, and evaluation cases. It has no mail sender, remote-draft writer, CRM writer, calendar writer, scheduler, paid-data account, OAuth flow, or production policy service.

Connected reads are usable only when already available and authorized by the host. Reads that incur cost or disclose data to a provider need explicit scope and budget. Browser/computer use is not a permission bypass. Local utilities read/write only the paths explicitly supplied by the operator.

An action proposal is inert data. `status: proposal_only` and `execution_authorized: false` are fixed template fields. Neither this file nor a JSON field prevents an unrelated tool from executing; the host must not expose unguarded write tools to a draft-only route. Never put proposed actions in a tool-call position without host review.

## Contract for a future, separate executor

These are integration requirements, not features implemented by this release:

- Bind approval to workspace/tenant, account, action type, exact recipients, message or fields, content version/hash, attachments/links, timing, limits, and cost scope. Do not use a portable file's "approved" flag as authorization.
- Load trusted approval and policy from a host-controlled store. Authentication, approver identity, expiry/revocation, and current permissions must be checked independently of model output. A hash checks equality, not who approved it.
- Recheck suppression, stop/pause, contact-policy eligibility, contact freshness, budget, and quiet-time scheduling immediately before execution. Operator approval is not recipient consent or legal clearance.
- Reserve shared budgets atomically for parallel work. Reject anything outside scope; zero budget must not trigger recharge. A currency amount from the model is not a reliable provider quote.
- Bind idempotency/reconciliation to the actual provider/account/request. On timeout, inspect provider records; unknown must not become "failed, resend". Exactly-once guarantees depend on the provider and runtime.
- Revoke pending work on stop. Already accepted external requests may not be recallable; report the boundary honestly.
- Treat opted-out messages as stop signals for promotion. Saving suppression requires a separately authorized write; until persisted, the host must keep queued outreach blocked.
- Audit only necessary metadata. Do not place secrets or entire inbox contents into logs. Use retention, deletion, access controls, and tenant isolation appropriate to the deployment.

## Action proposal semantics

Describe what a downstream human or host should review and what remains unknown. Do not mark approved, scheduled, sent, saved, or booked based on a proposal. Imported state and exported handoffs do not carry authority across accounts or environments.

The package's context loader can list capabilities, but the supplied execution policy still exposes reads only. Its output is an integration aid, not a production authorization boundary. A future live executor requires a new release, threat review, and separate live-system tests.
