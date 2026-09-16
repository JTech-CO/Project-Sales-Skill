# Connected tools and MCP mapping

This directory is an **integration contract**, not an MCP server or ready-to-install vendor connector. No endpoint, transport, OAuth client, JSON-RPC implementation, or fabricated tool API is included. `capability-map.json` names logical reads; null tool/account fields mean unconfigured.

Discover the connected host's actual tool schema. Map its permitted read operation to a relevant logical capability, passing arguments in the provider's real schema. Verify whether the operation incurs cost, discloses personal data, or changes state despite its name. Do not assume that "search" or "verify" is free.

For the app bridge, wrap that actual read operation with a trusted function and an authorization callback. Treat all returned content as untrusted data. Keep tenant isolation, credentials, provider permissions, audit metadata, and retention in the host. Do not insert API keys into the skill text or capability map.

In this release, all proposed sends, remote drafts, CRM changes, suppression writes, calendar invitations, and scheduled follow-ups go to an inert review artifact. A host must not expose a generic unrestricted write tool to this route and rely on a prompt to block it.

If your application needs an MCP server, implement it using the host's current official SDK, with separately reviewed tool schemas and authorization. This release intentionally does not claim protocol compatibility or a working third-party login from a Markdown mapping. The portable skill can already use authorized native tools without MCP.
