# Host adapters

These adapters connect the skill's **instructions and read capabilities**, not a mail sender. They do not install third-party apps, register an MCP server, authenticate accounts, or provide a published plugin.

| Host | Shipped path | What actually works |
|---|---|---|
| Any text-capable web/app agent | [Web guide](web/README.md) | Paste LITE with task input, no local runtime needed |
| Custom browser/Node app | [App bridge](app/README.md) | Load selected guidance and call explicitly bound, authorized read functions |
| Local agent / CLI | [CLI guide](cli/README.md) | Install self-contained skill folders; normalize local CSV to JSON |
| Connected tools / MCP host | [MCP mapping](mcp/README.md) | Map existing reads by capability; contract and integration guidance, no server |

The caller chooses the host. Instructions never assume a shell or network. Host-specific paths and support notes are documented with source links in SOURCES.md. No native-app or live-account compatibility claim is made from offline tests.
