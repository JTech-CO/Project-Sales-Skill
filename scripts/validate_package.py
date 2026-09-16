#!/usr/bin/env python3
"""Offline package integrity checks, not an LLM or live-provider evaluation."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
FOCUSES = {'discovery':'DISCOVERY', 'qualification':'QUALIFICATION', 'outreach':'OUTREACH',
           'triage':'TRIAGE', 'handoff':'HANDOFF', 'review':'REVIEW'}
IGNORED = {'__pycache__', '.git', 'node_modules', '.venv', 'local-output', '.sales-private'}


def check(root: Path = ROOT) -> dict:
    errors = []
    paths = sorted(p for p in root.rglob('*') if p.is_file() and not (set(p.relative_to(root).parts) & IGNORED))
    for p in paths:
        if p.is_symlink():
            errors.append(f'Symlink in package: {p.relative_to(root)}')
    skills = [root/'SKILL.md'] + [root/f'optional-skills/project-sales-{key}/SKILL.md' for key in FOCUSES]
    for p in skills:
        if not p.exists():
            errors.append(f'Missing skill: {p.relative_to(root)}'); continue
        text = p.read_text(encoding='utf-8')
        front = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not front:
            errors.append(f'Missing frontmatter: {p.relative_to(root)}'); continue
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', front.group(1), re.M)
        description = re.search(r'^description: (.+)$', front.group(1), re.M)
        if not name or name.group(1) != p.parent.name or len(name.group(1)) > 64:
            errors.append(f'Invalid/mismatched name: {p.relative_to(root)}')
        if not description or not 1 <= len(description.group(1)) <= 1024:
            errors.append(f'Invalid description: {p.relative_to(root)}')
        if len(text.splitlines()) > 150:
            errors.append(f'Unexpectedly long entrypoint: {p.relative_to(root)}')
        if 'draft-only' not in text:
            errors.append(f'Missing execution boundary: {p.relative_to(root)}')
    link_count = 0
    json_count = 0
    for p in paths:
        if p.suffix in ('.md', '.mjs', '.py', '.json', '.yaml', '.txt', '.html'):
            try:
                text = p.read_text(encoding='utf-8')
            except UnicodeError:
                errors.append(f'Not UTF-8: {p.relative_to(root)}'); continue
            if '\ufffd' in text or '\x00' in text:
                errors.append(f'Replacement/NUL character: {p.relative_to(root)}')
            if p.suffix == '.json':
                try:
                    json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
                    json_count += 1
                except ValueError as error:
                    errors.append(f'Invalid JSON: {p.relative_to(root)}: {error}')
            if p.suffix == '.md':
                # Local Markdown targets only; external URLs are not fetched.
                for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                        continue
                    target = unquote(target.split('#')[0])
                    if not target:
                        continue
                    resolved = (p.parent/target).resolve()
                    if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                        errors.append(f'Broken/outside local link: {p.relative_to(root)} -> {target}')
                    link_count += 1
    for key, filename in FOCUSES.items():
        src = root/'references'/f'{filename}.md'
        dst = root/f'optional-skills/project-sales-{key}/references/FOCUS.md'
        if not src.exists() or not dst.exists() or src.read_bytes() != dst.read_bytes():
            errors.append(f'Out-of-sync standalone reference: {key}')
    lite = root/'LITE.md'
    if lite.exists() and len(lite.read_text(encoding='utf-8').split()) > 600:
        errors.append('LITE exceeds the package 600-word ceiling.')
    fixture = root/'evals/cases.json'
    if fixture.exists():
        cases = json.loads(fixture.read_text(encoding='utf-8'))
        seen = set()
        for case in cases:
            if case['id'] in seen or any(key not in FOCUSES for key in case['expected_capabilities']):
                errors.append(f'Invalid evaluation case: {case.get("id")}')
            seen.add(case['id'])
    checksums = root/'CHECKSUMS.sha256'
    if checksums.exists():
        for line in checksums.read_text(encoding='utf-8').splitlines():
            digest, relative = line.split('  ', 1)
            path = root/relative
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f'Checksum mismatch: {relative}')
    return {'ok': not errors, 'skill_entrypoints': len(skills), 'json_files_checked': json_count,
            'local_markdown_links_checked': link_count, 'files_scanned': len(paths), 'errors': errors,
            'not_tested': ['Live model routing/quality', 'Native host installation UI', 'Live providers and OAuth', 'Production execution controls']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        report = check(args.root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Package validation failed: {error}', file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
