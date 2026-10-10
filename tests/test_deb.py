import gzip
import importlib.util
import io
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location('deb', ROOT / 'scripts/build_deb.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def read_ar(path):
    data = Path(path).read_bytes()
    assert data[:8] == b'!<arch>\n', 'not an ar archive'
    members = {}
    pos = 8
    while pos < len(data):
        header = data[pos:pos + 60]
        name = header[:16].decode('ascii').strip().rstrip('/')
        size = int(header[48:58].decode('ascii').strip())
        assert data[pos + 58:pos + 60] == b'`\n'
        members[name] = data[pos + 60:pos + 60 + size]
        pos += 60 + size + (size % 2)
    return members


class DebTest(unittest.TestCase):
    def test_deb_structure_and_control(self):
        with tempfile.TemporaryDirectory() as tmp:
            deb = m.build('1.0.0', Path(tmp))
            members = read_ar(deb)
            self.assertEqual(members['debian-binary'], b'2.0\n')
            control = tarfile.open(fileobj=io.BytesIO(gzip.decompress(members['control.tar.gz'])))
            text = control.extractfile('control').read().decode()
            self.assertIn('Package: incy-downloader', text)
            self.assertIn('Version: 1.0.0', text)
            self.assertIn('Architecture: all', text)
            self.assertIn('Depends: python3', text)
            data = tarfile.open(fileobj=io.BytesIO(gzip.decompress(members['data.tar.gz'])))
            names = data.getnames()
            self.assertIn('usr/bin/incy-download', names)
            exe = data.getmember('usr/bin/incy-download')
            self.assertTrue(exe.mode & 0o111, 'binary must be executable')


if __name__ == '__main__':
    unittest.main()
