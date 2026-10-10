"""incy-download: fetch INCY installers from the versioned manifest.

Stdlib only (so the .exe/.deb builds stay small). Usage:

  python scripts/incy_download.py list [--manifest URL-or-path]
  python scripts/incy_download.py get windows-x64 --out incy-setup.exe
  python scripts/incy_download.py get linux-x64-deb --out incy.deb
  python scripts/incy_download.py get android --out Incy.apk

Targets: android, windows-x64, windows-portable, macos-arm64, macos-intel,
         linux-x64-deb, linux-arm64-deb, linux-x64-rpm, linux-x64-arch,
         linux-x64-portable, linux-arm64-portable

SHA256 is verified automatically when the manifest carries it.
Default manifest is the stable raw file (no /latest ambiguity).
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

DEFAULT_MANIFEST = (
    'https://raw.githubusercontent.com/INCY-DEV/incy-platforms/main/RELEASE.json'
)

TARGETS = {
    'android': ('android', ['download']),
    'windows-x64': ('desktop', ['windows', 'x64']),
    'windows-portable': ('desktop', ['windows', 'x64_portable']),
    'macos-arm64': ('desktop', ['macos', 'arm64']),
    'macos-intel': ('desktop', ['macos', 'intel']),
    'linux-x64-deb': ('desktop', ['linux', 'x64_deb']),
    'linux-arm64-deb': ('desktop', ['linux', 'arm64_deb']),
    'linux-x64-rpm': ('desktop', ['linux', 'x64_rpm']),
    'linux-x64-arch': ('desktop', ['linux', 'x64_arch']),
    'linux-x64-portable': ('desktop', ['linux', 'x64_portable']),
    'linux-arm64-portable': ('desktop', ['linux', 'arm64_portable']),
}


def load_manifest(src):
    if src.startswith(('http://', 'https://')):
        with urllib.request.urlopen(src) as r:
            return json.loads(r.read().decode('utf-8'))
    return json.loads(Path(src).read_text(encoding='utf-8'))


def resolve(manifest, target):
    platform, path = TARGETS[target]
    node = manifest[platform]
    for key in path:
        node = node[key]
    return platform, node


def sha256_of(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def download(url, out):
    out = Path(out)
    req = urllib.request.Request(url, headers={'User-Agent': 'incy-download/1.0'})
    total = 0
    with urllib.request.urlopen(req) as r, open(out, 'wb') as f:
        size = r.headers.get('Content-Length')
        size = int(size) if size else 0
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            total += len(chunk)
            if size:
                print(f"\r{total * 100 // size}%  {total // 1024 // 1024}MB", end='', flush=True)
    print(f"\nsaved: {out} ({total // 1024 // 1024}MB)")
    return out


def main(argv=None):
    p = argparse.ArgumentParser(prog='incy-download')
    p.add_argument('--manifest', default=DEFAULT_MANIFEST)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list')
    g = sub.add_parser('get')
    g.add_argument('target', choices=sorted(TARGETS))
    g.add_argument('--out', required=True)
    args = p.parse_args(argv)

    manifest = load_manifest(args.manifest)
    if args.cmd == 'list':
        print(f"android:  {manifest['android']['version']}")
        print(f"desktop:  {manifest['desktop']['version']}")
        print(f"ios:      {manifest['ios']['version']}")
        for t in sorted(TARGETS):
            _, url = resolve(manifest, t)
            print(f"  {t:22s} {url.rsplit('/', 1)[-1]}")
        return 0

    platform, url = resolve(manifest, args.target)
    print(f"{args.target} <- {url}")
    out = download(url, args.out)
    filename = url.rsplit('/', 1)[-1]
    expected = manifest.get(platform, {}).get('sha256', {}).get(filename)
    if expected:
        actual = sha256_of(out)
        if actual != expected:
            print(f"SHA256 MISMATCH! expected {expected}, got {actual}", file=sys.stderr)
            return 1
        print('SHA256 OK')
    else:
        print('note: manifest carries no SHA256 for this file, skipped verification')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
