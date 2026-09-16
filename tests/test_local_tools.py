"""Offline unit tests. All inputs are temporary or fictional."""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
installer = module('install')
normalizer = module('normalize_leads')


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project-sales-test-')
        self.addCleanup(self.temp.cleanup)
        self.dest = Path(self.temp.name)/'skills'

    def test_dry_run_writes_nothing(self):
        result = installer.install(self.dest, dry_run=True)
        self.assertFalse(self.dest.exists())
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]['dry_run'])

    def test_core_self_contained(self):
        installer.install(self.dest)
        root = self.dest/'project-sales'
        for path in ('SKILL.md','SKILL-KR.md','LITE-KR.md','references/TRIAGE.md','assets/action-proposal.json'):
            self.assertTrue((root/path).is_file(), path)
        self.assertFalse((root/'optional-skills').exists())
        self.assertFalse((root/'scripts').exists())

    def test_specialists_only(self):
        installer.install(self.dest, ['triage','handoff'])
        self.assertFalse((self.dest/'project-sales').exists())
        for name in ('triage','handoff'):
            self.assertTrue((self.dest/f'project-sales-{name}/references/FOCUS.md').is_file())

    def test_existing_target_not_overwritten(self):
        installer.install(self.dest)
        marker = self.dest/'project-sales/SKILL.md'
        marker.write_text('user content')
        with self.assertRaises(FileExistsError): installer.install(self.dest)
        self.assertEqual(marker.read_text(), 'user content')

    def test_batch_preflight_avoids_partial_install(self):
        installer.install(self.dest,['handoff'])
        with self.assertRaises(FileExistsError): installer.install(self.dest,['triage','handoff'])
        self.assertFalse((self.dest/'project-sales-triage').exists())

    def test_reject_unknown(self):
        with self.assertRaises(ValueError): installer.install(self.dest,['send'])

    def test_reject_duplicate(self):
        with self.assertRaises(ValueError): installer.install(self.dest,['triage','triage'])

    def test_reject_core_plus_specialist(self):
        with self.assertRaises(ValueError): installer.install(self.dest,['core','triage'])

    def test_reject_inside_source(self):
        with self.assertRaises(ValueError): installer.install(ROOT/'.agents/skills',dry_run=True)

    def test_reject_symlink_target(self):
        actual = Path(self.temp.name)/'real'
        actual.mkdir()
        self.dest.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(ValueError): installer.install(self.dest)


class NormalizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project-sales-csv-')
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'input.csv'

    def run_csv(self,text,**kwargs):
        self.path.write_text(text,encoding='utf-8')
        return normalizer.normalize(self.path,**kwargs)

    def test_example_preserves_four_records_and_duplicate(self):
        result = normalizer.normalize(ROOT/'examples/leads.csv')
        self.assertEqual(result['summary']['records'],4)
        self.assertEqual(result['summary']['exact_email_duplicates'],1)
        self.assertEqual(result['records'][1]['duplicate_of'],'contact-000001')

    def test_no_permission_or_verification_inferred(self):
        row = self.run_csv('company,email,approved,consent\nX,a@x.example,true,yes\n')['records'][0]
        self.assertEqual(row['contact_permission'],'unreviewed')
        self.assertEqual(row['mailbox_verification'],'unverified')
        self.assertEqual(row['suppression_status'],'unknown')
        self.assertIn('imported_policy_claim_not_treated_as_authorization',row['warnings'])

    def test_plus_tag_preserved(self):
        row=self.run_csv('company,email\nX,A+tag@X.EXAMPLE\n')['records'][0]
        self.assertEqual(row['email'],'A+tag@x.example')

    def test_case_variant_not_merged(self):
        result=self.run_csv('company,email\nX,A@x.example\nX,a@x.example\n')
        self.assertIsNone(result['records'][1]['duplicate_of'])
        self.assertEqual(result['records'][1]['possible_duplicate_of'],'contact-000001')

    def test_missing_addresses_do_not_deduplicate(self):
        result=self.run_csv('company,email\nX,\nX,\n')
        self.assertEqual(len(result['records']),2)
        self.assertTrue(all(r['duplicate_of'] is None for r in result['records']))

    def test_formula_is_inert_text(self):
        row=self.run_csv('company,email\n=1+1,a@x.example\n')['records'][0]
        self.assertEqual(row['raw']['company'],'=1+1')
        self.assertIn('formula_like_text_preserved_as_inert_json',row['warnings'])

    def test_bom_and_korean(self):
        row=self.run_csv('\ufeffcompany,email\n가상기업,a@x.example\n')['records'][0]
        self.assertEqual(row['company'],'가상기업')

    def test_missing_required_header(self):
        with self.assertRaises(ValueError): self.run_csv('email\na@x.example\n')

    def test_duplicate_header(self):
        with self.assertRaises(ValueError): self.run_csv('company, Company\nX,Y\n')

    def test_malformed_field_count(self):
        with self.assertRaises(ValueError): self.run_csv('company,email\nX,a@x.example,extra\n')

    def test_short_field_count(self):
        with self.assertRaises(ValueError): self.run_csv('company,email\nX\n')

    def test_limit_no_truncated_success(self):
        with self.assertRaises(ValueError): self.run_csv('company\nX\nY\n',max_rows=1)

    def test_invalid_limit(self):
        with self.assertRaises(ValueError): self.run_csv('company\nX\n',max_rows=0)

    def test_invalid_email_stays_visible(self):
        row=self.run_csv('company,email\nX,not-an-address\n')['records'][0]
        self.assertEqual(row['email'],'not-an-address')
        self.assertEqual(row['email_syntax'],'invalid')

    def test_empty_and_unknown_dates_remain_unknown(self):
        row=self.run_csv('company,email,collected_at\nX,,\n')['records'][0]
        self.assertIsNone(row['collected_at_as_supplied'])
        self.assertEqual(row['email_syntax'],'missing')

    def test_cli_refuses_output_overwrite(self):
        self.path.write_text('company\nX\n')
        output=Path(self.temp.name)/'existing.json'
        output.write_text('preserve')
        run=subprocess.run([sys.executable,str(ROOT/'scripts/normalize_leads.py'),str(self.path),str(output)],capture_output=True,text=True)
        self.assertEqual(run.returncode,2)
        self.assertEqual(output.read_text(),'preserve')

    def test_multiline_text_remains_one_record(self):
        result=self.run_csv('company,email\n"X\nY",a@x.example\n')
        self.assertEqual(result['summary']['records'],1)
        self.assertEqual(result['records'][0]['company'],'X\nY')


if __name__ == '__main__': unittest.main()
