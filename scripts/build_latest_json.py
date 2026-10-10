"""Build stable per-platform `latest-*.json` pointers from RELEASE.json.

GitHub offers only one global /releases/latest, so Android clients must NOT
follow it (a desktop release would shadow Android). These small files live at
stable raw URLs and always contain the current platform download:

  https://raw.githubusercontent.com/INCY-DEV/incy-platforms/main/latest-android.json
  https://raw.githubusercontent.com/INCY-DEV/incy-platforms/main/latest-desktop.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def build(manifest_path=ROOT / 'RELEASE.json', out_dir=ROOT):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    android = manifest['android']
    desktop = manifest['desktop']
    latest_android = {
        'platform': 'android',
        'version': android['version'],
        'tag': android.get('tag', f"android-v{android['version']}"),
        'download': android['download'],
        'name': android.get('name', f"INCY Android {android['version']}"),
    }
    if 'sha256' in android:
        latest_android['sha256'] = android['sha256']
    latest_desktop = {
        'platform': 'desktop',
        'version': desktop['version'],
        'tag': desktop.get('tag', f"desktop-v{desktop['version']}"),
        'name': desktop.get('name', f"INCY Desktop {desktop['version']}"),
        'windows': desktop['windows'],
        'macos': desktop['macos'],
        'linux': desktop['linux'],
    }
    if 'sha256' in desktop:
        latest_desktop['sha256'] = desktop['sha256']
    out_dir = Path(out_dir)
    (out_dir / 'latest-android.json').write_text(json.dumps(latest_android, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out_dir / 'latest-desktop.json').write_text(json.dumps(latest_desktop, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return latest_android, latest_desktop


if __name__ == '__main__':
    build()
    print('latest-android.json + latest-desktop.json written')
