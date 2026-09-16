# Project Sales | Quick start

## No installation

Copy [LITE.md](LITE.md) into a text-capable agent and supply your task below it. For Korean use [LITE-KR.md](LITE-KR.md). No external account, Python, or Node is needed for the instruction-only route.

```text
Use Project Sales to evaluate this product brief and the supplied company list.
Return fit/exclusion reasons and one supported first-message draft.
Leave contact verification and permission unknown where not established.
```

## Native skill folder

From the package root, preview then install:

```sh
python scripts/install.py --dest ../my-project/.agents/skills --dry-run
python scripts/install.py --dest ../my-project/.agents/skills
```

Open the host at the target project and confirm that `project-sales` is visible in its skill selector. The copy being successful is not proof of host activation. For Claude Code use the documented `.claude/skills` destination. For other hosts use their actual directory or the LITE route. See [source notes](SOURCES.md).

The small [core ZIP](dist/project-sales-core.zip) is also available for compatible folder/ZIP loaders. Do not assume every web upload is a skill installer.

## App / read-tool connection

```sh
node adapters/app/example.mjs
```

Expected: only `LITE-KR.md` and `references/TRIAGE.md` load, two fictional messages are read, and `modelCalled`, `externalNetworkUsed`, and `remoteChangesMade` are false. For real reads, supply trusted host handlers and authorization in [the app bridge](adapters/app/README.md).

## One specialist

```sh
python scripts/install.py --dest ../reply-agent/.agents/skills --select triage
```

Do not install the core and all specialists together by default. Specialist names and scope are listed in [optional-skills](optional-skills/README.md).

## Important

This release does not send, remotely save drafts, update CRM, create invitations, or schedule background work. It generates proposals. The selected host must expose suitable read tools; no provider connector or key is bundled. Real inputs stay private and should not be committed to this repository.
