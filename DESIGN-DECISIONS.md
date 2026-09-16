# Release decisions | 0.1.0

This is a design/implementation record, not compulsory runtime context.

| Decision | Basis | Status |
|---|---|---|
| Name: Project Sales | Explicit current user request | Implemented |
| Paste-anywhere LITE in English and Korean | User requested SANE-style LITE; its public LITE/SKILL were inspected | Implemented |
| One small core router | Prior agreed planning direction and current skill-format guidance | Implemented |
| Six independently installable specialists | User requested a skill composition usable across web/app/CLI; first-turn plan supplied six capabilities | Implemented as optional, not always active |
| Draft-only first release | Prior plan's initial Portable Core and source's draft/approval/measurement stance | Implemented in skill contract and supplied app bridge's read-only surface |
| No universal write executor | Prior plan separates judgment from actual execution | Deliberately not included; text is not host enforcement |
| Provider-independent reads | Source separates data/sending/booking infrastructure from core | Function-binding contract and offline example implemented; no live provider integration |
| No website or new sales dashboard | Not requested in this turn; portability does not require a new UI | Out of scope |
| No dedicated MCP server or plugin publication | Prior plan does not make either an initial requirement | Integration guidance only |
| Exchange schemas are optional | Prior plan asks for minimal portable state, not JSON on every task | Three optional schemas and examples |
| Local scripts only for deterministic tasks | Current implementation choice | Installer, CSV normalization, package/dist validation |
| No country-specific auto-clearance | Source raises legal dimensions but does not define a valid rules engine | Review checklist; current deployment policy is a host responsibility |
| License not chosen | Original and prior planning explicitly left license open | Pending owner selection; no silent MIT assumption |

## What a live-execution extension would still need

Trusted identity and approvals, suppression and stop persistence, safe provider bindings, transactional cost limits, idempotency/reconciliation, scheduling semantics, applicable contact-policy review, tenant isolation, credential handling, audit/retention, and live-system testing. Merely changing a Markdown sentence or `execution_authorized` field is not a supported upgrade.

## Context budget

LITE stands alone. The core points directly to focused references. Specialists package a shared small boundary plus one focus reference. Development docs, templates, schemas, tests, and eval fixtures are not automatically injected into the model context. The app context loader demonstrates this by loading only LITE and explicitly selected modules.

## Provenance

The attached research is an input, not a live audit of a vendor. Its time-sensitive product statistics and review allegations are not revalidated or promoted into this release's requirements. Current outside research in this build is limited to the named SANE reference, skill format, and host installation conventions. See SOURCES.md.
