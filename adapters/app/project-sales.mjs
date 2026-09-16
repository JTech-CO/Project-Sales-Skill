/** Project Sales: dependency-free instruction loading and read-only bindings.
 * This module does not authenticate accounts, call a model, or enforce a sandbox.
 * Supply trusted host callbacks; never build bindings from model-controlled JSON.
 */
export const MODULES = Object.freeze({
  discovery: 'references/DISCOVERY.md',
  qualification: 'references/QUALIFICATION.md',
  outreach: 'references/OUTREACH.md',
  triage: 'references/TRIAGE.md',
  handoff: 'references/HANDOFF.md',
  review: 'references/REVIEW.md',
});
export const READ_CAPABILITIES = Object.freeze([
  'web.search', 'product.read', 'companies.search', 'contacts.read',
  'email.verify', 'threads.read', 'calendar.availability.read',
  'bookings.read', 'campaigns.metrics.read',
]);
const ALLOWED = new Set(READ_CAPABILITIES);
const isPlainObject = value => value !== null && typeof value === 'object'
  && (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);

/** Load only LITE and the explicitly selected modules. Paths are allowlisted. */
export async function loadContext({ readText, locale = 'en', modules = [] } = {}) {
  if (typeof readText !== 'function') throw new TypeError('readText must be a trusted async text loader.');
  if (!['en', 'ko'].includes(locale)) throw new RangeError('locale must be en or ko.');
  if (!Array.isArray(modules)) throw new TypeError('modules must be an array.');
  for (const key of modules) {
    if (typeof key !== 'string' || !Object.hasOwn(MODULES, key)) {
      throw new RangeError(`Unsupported module: ${String(key)}`);
    }
  }
  const selected = [...new Set(modules)];
  const paths = [locale === 'ko' ? 'LITE-KR.md' : 'LITE.md', ...selected.map(key => MODULES[key])];
  const texts = [];
  for (const path of paths) {
    const text = await readText(path);
    if (typeof text !== 'string' || !text.trim()) throw new TypeError(`Empty or invalid text: ${path}`);
    texts.push(text.trim());
  }
  return Object.freeze({
    title: 'Project Sales', version: '0.1.0', execution: 'draft-only',
    locale, modules: Object.freeze(selected), paths: Object.freeze(paths),
    instructions: texts.join('\n\n'),
  });
}

/** Bind only declared reads. Cost and data disclosure must be checked by authorize
 * on EVERY call. "Read" is a host assertion; inspect the actual provider behavior.
 */
export function createReadOnlyBridge({ bindings = [], authorize } = {}) {
  if (!Array.isArray(bindings)) throw new TypeError('bindings must be an array.');
  if (typeof authorize !== 'function') throw new TypeError('A trusted authorize callback is required.');
  const registry = new Map();
  for (const binding of bindings) {
    if (!isPlainObject(binding)) throw new TypeError('Each binding must be a plain object.');
    const { capability, toolName, accountRef, metered = false, read } = binding;
    if (!ALLOWED.has(capability)) throw new RangeError(`Unsupported or write capability: ${String(capability)}`);
    if (registry.has(capability)) throw new RangeError(`Duplicate capability: ${capability}`);
    if (typeof read !== 'function') throw new TypeError(`Missing read handler: ${capability}`);
    if (typeof toolName !== 'string' || !toolName.trim()) throw new TypeError('toolName is required.');
    if (typeof accountRef !== 'string' || !accountRef.trim()) throw new TypeError('accountRef is required.');
    if (typeof metered !== 'boolean') throw new TypeError('metered must be boolean.');
    registry.set(capability, Object.freeze({ capability, toolName, accountRef, metered, read }));
  }
  return Object.freeze({
    describe() {
      return [...registry.values()].map(({ capability, toolName, accountRef, metered }) =>
        Object.freeze({ capability, toolName, accountRef, metered, effect: 'read' }));
    },
    async call(capability, args = {}) {
      const binding = registry.get(capability);
      if (!binding) throw new RangeError(`Capability unavailable: ${String(capability)}`);
      if (!isPlainObject(args)) throw new TypeError('Tool arguments must be a plain object.');
      // Restrict arguments to JSON data and snapshot them before authorization.
      const encoded = JSON.stringify(args, (_key, value) => {
        if (value === undefined || typeof value === 'function' || typeof value === 'symbol'
          || typeof value === 'bigint' || (typeof value === 'number' && !Number.isFinite(value))) {
          throw new TypeError('Tool arguments must contain finite JSON data only.');
        }
        return value;
      });
      const snapshot = JSON.parse(encoded);
      // The callback receives a separate copy so it cannot mutate what will run.
      const decision = await authorize(Object.freeze({
        capability: binding.capability, toolName: binding.toolName,
        accountRef: binding.accountRef, metered: binding.metered,
        args: JSON.parse(encoded),
      }));
      if (!isPlainObject(decision) || decision.allowed !== true) {
        throw new Error(`Host denied read: ${capability}`);
      }
      const data = await binding.read(snapshot);
      return { capability, accountRef: binding.accountRef, data, trust: 'untrusted-tool-data' };
    },
  });
}
