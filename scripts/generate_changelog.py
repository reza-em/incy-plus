"""Ensure CHANGELOG.md has entries for the current RELEASE.json versions.

Idempotent: re-running never duplicates. Workflows call this after every
manifest update; humans can run `python scripts/generate_changelog.py`.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parents[1]


def ensure_entry(lines, version, tag, download_note):
    header = f"## {version}"
    if any(l.strip() == header for l in lines):
        return lines
    today = date.today().isoformat()
    block = [header + f" - {today}\n", "\n", f"- Tag: `{tag}`\n", f"- {download_note}\n", "\n"]
    # Insert after the title block (first `# ` + blank + intro).
    idx = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            idx = i
            break
        idx = i + 1
    return lines[:idx] + block + lines[idx:]


def main():
    manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
    path = ROOT / 'CHANGELOG.md'
    if path.exists():
        lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    else:
        lines = ["# Changelog\n", "\n", "All notable platform releases.\n", "\n"]
    a, d, i = manifest['android'], manifest['desktop'], manifest['ios']
    lines = ensure_entry(lines, f"Android v{a['version']}", a.get('tag', f"android-v{a['version']}"),
                         f"[Incy.apk]({a['download']}) + SHA256SUMS")
    lines = ensure_entry(lines, f"Desktop v{d['version']}", d.get('tag', f"desktop-v{d['version']}"),
                         "Windows setup/portable, macOS arm64/intel, Linux deb/rpm/arch/portable")
    ios_header = f"## iOS {i['version']} ({i['build']})"
    if not any(l.strip() == ios_header for l in lines):
        today = date.today().isoformat()
        block = [ios_header + f" - {today}\n", "\n", f"- App Store: {i['AppStore']}\n", "\n"]
        idx = next((n for n, l in enumerate(lines) if l.startswith('## ')), len(lines))
        lines = lines[:idx] + block + lines[idx:]
    path.write_text(''.join(lines), encoding='utf-8')
    print('CHANGELOG.md synced')


if __name__ == '__main__':
    main()
