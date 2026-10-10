"""Build incy-downloader .deb with pure stdlib (works on Windows, no dpkg).

Package: incy-downloader (the manifest-based installer fetcher from
scripts/incy_download.py) -> /usr/bin/incy-download, Depends: python3.

Usage:  python scripts/build_deb.py [--version 1.0.0 --out dist]
"""
import argparse
import gzip
import io
import tarfile
import time
from pathlib import Path

ROOT = Path(__file__).parents[1]
PKG = 'incy-downloader'
ARCH = 'all'


def ar_entry(name, data, mtime=0, mode=0o644):
    name = (name + '/').encode('ascii')
    header = (
        name.ljust(16, b' ')
        + str(mtime).encode().ljust(12, b' ')
        + b'0'.ljust(6, b' ')
        + b'0'.ljust(6, b' ')
        + oct(mode)[2:].encode().rjust(8, b' ')
        + str(len(data)).encode().ljust(10, b' ')
        + b'`\n'
    )
    assert len(header) == 60
    body = data + (b'\n' if len(data) % 2 else b'')
    return header + body


def tar_gz(members):
    """members: list of (arcname, bytes, mode). Returns .tar.gz bytes."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w') as tar:
        for arcname, data, mode in members:
            info = tarfile.TarInfo(arcname)
            info.size = len(data)
            info.mtime = 0
            info.mode = mode
            tar.addfile(info, io.BytesIO(data))
    return gzip.compress(buf.getvalue(), mtime=0)


def control_text(version):
    return (
        f"Package: {PKG}\n"
        f"Version: {version}\n"
        "Section: net\n"
        "Priority: optional\n"
        f"Architecture: {ARCH}\n"
        "Depends: python3\n"
        "Maintainer: reza-em <noreply@example.com>\n"
        "Description: Fetch INCY installers from the versioned manifest\n"
        " Small helper that downloads INCY .exe/.deb/.apk from the pinned\n"
        " RELEASE.json URLs and verifies SHA256 when the manifest has it.\n"
    )


def build(version='1.0.0', out_dir=ROOT / 'dist'):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    script = (ROOT / 'scripts' / 'incy_download.py').read_bytes()
    if not script.startswith(b'#!'):
        script = b'#!/usr/bin/env python3\n' + script
    doc = (
        f"{PKG} {version}\n"
        "See: https://github.com/reza-em/incy-plus\n".encode()
    )
    control = tar_gz([('control', control_text(version).encode(), 0o644)])
    data = tar_gz([
        ('usr/bin/incy-download', script, 0o755),
        (f'usr/share/doc/{PKG}/README', doc, 0o644),
    ])
    deb = (
        b'!<arch>\n'
        + ar_entry('debian-binary', b'2.0\n')
        + ar_entry('control.tar.gz', control)
        + ar_entry('data.tar.gz', data)
    )
    path = out_dir / f'{PKG}_{version}_{ARCH}.deb'
    path.write_bytes(deb)
    print(f'wrote {path} ({len(deb)} bytes)')
    return path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--version', default='1.0.0')
    p.add_argument('--out', default='dist')
    args = p.parse_args()
    build(args.version, Path(args.out))


if __name__ == '__main__':
    main()
