#!/usr/bin/env python3
"""Capture README images from the real introduction. Optional Playwright tooling."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def capture(executable: str) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError('Preview capture requires Playwright and Chromium; the skills do not.') from error
    source = ROOT / 'index.html'
    output = ROOT / 'images'
    output.mkdir(exist_ok=True)
    package = json.loads((ROOT / 'package-info.json').read_text(encoding='utf-8'))
    records = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=executable, headless=True,
                                             args=['--no-sandbox'])
        try:
            context = browser.new_context(viewport={'width': 1440, 'height': 1000},
                                          device_scale_factor=1, reduced_motion='reduce')
            page = context.new_page()
            page.set_content(source.read_text(encoding='utf-8'), wait_until='load')
            page.evaluate('document.fonts.ready')
            for locale, name in (('en', 'intro-en.png'), ('ko', 'intro-kr.png')):
                page.locator('#lang-' + locale).click()
                page.evaluate('window.scrollTo(0, 0)')
                bounds = page.locator('.surface-strip').bounding_box()
                if bounds is None:
                    raise RuntimeError('Missing environment strip; cannot determine the capture boundary.')
                height = math.ceil(bounds['y'] + bounds['height'])
                if height > 1600:
                    raise RuntimeError('Unexpectedly tall introduction. Inspect layout before capturing.')
                page.set_viewport_size({'width': 1440, 'height': max(1000, height)})
                destination = output / name
                page.screenshot(path=str(destination), clip={'x': 0, 'y': 0, 'width': 1440,
                                                           'height': height}, animations='disabled')
                records.append({'locale': locale, 'file': name, 'width': 1440, 'height': height,
                                'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()})
            report = {'version': package['version'], 'page': '../index.html',
                      'page_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                      'mode': 'Actual Chromium rendering via Playwright Page.set_content',
                      'browser': browser.version, 'theme': 'dark', 'highlight': '#76dba3',
                      'images': records, 'live_site_capture': False}
            context.close()
        finally:
            browser.close()
    (output / 'preview-info.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n',
                                            encoding='utf-8')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    try:
        print(json.dumps(capture(args.chromium), ensure_ascii=False, indent=2))
    except (OSError, RuntimeError) as error:
        parser.exit(2, f'Preview capture failed: {error}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
