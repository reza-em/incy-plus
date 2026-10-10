import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('manifest', Path(__file__).parents[1] / 'scripts/update_manifest.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ChecksumsTest(unittest.TestCase):
    def release(self, tag, names):
        return {'tag_name': tag, 'assets': [{'name': n, 'size': 1} for n in names]}

    def test_parse_sha256sums_standard_format(self):
        text = (
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  Incy.apk\n"
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa *incy-windows-setup.exe\n"
            "# comment\n"
            "\n"
        )
        out = m.parse_sha256sums(text)
        self.assertEqual(out['Incy.apk'], 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(len(out['Incy.apk']), 64)
        self.assertIn('incy-windows-setup.exe', out)

    def test_parse_lowercases_and_strips_paths(self):
        text = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855  ./dist/Incy.apk\n"
        out = m.parse_sha256sums(text)
        self.assertEqual(out['Incy.apk'], 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def test_update_with_checksums_adds_sha256(self):
        data = {}
        sums = {'Incy.apk': 'e' * 64}
        m.update(data, self.release('android-v3.7.0', ['Incy.apk']), sums)
        self.assertEqual(data['android']['sha256']['Incy.apk'], 'e' * 64)
        self.assertEqual(data['android']['tag'], 'android-v3.7.0')

    def test_update_without_checksums_preserves_old_hashes(self):
        data = {'android': {'version': '3.7.0', 'download': 'kept', 'tag': 'android-v3.7.0',
                            'sha256': {'Incy.apk': 'a' * 64}}}
        # Same version re-publish must not wipe the hash when SHA256SUMS is unavailable
        # (multi-release sync path in release-manifest.yml).
        m.update(data, self.release('android-v3.7.0', ['Incy.apk']))
        self.assertEqual(data['android']['sha256']['Incy.apk'], 'a' * 64)

    def test_update_with_incomplete_checksums_rejected(self):
        data = {}
        with self.assertRaises(ValueError):
            m.update(data, self.release('android-v3.7.0', ['Incy.apk']), {})
        self.assertEqual({}, data)


if __name__ == '__main__':
    unittest.main()
