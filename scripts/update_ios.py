"""Update the iOS section of RELEASE.json (App Store releases are external)."""
import argparse
import json
import re
from pathlib import Path

VERSION_RE = re.compile(r'^\d+\.\d+\.\d+$')
BUILD_RE = re.compile(r'^[0-9]+$')


def update_ios(manifest, version, build, appstore=None):
    if not VERSION_RE.fullmatch(version):
        raise ValueError(f"Bad iOS version: {version!r} (expected X.Y.Z)")
    if not BUILD_RE.fullmatch(build):
        raise ValueError(f"Bad iOS build: {build!r} (expected digits)")
    old = manifest.get('ios', {})
    old_key = tuple(map(int, old.get('version', '0.0.0').split('.')))
    new_key = tuple(map(int, version.split('.')))
    if new_key < old_key or (new_key == old_key and str(old.get('build', '0')) >= str(build)):
        return False  # Never roll back App Store clients.
    entry = dict(old)
    entry.update(version=version, build=str(build), name=f"INCY {version}")
    if appstore:
        if not appstore.startswith('https://apps.apple.com/'):
            raise ValueError(f"Bad AppStore URL: {appstore!r}")
        entry['AppStore'] = appstore
    elif 'AppStore' not in entry:
        raise ValueError("AppStore URL is required for the first iOS entry")
    manifest['ios'] = entry
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', required=True)
    parser.add_argument('--build', required=True)
    parser.add_argument('--appstore', required=False, default=None)
    parser.add_argument('--manifest', type=Path, default=Path('RELEASE.json'))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    changed = update_ios(manifest, args.version, args.build, args.appstore)
    if not changed:
        print('Older iOS release: manifest unchanged')
        return
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"iOS {args.version} ({args.build}) written")


if __name__ == '__main__':
    main()
