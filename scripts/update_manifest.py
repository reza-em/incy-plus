"""Update one platform from a published GitHub release; never use global /latest."""
import argparse
import json
import re
from pathlib import Path

REPO = "INCY-DEV/incy-platforms"
DESKTOP = {
    "windows": {"x64": "incy-windows-setup.exe", "arm64": "incy-windows-setup.exe",
                "x64_portable": "incy-windows-portable.zip", "arm64_portable": "incy-windows-portable.zip"},
    "macos": {"arm64": "incy-macos-arm64.dmg", "intel": "incy-macos-intel.dmg"},
    "linux": {"x64_deb": "incy-linux-x64.deb", "arm64_deb": "incy-linux-arm64.deb",
              "x64_rpm": "incy-linux-x64.rpm", "arm64_rpm": "incy-linux-arm64.rpm",
              "x64_arch": "incy-linux-x64.pkg.tar.zst", "x64_portable": "incy-linux-x64-portable.zip",
              "arm64_portable": "incy-linux-arm64-portable.zip"},
}

def parse_sha256sums(text):
    """Parse `sha256sum` output (SHA256SUMS asset) into {filename: hex}."""
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        digest, name = parts[0], parts[-1].lstrip('*')
        # basename only: SHA256SUMS may contain paths
        name = name.split('/')[-1]
        if re.fullmatch(r'[0-9a-fA-F]{64}', digest) and name:
            out[name] = digest.lower()
    return out


def update(manifest, release, checksums=None):
    match = re.fullmatch(r"(android|desktop)-v(\d+\.\d+\.\d+)", release["tag_name"])
    if not match or release.get("draft") or release.get("prerelease"):
        raise ValueError("Expected a published stable android-vX.Y.Z or desktop-vX.Y.Z release")
    platform, version = match.groups()
    old = manifest.get(platform, {}).get("version", "0.0.0")
    if tuple(map(int, version.split('.'))) < tuple(map(int, old.split('.'))):
        return {}  # Publishing an older version must not roll back clients.
    names = {a["name"] for a in release["assets"] if a.get("size", 0) > 0}
    required = {"Incy.apk"} if platform == "android" else {n for group in DESKTOP.values() for n in group.values()}
    if not required <= names:
        raise ValueError(f"Release assets not ready: missing {sorted(required - names)}")
    urls = {n: f"https://github.com/{REPO}/releases/download/{release['tag_name']}/{n}" for n in required}
    entry = dict(manifest.get(platform, {}))
    entry.update(version=version, tag=release['tag_name'],
                 name=f"INCY {'Android' if platform == 'android' else 'Desktop'} {version}")
    if platform == 'android':
        entry['download'] = urls['Incy.apk']
    else:
        for os_name, assets in DESKTOP.items():
            entry[os_name] = {key: urls[name] for key, name in assets.items()}
    # Optional integrity data: never delete old hashes when checksums are absent
    # (multi-release sync in release-manifest.yml has no file contents).
    if checksums is not None:
        missing = sorted(required - set(checksums))
        if missing:
            raise ValueError(f"SHA256SUMS missing entries for {missing}")
        merged = dict(entry.get('sha256', {}))
        for name in required:
            merged[name] = checksums[name]
        entry['sha256'] = merged
    manifest[platform] = entry
    return urls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('release', type=Path)
    parser.add_argument('--sha256sums', type=Path, required=False, default=None,
                        help='Optional path to SHA256SUMS for a single-release update')
    args = parser.parse_args()
    checksums = parse_sha256sums(args.sha256sums.read_text(encoding='utf-8')) if args.sha256sums else None
    path = Path('RELEASE.json')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    payload = json.loads(args.release.read_text(encoding='utf-8'))
    releases = payload if isinstance(payload, list) else [payload]
    # Reconcile both channels: GitHub concurrency can replace pending runs.
    # A later event must also include a previously queued platform update.
    newest = {}
    for release in releases:
        match = re.fullmatch(r"(android|desktop)-v(\d+\.\d+\.\d+)", release.get("tag_name", ""))
        if not match or release.get("draft") or release.get("prerelease"):
            continue
        platform, version = match.groups()
        key = tuple(map(int, version.split('.')))
        if platform not in newest or key > newest[platform][0]:
            newest[platform] = (key, release)
    if not newest:
        raise ValueError('No published stable platform release found')
    urls = {}
    for _, release in newest.values():
        # Single-release runs (publish-android.yml) can pass --sha256sums.
        # Multi-release sync keeps existing hashes (no file contents available).
        if checksums is not None and len(newest) == 1:
            urls.update(update(manifest, release, checksums))
        else:
            urls.update(update(manifest, release))
    if not urls:
        print('Older release: manifest unchanged')
        return
    readme = Path('README.md')
    text = readme.read_text(encoding='utf-8')
    for name, url in urls.items():
        pattern = rf"https://github\.com/{re.escape(REPO)}/releases/(?:latest/download|download/[^/\s)]+)/{re.escape(name)}(?=[\s)\"<>]|$)"
        text = re.sub(pattern, lambda _: url, text)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    readme.write_text(text, encoding='utf-8')
    try:
        from build_latest_json import build as build_latest
    except ImportError:
        try:
            from scripts.build_latest_json import build as build_latest
        except ImportError:
            build_latest = None
    if build_latest is not None:
        build_latest(path, path.parent)

if __name__ == '__main__':
    main()
