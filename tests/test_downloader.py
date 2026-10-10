import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('dl', ROOT / 'scripts/incy_download.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class DownloaderTest(unittest.TestCase):
    def test_resolve_windows_and_deb(self):
        manifest = m.load_manifest(str(ROOT / 'RELEASE.json'))
        _, exe = m.resolve(manifest, 'windows-x64')
        self.assertTrue(exe.endswith('incy-windows-setup.exe'))
        _, deb = m.resolve(manifest, 'linux-x64-deb')
        self.assertTrue(deb.endswith('incy-linux-x64.deb'))

    def test_all_targets_resolve(self):
        manifest = m.load_manifest(str(ROOT / 'RELEASE.json'))
        for target in m.TARGETS:
            _, url = m.resolve(manifest, target)
            self.assertTrue(url.startswith('https://'), target)

    def test_readme_download_buttons(self):
        for name in ('README.md', 'README.fa.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            self.assertIn('for-the-badge', text, name)
            # Primary buttons must be OUR builds, not the upstream app.
            self.assertIn('github.com/reza-em/incy-plus/releases/download/', text, name)
            self.assertIn('incy-download.exe', text, name)
            self.assertIn('incy-downloader_', text, name)
            self.assertIn('incy-configs-', text, name)


if __name__ == '__main__':
    unittest.main()
