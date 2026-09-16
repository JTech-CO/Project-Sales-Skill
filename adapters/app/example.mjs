/** Offline smoke example. No model, internet, real account, or external write. */
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, sep } from 'node:path';
import { loadContext, createReadOnlyBridge } from './project-sales.mjs';

const root = fileURLToPath(new URL('../../', import.meta.url));
const readText = async relativePath => {
  const path = resolve(root, relativePath);
  if (!path.startsWith(resolve(root) + sep)) throw new Error('Path outside package.');
  return readFile(path, 'utf8');
};
const context = await loadContext({ readText, locale: 'ko', modules: ['triage'] });
const bridge = createReadOnlyBridge({
  bindings: [{
    capability: 'threads.read', toolName: 'local.fixture.readThread',
    accountRef: 'fictional-local-only', metered: false,
    read: async ({ threadId }) => {
      if (threadId !== 'thread-example-001') throw new Error('Unknown fictional thread.');
      return JSON.parse(await readText('examples/thread.json'));
    },
  }],
  authorize: async ({ capability, args, accountRef, metered }) => ({
    allowed: capability === 'threads.read' && args.threadId === 'thread-example-001'
      && accountRef === 'fictional-local-only' && metered === false,
  }),
});
const result = await bridge.call('threads.read', { threadId: 'thread-example-001' });
console.log(JSON.stringify({
  title: context.title, execution: context.execution, modules: context.modules,
  loadedPaths: context.paths, instructionCharacters: context.instructions.length,
  fictionalMessagesRead: result.data.messages.length,
  modelCalled: false, externalNetworkUsed: false, remoteChangesMade: false,
}, null, 2));
