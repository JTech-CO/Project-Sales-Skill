#!/usr/bin/env python3
"""Optional developer check for JSON Schema records and YAML metadata."""
from __future__ import annotations
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    try:
        import yaml
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        print('Optional check needs jsonschema and PyYAML; core utilities do not.', file=sys.stderr)
        return 2
    validators = {}
    examples = {}
    for name in ('action-proposal','evidence','handoff'):
        schema = json.loads((ROOT/f'schemas/{name}.schema.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())
        examples[name] = json.loads((ROOT/f'assets/{name}.json').read_text(encoding='utf-8'))
        validators[name].validate(examples[name])
    negatives = []
    bad = copy.deepcopy(examples['action-proposal']); bad['execution_authorized'] = True
    negatives.append(('action-proposal',bad))
    bad = copy.deepcopy(examples['action-proposal']); bad['status'] = 'approved'
    negatives.append(('action-proposal',bad))
    bad = copy.deepcopy(examples['action-proposal']); bad['host_approved'] = True
    negatives.append(('action-proposal',bad))
    bad = copy.deepcopy(examples['handoff']); bad['booking'].update(state='confirmed',starts_at='2026-09-20T14:00:00+09:00',timezone='Asia/Seoul',evidence_refs=[])
    negatives.append(('handoff',bad))
    bad = copy.deepcopy(examples['handoff']); bad['booking'].update(state='confirmed',starts_at=None,timezone='Asia/Seoul',evidence_refs=['fixture:booking'])
    negatives.append(('handoff',bad))
    bad = copy.deepcopy(examples['handoff']); bad['booking'].update(state='held',starts_at='2026-09-15T14:00:00+09:00',timezone='Asia/Seoul',evidence_refs=[])
    negatives.append(('handoff',bad))
    bad = copy.deepcopy(examples['evidence']); bad['observed_at'] = 'yesterday'
    negatives.append(('evidence',bad))
    for name, record in negatives:
        if validators[name].is_valid(record):
            raise AssertionError(f'Invalid {name} example unexpectedly accepted.')
    skill_count = 0
    meta_count = 0
    for path in [ROOT/'SKILL.md', *sorted((ROOT/'optional-skills').glob('*/SKILL.md'))]:
        front = path.read_text(encoding='utf-8').split('---',2)[1]
        data = yaml.safe_load(front)
        assert isinstance(data,dict)
        assert data['name'] == path.parent.name
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',data['name'])
        assert isinstance(data['description'],str) and 0 < len(data['description']) <= 1024
        assert all(isinstance(k,str) and isinstance(v,str) for k,v in data['metadata'].items())
        skill_count += 1
        metadata = yaml.safe_load((path.parent/'agents/openai.yaml').read_text(encoding='utf-8'))
        assert isinstance(metadata['interface']['display_name'],str)
        assert isinstance(metadata['interface']['default_prompt'],str)
        assert isinstance(metadata['policy']['allow_implicit_invocation'],bool)
        meta_count += 1
    print(json.dumps({'ok':True,'schemas_compiled':len(validators),'valid_examples':len(examples),
                      'invalid_examples_rejected':len(negatives),'skill_frontmatter':skill_count,
                      'openai_ui_metadata':meta_count,'authorization_or_truth_verified':False},indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
