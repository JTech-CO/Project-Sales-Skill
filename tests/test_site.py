"""Offline source checks for the self-contained introduction and release metadata."""
from __future__ import annotations
import json
import hashlib
import struct
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.handle_text = None
        self.blocks = {}
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if tag in ('script', 'textarea') and attrs.get('id'):
            self.handle_text = attrs['id']
            self.blocks[self.handle_text] = ''
    def handle_data(self, text):
        if self.handle_text:
            self.blocks[self.handle_text] += text
    def handle_endtag(self, tag):
        if tag in ('script', 'textarea'):
            self.handle_text = None

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT/'index.html').read_text(encoding='utf-8')
        cls.page = PageParser(cls.html)
        cls.data = json.loads(cls.page.blocks['site-data'])
        cls.package = json.loads((ROOT/'package-info.json').read_text())

    def test_embedded_lite_matches_source_bytes(self):
        for locale, filename in (('en','LITE.md'), ('ko','LITE-KR.md')):
            self.assertEqual(self.data['lite'][locale].encode('utf-8'), (ROOT/filename).read_bytes())

    def test_no_script_initial_lite_is_complete(self):
        self.assertEqual(self.page.blocks['lite-text'], self.data['lite']['en'])

    def test_single_main_heading_and_landmark(self):
        self.assertEqual(sum(tag=='h1' for tag, _ in self.page.nodes), 1)
        self.assertEqual(sum(tag=='main' for tag, _ in self.page.nodes), 1)

    def test_unique_ids_and_real_fragment_targets(self):
        ids=[a['id'] for _, a in self.page.nodes if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        for tag, a in self.page.nodes:
            if tag=='a' and a.get('href','').startswith('#'):
                self.assertIn(a['href'][1:], ids)

    def test_no_external_runtime_assets(self):
        for tag,a in self.page.nodes:
            if tag in ('script','img','iframe','audio','video','source'):
                self.assertFalse(a.get('src'))
            if tag=='link':
                self.assertNotEqual(a.get('rel'), 'stylesheet')
                if a.get('rel') == 'canonical':
                    self.assertEqual(a.get('href'), self.package['website'])
                else:
                    self.assertEqual(a.get('rel'), 'icon')
                    self.assertTrue(a.get('href','').startswith('data:'))
        self.assertNotRegex(self.html, r'@import\b|@font-face\b|\bfetch\s*\(|\bXMLHttpRequest\b')

    def test_repository_ctas_and_guides_match_package(self):
        repo=self.package['repository']
        self.assertEqual(self.data['repository'], repo)
        links=[a.get('href','') for tag,a in self.page.nodes if tag=='a']
        self.assertGreaterEqual(links.count(repo), 3)
        for href in links + [item['href'] for item in self.data['setup'].values()]:
            for branchpath in ('blob/main/','tree/main/'):
                if href.startswith(repo + branchpath):
                    self.assertTrue((ROOT/href[len(repo + branchpath):]).exists(), href)

    def test_external_new_tabs_have_safe_rel(self):
        for tag,a in self.page.nodes:
            if tag=='a' and a.get('target')=='_blank':
                self.assertTrue({'noopener','noreferrer'} <= set(a.get('rel','').split()))

    def test_all_scenarios_have_both_languages(self):
        self.assertEqual(set(self.data['scenarios']), {'discover','draft','reply'})
        for sample in self.data['scenarios'].values():
            for locale in ('en','ko'):
                for key in ('request','input','result','detail','note'):
                    self.assertTrue(sample[locale][key])

    def test_all_setup_environments_have_both_languages(self):
        self.assertEqual(set(self.data['setup']), {'web','app','cli'})
        for item in self.data['setup'].values():
            for locale in ('en','ko'):
                for key in ('title','body','code','note','link'):
                    self.assertTrue(item[locale][key])

    def test_six_independent_capabilities(self):
        self.assertEqual(sum(tag=='details' and a.get('class')=='capability' for tag,a in self.page.nodes), 6)
        for key in self.package['specialists']:
            self.assertTrue((ROOT/f'optional-skills/project-sales-{key}/SKILL.md').exists())

    def test_version_sync(self):
        version=self.package['version']
        self.assertEqual(version, '0.1.2')
        self.assertEqual(self.data['version'], version)
        for path in [ROOT/'SKILL.md', *ROOT.glob('optional-skills/*/SKILL.md')]:
            self.assertIn(f'version: "{version}"', path.read_text())
        for path in ROOT.glob('assets/*.json'):
            self.assertEqual(json.loads(path.read_text())['schema_version'], version)
        self.assertIn(version,(ROOT/'adapters/app/project-sales.mjs').read_text())

    def test_license_in_every_installable_skill(self):
        license_text=(ROOT/'LICENSE').read_bytes()
        self.assertTrue(license_text.startswith(b'MIT License'))
        self.assertEqual(self.package['license'],'MIT')
        for path in [ROOT/'SKILL.md', *ROOT.glob('optional-skills/*/SKILL.md')]:
            self.assertIn('license: MIT', path.read_text())
            self.assertEqual((path.parent/'LICENSE').read_bytes(),license_text)

    def test_minimum_accessibility_source_hooks(self):
        for marker in ('prefers-reduced-motion',':focus-visible','skip-link','aria-live="polite"','role="tablist"','role="tabpanel"'):
            self.assertIn(marker,self.html)
        labels={a.get('for') for tag,a in self.page.nodes if tag=='label'}
        self.assertIn('lite-text',labels)

    def test_default_dark_theme_and_green_highlight(self):
        meta = {a.get('name'): a.get('content') for tag, a in self.page.nodes if tag == 'meta'}
        self.assertEqual(meta['color-scheme'], 'dark')
        self.assertEqual(meta['theme-color'], '#101613')
        tokens = re.search(r':root\{([^}]+)\}', self.html).group(1)
        self.assertIn('color-scheme:dark', tokens)
        self.assertIn('--accent:#76dba3', tokens)
        self.assertIn('color:var(--button-ink)', self.html)

    def test_published_website_metadata(self):
        site = 'https://jtech-co.github.io/Project-Sales-Skill/'
        self.assertEqual(self.package['website'], site)
        canonical = [a['href'] for tag,a in self.page.nodes if tag == 'link' and a.get('rel') == 'canonical']
        self.assertEqual(canonical, [site])
        self.assertIn(('meta', {'property': 'og:url', 'content': site}), self.page.nodes)

    def test_readme_visuals_and_live_links(self):
        for name, image in (('README.md', 'intro-en.png'), ('README-KR.md', 'intro-kr.png')):
            text = (ROOT/name).read_text(encoding='utf-8')
            self.assertIn(self.package['website'], text)
            self.assertIn(f'(images/{image})', text)
            self.assertIn('> [!NOTE]', text)
            self.assertLess(len(text), 4200, 'Keep the README concise; details belong in guides.')
            for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
                self.assertFalse(target.startswith('http'), 'Own the screenshot and badge files locally.')
                self.assertTrue((ROOT/target).is_file(), target)
            for badge in ('version.svg', 'license.svg', 'languages.svg'):
                self.assertIn(f'images/badges/{badge}', text)

    def test_badges_are_well_formed_and_versioned(self):
        for path in (ROOT/'images/badges').glob('*.svg'):
            svg = ET.fromstring(path.read_text(encoding='utf-8'))
            self.assertEqual(svg.get('role'), 'img')
            self.assertTrue(svg.get('aria-label'))
            self.assertIsNotNone(svg.find('{http://www.w3.org/2000/svg}title'))
        version = (ROOT/'images/badges/version.svg').read_text(encoding='utf-8')
        self.assertIn(self.package['version'], version)

    def test_actual_preview_files_match_the_page_and_manifest(self):
        data = json.loads((ROOT/'images/preview-info.json').read_text(encoding='utf-8'))
        self.assertEqual(data['page_sha256'], hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest())
        self.assertEqual(data['version'], self.package['version'])
        self.assertEqual({i['locale'] for i in data['images']}, {'en', 'ko'})
        for image in data['images']:
            raw = (ROOT/'images'/image['file']).read_bytes()
            self.assertEqual(raw[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II', raw[16:24]), (image['width'], image['height']))
            self.assertEqual(hashlib.sha256(raw).hexdigest(), image['sha256'])

    def test_visuals_are_not_in_installable_skill_archives(self):
        import zipfile
        for path in (ROOT/'dist').glob('*.zip'):
            with zipfile.ZipFile(path) as archive:
                self.assertTrue(archive.namelist())
                self.assertFalse(any('/images/' in name for name in archive.namelist()))
                self.assertTrue(all(not name.endswith('.png') for name in archive.namelist()))

    def test_text_palette_contrast(self):
        # Resolve actual tokens rather than testing unrelated hard-coded colors.
        tokens = dict(re.findall(r'--([a-z-]+):#([0-9a-f]{6})(?:;|})',
                                 re.search(r':root\{([^}]+)\}', self.html).group(0)))
        def luminance(color):
            rgb = [int(color[i:i+2],16)/255 for i in (0,2,4)]
            linear = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in rgb]
            return sum(a*b for a,b in zip(linear,(.2126,.7152,.0722)))
        pairs = [('ink','paper'),('muted','paper'),('accent','paper'),
                 ('ink','surface'),('muted','surface'),('ink','soft'),('muted','soft'),
                 ('route-ink','soft'),('button-ink','accent'),('button-ink','accent-hover')]
        for foreground, background in pairs:
            a,b = sorted([luminance(tokens[foreground]), luminance(tokens[background])])
            self.assertGreaterEqual((b+.05)/(a+.05),4.5,(foreground,background))
        a,b = sorted([luminance(tokens['control-line']), luminance(tokens['paper'])])
        self.assertGreaterEqual((b+.05)/(a+.05), 3.0, 'Outline control boundary contrast')

if __name__=='__main__':
    unittest.main()
