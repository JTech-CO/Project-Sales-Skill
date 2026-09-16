#!/usr/bin/env python3
"""Install Project Sales folders locally. Never authenticates or overwrites files."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIALISTS = ('discovery', 'qualification', 'outreach', 'triage', 'handoff', 'review')
CORE_ITEMS = ('SKILL.md', 'SKILL-KR.md', 'LITE.md', 'LITE-KR.md', 'references', 'assets', 'agents', 'LICENSE-NOTE.md')


def _symlink_check(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f'Refusing a symlinked path: {part}')


def install(destination: Path, selected: list[str] | None = None, dry_run: bool = False) -> list[dict]:
    """Copy the core or independent specialists after a full no-overwrite preflight."""
    chosen = selected or ['core']
    if len(chosen) != len(set(chosen)):
        raise ValueError('Duplicate selections are not allowed.')
    if any(key not in ('core', *SPECIALISTS) for key in chosen):
        raise ValueError('Unknown skill selection.')
    if 'core' in chosen and len(chosen) > 1:
        raise ValueError('Install the core OR selected specialists, not both by default.')
    raw_destination = destination.expanduser().absolute()
    _symlink_check(raw_destination)
    dest = raw_destination.resolve()
    if dest == ROOT or ROOT in dest.parents:
        raise ValueError('Choose a destination outside this source package.')
    if dest.exists() and not dest.is_dir():
        raise ValueError('Destination must be a directory.')
    plans: list[tuple[Path, list[tuple[Path, Path]]]] = []
    for key in chosen:
        name = 'project-sales' if key == 'core' else f'project-sales-{key}'
        source = ROOT if key == 'core' else ROOT / 'optional-skills' / name
        items = [source / item for item in CORE_ITEMS] if key == 'core' else list(source.iterdir())
        pairs: list[tuple[Path, Path]] = []
        for item in items:
            if not item.exists():
                raise FileNotFoundError(f'Missing package item: {item}')
            _symlink_check(item)
            files = sorted(item.rglob('*')) if item.is_dir() else [item]
            for file in files:
                _symlink_check(file)
                if file.is_file():
                    pairs.append((file, file.relative_to(source)))
        target = dest / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(f'Refusing to overwrite existing skill: {target}')
        plans.append((target, pairs))
    results = [{'path': str(target), 'files': len(pairs), 'dry_run': dry_run} for target, pairs in plans]
    if dry_run:
        return results
    dest.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        for target, pairs in plans:
            # mkdir without exist_ok is the final no-overwrite check.
            target.mkdir()
            created.append(target)
            for source, relative in pairs:
                output = target / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                with source.open('rb') as incoming, output.open('xb') as outgoing:
                    shutil.copyfileobj(incoming, outgoing)
    except Exception:
        for path in reversed(created):
            shutil.rmtree(path)
        raise
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, required=True, help='Host skill directory, outside this source package.')
    parser.add_argument('--select', nargs='+', choices=('core', *SPECIALISTS), help='Default: core; otherwise one or more specialists.')
    parser.add_argument('--dry-run', action='store_true', help='Show copies without creating anything.')
    args = parser.parse_args()
    try:
        result = install(args.dest, args.select, args.dry_run)
    except (ValueError, OSError) as error:
        print(f'Project Sales installer: {error}', file=sys.stderr)
        return 2
    print(json.dumps({'installed': not args.dry_run, 'skills': result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
