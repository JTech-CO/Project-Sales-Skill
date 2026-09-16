#!/usr/bin/env python3
"""Build self-contained core and specialist ZIPs locally, without overwriting."""
from __future__ import annotations
import argparse
import json
import tempfile
import zipfile
from pathlib import Path
from install import ROOT, SPECIALISTS, install


def build(output_dir: Path) -> list[dict]:
    output_dir = output_dir.expanduser().absolute()
    names = ('project-sales-core.zip','project-sales-specialists.zip')
    for name in names:
        if (output_dir/name).exists():
            raise FileExistsError(f'Refusing to overwrite: {output_dir/name}')
    results = []
    with tempfile.TemporaryDirectory(prefix='project-sales-dist-') as temp:
        stage = Path(temp)
        core = stage/'core'
        specialists = stage/'specialists'
        install(core)
        install(specialists,list(SPECIALISTS))
        output_dir.mkdir(parents=True,exist_ok=True)
        for name,source in zip(names,(core,specialists)):
            output = output_dir/name
            files = sorted(p for p in source.rglob('*') if p.is_file())
            with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
                for path in files:
                    info = zipfile.ZipInfo(path.relative_to(source).as_posix(),date_time=(2026,9,17,0,0,0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info,path.read_bytes())
            results.append({'path':str(output),'files':len(files),'bytes':output.stat().st_size})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'dist')
    args=parser.parse_args()
    try:
        results=build(args.output_dir)
    except (OSError,ValueError) as error:
        parser.exit(2,f'Project Sales distribution builder: {error}\n')
    print(json.dumps({'archives':results,'remote_changes_made':False},indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
