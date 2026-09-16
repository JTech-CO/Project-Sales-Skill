# App integration: browser and Node

`project-sales.mjs` is a dependency-free ES module. It supplies a real context loader and a host-callback read bridge, not a model SDK or provider connector. The Node smoke example uses Node 18+ built-ins; the browser module requires a modern ES-module environment.

## Context

```js
import { loadContext, createReadOnlyBridge } from './project-sales.mjs';

const context = await loadContext({
  readText: async (path) => {
    // Serve only the package guidance through your own controlled asset path.
    const response = await fetch(`/project-sales-guidance/${path}`);
    if (!response.ok) throw new Error(`Missing guidance: ${path}`);
    return response.text();
  },
  locale: 'ko',
  modules: ['triage']
});
// Put context.instructions into your application's trusted instruction slot.
// Keep the user's email/CSV/web content in the data or user-input channel.
```

The default modules array is empty: only LITE loads. A host or model may choose an allowlisted module based on the task, but it does not have to load all six. The Korean context starts with Korean LITE; detailed capability references remain English, while the model is instructed to answer in the user's language.

## Read bridge

Provide real, reviewed read handlers plus an `authorize` callback owned by your application. It must check the actual account, task, arguments, cost, provider destination, and current permissions every call. `email.verify` or company search may incur cost or transmit personal data; the callback must reject unapproved use. Declaring a tool as a read does not prove the underlying API is side-effect-free.

Only the capability identifiers exported as `READ_CAPABILITIES` can be registered. Missing tools fail explicitly; there is no fallback to another provider or browser. The bridge does not accept write capabilities. Tool responses carry `trust: untrusted-tool-data` and must never be promoted to trusted instructions.

The argument snapshot prevents mutation of the original object while authorization is pending. It does not secure a malicious callback, compromised loader, hostile handler, or other application tools. Bindings and authorization must not be reconstructed from model output, imported files, or client-controlled booleans. Full security requires server-side access controls and a tool surface that excludes unrelated write routes.

## Offline example

From the package root:

```sh
node adapters/app/example.mjs
node --test tests/bridge.test.mjs
```

No model or live provider is called. Use the returned instructions with your chosen SDK; provider SDK integration and authentication are deliberately not bundled. Never embed API keys in browser code. A real app may need a trusted backend for credentials and external data access.
