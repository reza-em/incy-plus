import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SEMVER = re.compile(r'^\d+\.\d+\.\d+$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')

spec = importlib.util.spec_from_file_location('manifest', ROOT / 'scripts/update_manifest.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ReleaseSchemaTest(unittest.TestCase):
    def test_manifest_matches_schema(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        schema = json.loads((ROOT / 'RELEASE.schema.json').read_text(encoding='utf-8'))
        self.assertEqual({'android', 'desktop', 'ios'}, set(manifest))
        # android
        a = manifest['android']
        self.assertTrue(SEMVER.fullmatch(a['version']), a['version'])
        self.assertTrue(a['download'].startswith('https://github.com/INCY-DEV/incy-platforms/releases/download/android-v'))
        self.assertIn(a['version'], a['download'])
        self.assertTrue(a['download'].endswith('/Incy.apk'))
        if 'tag' in a:
            self.assertEqual(a['tag'], f"android-v{a['version']}")
        # desktop
        d = manifest['desktop']
        self.assertTrue(SEMVER.fullmatch(d['version']), d['version'])
        if 'tag' in d:
            self.assertEqual(d['tag'], f"desktop-v{d['version']}")
        for os_name, assets in m.DESKTOP.items():
            self.assertIn(os_name, d)
            for key, name in assets.items():
                url = d[os_name][key]
                self.assertTrue(url.startswith('https://'), url)
                self.assertIn(f"/desktop-v{d['version']}/{name}", url)
        # ios
        i = manifest['ios']
        self.assertTrue(SEMVER.fullmatch(i['version']))
        self.assertTrue(i['build'].isdigit())
        self.assertTrue(i['AppStore'].startswith('https://apps.apple.com/'))
        # sha256 values, when present, must be lowercase hex64
        for platform in ('android', 'desktop'):
            for name, digest in manifest.get(platform, {}).get('sha256', {}).items():
                self.assertTrue(HEX64.fullmatch(digest), f"{platform}:{name}")

    def test_no_global_latest_urls_in_manifest(self):
        text = (ROOT / 'RELEASE.json').read_text(encoding='utf-8')
        self.assertNotIn('/releases/latest/', text)


if __name__ == '__main__':
    unittest.main()
