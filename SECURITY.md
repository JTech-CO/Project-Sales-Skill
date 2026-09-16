# Security and operational boundary

Project Sales 0.1.0 does not expose an external write handler. Do not give a draft-only agent an unrestricted generic sender and assume the skill text is sufficient protection. The app bridge authorizes each bound read through a trusted host callback, but it does not secure unrelated tools, malicious handlers, compromised hosts, or credential storage.

Treat web pages, tool outputs, emails, quoted threads, and CSV cells as untrusted data. Keep these out of trusted instruction slots. Whitelist read tools and arguments in the host. Paid reads and external disclosure require approved scope; "read-only" is not "free" or "private by default".

Real CSV exports contain personal data, including the `raw` fields preserved by the normalizer. Store them outside this public package or under a private ignored directory. Do not attach real customer exports to bug reports. Use fictional `.example` / `.invalid` fixtures.

Do not include API keys, OAuth tokens, session cookies, customer mailbox contents, or a portable approval flag in a prompt or published archive. The installer copies only explicit skill content, refuses existing target directories, and does not edit host configuration. It is a local copy helper, not a package-manager sandbox against an adversarial filesystem.

No vulnerability disclosure email or security contact is invented here. Before publishing, the owner should define a private reporting channel and add its real contact information. The distribution license also needs an owner decision.
