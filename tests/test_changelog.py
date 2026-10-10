import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class ChangelogTest(unittest.TestCase):
    def test_changelog_covers_current_versions(self):
        manifest = json.loads((ROOT / 'RELEASE.json').read_text(encoding='utf-8'))
        log = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        self.assertIn(f"Android v{manifest['android']['version']}", log)
        self.assertIn(f"Desktop v{manifest['desktop']['version']}", log)
        self.assertIn(manifest['ios']['version'], log)
        self.assertIn(manifest['ios']['build'], log)


if __name__ == '__main__':
    unittest.main()
