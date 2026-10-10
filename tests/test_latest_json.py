import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class LatestJsonTest(unittest.TestCase):
    def test_latest_files_match_manifest(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        android = json.loads((ROOT / 'latest-android.json').read_text(encoding='utf-8'))
        desktop = json.loads((ROOT / 'latest-desktop.json').read_text(encoding='utf-8'))
        self.assertEqual(android['version'], manifest['android']['version'])
        self.assertEqual(android['download'], manifest['android']['download'])
        self.assertEqual(desktop['version'], manifest['desktop']['version'])
        self.assertEqual(desktop['windows'], manifest['desktop']['windows'])
        self.assertEqual(desktop['macos'], manifest['desktop']['macos'])
        self.assertEqual(desktop['linux'], manifest['desktop']['linux'])

    def test_worker_routes_cover_desktop_assets(self):
        worker = (ROOT / 'worker' / 'worker.js').read_text(encoding='utf-8')
        for route in ('/android', '/desktop/windows', '/desktop/macos-arm',
                      '/desktop/linux-x64', '/health', '/android.json', '/desktop.json'):
            self.assertIn(route, worker)


if __name__ == '__main__':
    unittest.main()
