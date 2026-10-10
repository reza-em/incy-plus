import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('manifest', ROOT / 'scripts/update_manifest.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def collect_manifest_urls(manifest):
    urls = set()
    a = manifest.get('android', {})
    if 'download' in a:
        urls.add(a['download'])
    d = manifest.get('desktop', {})
    for os_name in ('windows', 'macos', 'linux'):
        for url in d.get(os_name, {}).values():
            urls.add(url)
    return urls


class ReadmeLinksTest(unittest.TestCase):
    def test_every_manifest_url_exists_in_readme(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for url in collect_manifest_urls(manifest):
            self.assertIn(url, readme, f"manifest URL missing from README: {url}")

    def test_readme_uses_versioned_links_not_latest(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertNotIn('/releases/latest/download/', readme)

    def test_readme_versions_match_manifest(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn(manifest['android']['version'], readme)
        self.assertIn(manifest['desktop']['version'], readme)

    def test_desktop_asset_coverage(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        expected = {n for group in m.DESKTOP.values() for n in group.values()}
        found = set()
        d = manifest['desktop']
        for os_name in ('windows', 'macos', 'linux'):
            for url in d.get(os_name, {}).values():
                found.add(url.rsplit('/', 1)[-1])
        self.assertTrue(expected <= found, f"missing {sorted(expected - found)}")


if __name__ == '__main__':
    unittest.main()
