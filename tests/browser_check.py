#!/usr/bin/env python3
"""Optional rendered checks. Requires Playwright and an installed Chromium.

Uses Page.set_content: browser rendering, interactions and Blob downloads are real;
HTTP/file navigation and persistent native storage are not validated by this runner.
No model, mailbox, remote site or other external service is contacted.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def run(executable: str, screenshots: Path | None = None) -> dict:
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    results=[]
    def check(name, function):
        try:
            function()
            results.append({'name':name,'status':'passed'})
        except Exception as error:
            results.append({'name':name,'status':'failed','detail':str(error)})
    def equal(actual, expected):
        if actual != expected:
            raise AssertionError(f'{actual!r} != {expected!r}')
    def yes(condition, message='Assertion failed'):
        if not condition:
            raise AssertionError(message)
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
        page=context.new_page()
        errors=[];requests=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('request',lambda request:requests.append(request.url))
        page.set_content(html,wait_until='load')
        config=page.locator('#site-data').text_content()
        data=json.loads(config)
        check('Default dark background',lambda:equal(page.evaluate('getComputedStyle(document.body).backgroundColor'),'rgb(16, 22, 19)'))
        check('Green accent token',lambda:equal(page.evaluate('getComputedStyle(document.documentElement).getPropertyValue("--accent").trim()'),'#76dba3'))
        check('Primary CTA has dark text on green',lambda:equal(page.locator('.hero .button.primary').evaluate('(e)=>getComputedStyle(e).color'),'rgb(12, 36, 23)'))
        check('English default without stored preference',lambda:equal(page.locator('html').get_attribute('lang'),'en'))
        for locale in ('en','ko'):
            page.locator('#lang-'+locale).click()
            check(f'{locale}: title and LITE match the source',lambda loc=locale:(
                equal(page.title(),data['meta'][loc]['title']),
                equal(page.locator('#lite-text').input_value(),data['lite'][loc]),
                equal(page.locator('#lang-'+loc).get_attribute('aria-pressed'),'true'),
                equal(page.locator('meta[name=description]').get_attribute('content'),data['meta'][loc]['description'])))
            for width in (320,390,768,1440):
                page.set_viewport_size({'width':width,'height':900})
                check(f'{locale}: no page overflow at {width}px',lambda w=width:yes(
                    page.evaluate('document.documentElement.scrollWidth')<=w,'Horizontal page overflow'))
                if screenshots and width in (390,1440):
                    screenshots.mkdir(parents=True,exist_ok=True)
                    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                    page.screenshot(path=str(screenshots/f'{width}-{locale}.png'),full_page=True)
            for key in ('discover','draft','reply'):
                page.locator(f'[data-scenario="{key}"]').click()
                check(f'{locale}: {key} example routing',lambda k=key,loc=locale:(
                    equal(page.locator('#example-result').text_content(),data['scenarios'][k][loc]['result']),
                    equal(page.locator('.route-skill').all_text_contents(),data['scenarios'][k]['skills'])))
            for key in ('web','app','cli'):
                page.locator('#tab-'+key).click()
                check(f'{locale}: {key} setup tab',lambda k=key,loc=locale:(
                    equal(page.locator('#setup-code').text_content(),data['setup'][k][loc]['code']),
                    equal(page.locator('#setup-guide').get_attribute('href'),data['setup'][k]['href']),
                    equal(page.locator('#tab-'+k).get_attribute('aria-selected'),'true')))
            def download(loc=locale):
                with page.expect_download(timeout=5000) as expected:
                    page.locator('#download-lite').click()
                item=expected.value
                equal(item.suggested_filename,'LITE-KR.md' if loc=='ko' else 'LITE.md')
                equal(item.failure(),None)
                with tempfile.TemporaryDirectory() as directory:
                    target=Path(directory)/item.suggested_filename
                    item.save_as(str(target))
                    equal(target.read_bytes(),data['lite'][loc].encode('utf-8'))
            check(f'{locale}: actual Blob download matches source bytes',download)
        page.set_viewport_size({'width':320,'height':844})
        page.evaluate('document.querySelectorAll("details").forEach(e=>e.open=true)')
        for key in ('web','app','cli'):
            page.locator('#tab-'+key).click()
            check(f'320px expanded details and {key} setup stay within viewport',lambda:yes(page.evaluate('document.documentElement.scrollWidth')<=320))
        page.evaluate('document.querySelectorAll("details").forEach(e=>e.open=false)')
        page.set_viewport_size({'width':1440,'height':1000})
        page.locator('#tab-web').focus()
        page.keyboard.press('ArrowRight')
        check('Keyboard tab navigation',lambda:(equal(page.locator('#tab-app').get_attribute('aria-selected'),'true'),
            equal(page.evaluate('document.activeElement.id'),'tab-app')))
        page.keyboard.press('End')
        check('Keyboard tab End navigation',lambda:equal(page.evaluate('document.activeElement.id'),'tab-cli'))
        first=page.locator('details.capability').first
        first.locator('summary').focus();page.keyboard.press('Enter')
        check('Native details opens with keyboard',lambda:yes(first.evaluate('(e)=>e.open')))
        first.locator('summary').click()
        check('Native details closes with pointer',lambda:yes(not first.evaluate('(e)=>e.open')))
        page.locator('#copy-lite').click()
        check('Copy fallback returns a truthful browser result',lambda:yes(
            page.locator('#lite-status').text_content() in (data['messages']['ko']['copied'],data['messages']['ko']['manual'])))
        # Explicitly test the blocked-clipboard path, not an actual permission grant.
        page.evaluate('''() => {
            Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});
            document.execCommand=()=>false;
        }''')
        page.locator('#copy-lite').click()
        check('Blocked copy exposes manual selection',lambda:(
            equal(page.locator('#lite-status').text_content(),data['messages']['ko']['manual']),
            equal(page.locator('#lite-text').evaluate('(e)=>e.selectionEnd-e.selectionStart'),len(data['lite']['ko']))))
        page.locator('#copy-setup').click()
        check('Blocked example copy selects full text',lambda:(
            equal(page.locator('#setup-status').text_content(),data['messages']['ko']['codeManual']),
            equal(page.evaluate('window.getSelection().toString()'),page.locator('#setup-code').text_content())))
        page.set_viewport_size({'width':1280,'height':1000})
        page.evaluate('document.documentElement.style.fontSize="32px"')
        check('200 percent root text has no page overflow',lambda:yes(page.evaluate('document.documentElement.scrollWidth')<=1280))
        page.emulate_media(reduced_motion='reduce')
        check('Reduced-motion scrolling',lambda:equal(page.evaluate('getComputedStyle(document.documentElement).scrollBehavior'),'auto'))
        check('Repository CTAs use the requested destination',lambda:yes(page.locator('a[href="'+data['repository']+'"]').count()>=3))
        page.emulate_media(media='print')
        check('Print uses a readable paper palette',lambda:equal(page.evaluate('getComputedStyle(document.body).backgroundColor'),'rgb(255, 255, 255)'))
        page.emulate_media(media='screen')
        check('No runtime asset requests',lambda:equal([url for url in requests if not url.startswith('blob:')],[]))
        check('No uncaught JavaScript errors',lambda:equal(errors,[]))
        # A restricted-storage browser must still support manual language changes.
        restricted=context.new_page()
        restricted.evaluate('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("Blocked","SecurityError")}})')
        restricted.set_content(html)
        restricted.locator('#lang-ko').click()
        check('Language switch when storage is blocked',lambda:equal(restricted.locator('html').get_attribute('lang'),'ko'))
        restricted.close()
        nojs=browser.new_context(java_script_enabled=False)
        fallback=nojs.new_page();fallback.set_content(html)
        check('No-JavaScript English fallback',lambda:(
            yes(fallback.locator('h1').is_visible()),
            yes(not fallback.locator('#copy-lite').is_visible()),
            equal(fallback.locator('#lite-text').input_value(),data['lite']['en'])))
        nojs.close();context.close();browser.close()
    return {'mode':'Chromium DOM rendering via Playwright Page.set_content','version':'0.1.2',
            'passed':sum(r['status']=='passed' for r in results),
            'failed':sum(r['status']=='failed' for r in results), 'checks':results,
            'not_verified':['HTTP/file URL navigation','Clipboard read-back to the operating system','Native localStorage persistence and URL deep-linking','Other browser engines and operating systems','Live repository navigation or deployment'],
            'note':'Blob downloads are actual completed browser downloads, compared byte-for-byte. Forced clipboard failure is a simulated error path. No test invokes a model or external account.'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium',default='/usr/bin/chromium')
    parser.add_argument('--output',type=Path,default=ROOT/'tests/results/browser-check.json')
    parser.add_argument('--screenshots',type=Path)
    args=parser.parse_args()
    report=run(args.chromium,args.screenshots)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return int(report['failed']>0)

if __name__=='__main__':
    raise SystemExit(main())
