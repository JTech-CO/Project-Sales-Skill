#!/usr/bin/env python3
"""Normalize local CSV to review-only JSON. No network, lookup, approval, or sending."""
from __future__ import annotations
import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
POLICY_FIELDS = {'approved', 'consent', 'verified', 'contact_permission', 'permission', 'suppression'}


def _email(value: str) -> tuple[str, str]:
    value = value.strip()
    if not value:
        return '', 'missing'
    if value.count('@') != 1:
        return value, 'invalid'
    local, domain = value.rsplit('@', 1)
    normalized = local + '@' + domain.lower()
    plausible = bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+", local))
    plausible = plausible and not (local.startswith('.') or local.endswith('.') or '..' in local)
    labels = domain.split('.')
    plausible = plausible and len(labels) >= 2 and all(
        bool(re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?', label)) for label in labels)
    return normalized, 'plausible' if plausible else 'invalid'


def normalize(path: Path, max_rows: int = 10000) -> dict:
    """Keep every nonblank record and provenance. Flag duplicates; never merge."""
    if not isinstance(max_rows, int) or isinstance(max_rows, bool) or max_rows < 1:
        raise ValueError('max_rows must be a positive integer.')
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f'Input exceeds the local helper limit of {MAX_BYTES} bytes.')
    text = path.read_text(encoding='utf-8-sig')
    reader = csv.DictReader(io.StringIO(text, newline=''), strict=True)
    if not reader.fieldnames:
        raise ValueError('CSV has no header.')
    headers = [field.strip().lower() for field in reader.fieldnames]
    if any(not field for field in headers) or len(headers) != len(set(headers)):
        raise ValueError('Headers must be nonempty and unique after trimming/lowercasing.')
    if 'company' not in headers:
        raise ValueError('CSV requires a company header. See examples/leads.csv.')
    reader.fieldnames = headers
    exact: dict[str, str] = {}
    folded: dict[str, str] = {}
    records = []
    for record_number, raw in enumerate(reader, start=2):
        if None in raw or any(value is None for value in raw.values()):
            raise ValueError(f'CSV record {record_number} has a different field count than the header.')
        if not any(value.strip() for value in raw.values()):
            continue
        if len(records) >= max_rows:
            raise ValueError(f'Input exceeds max_rows={max_rows}; no partial output is written.')
        contact_id = f'contact-{len(records)+1:06d}'
        email, syntax = _email(raw.get('email', ''))
        warnings = []
        duplicate = None
        possible = None
        if email and syntax == 'plausible':
            duplicate = exact.get(email)
            if not duplicate:
                possible = folded.get(email.casefold())
            exact.setdefault(email, contact_id)
            folded.setdefault(email.casefold(), contact_id)
        if not raw['company'].strip():
            warnings.append('missing_company')
        if duplicate:
            warnings.append('exact_email_duplicate_not_merged')
        if possible:
            warnings.append('case_variant_email_requires_review')
        if any(value.lstrip().startswith(('=', '+', '-', '@')) for value in raw.values()):
            warnings.append('formula_like_text_preserved_as_inert_json')
        if any(raw.get(field, '').strip() for field in POLICY_FIELDS):
            warnings.append('imported_policy_claim_not_treated_as_authorization')
        records.append({
            'contact_id': contact_id,
            'csv_record_number': record_number,
            'company': raw['company'].strip(),
            'domain': raw.get('domain', '').strip().lower() or None,
            'contact_name': raw.get('contact_name', '').strip() or None,
            'role': raw.get('role', '').strip() or None,
            'email': email or None,
            'email_syntax': syntax,
            'mailbox_verification': 'unverified',
            'identity_verification': 'unverified',
            'contact_permission': 'unreviewed',
            'suppression_status': 'unknown',
            'source_ref': raw.get('source_url', '').strip() or None,
            'source_kind': 'user_supplied',
            'collected_at_as_supplied': raw.get('collected_at', '').strip() or None,
            'duplicate_of': duplicate,
            'possible_duplicate_of': possible,
            'warnings': warnings,
            'raw': raw,
        })
    return {
        'schema_version': '0.1.2', 'execution': 'draft-only', 'source_file': path.name,
        'summary': {'records': len(records), 'exact_email_duplicates': sum(r['duplicate_of'] is not None for r in records),
                    'invalid_email_syntax': sum(r['email_syntax'] == 'invalid' for r in records)},
        'records': records,
        'limitations': ['Syntax plausibility is not mailbox existence, current employment, deliverability, or contact permission.',
                        'Raw input may contain personal data. Store it privately and do not commit it.',
                        'No duplicate was merged and no provider or remote system was called.'],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--max-rows', type=int, default=10000)
    args = parser.parse_args()
    try:
        data = normalize(args.input, args.max_rows)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as output:
            json.dump(data, output, ensure_ascii=False, indent=2, allow_nan=False)
            output.write('\n')
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print(f'Project Sales normalizer: {error}', file=sys.stderr)
        return 2
    print(json.dumps({'output': str(args.output), **data['summary'], 'remote_changes_made': False}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
