<p align="center">
  <a href="https://github.com/reza-em/incy-platforms-plus/releases/download/tools-v1.0.0/incy-download.exe">
    <img src="https://img.shields.io/badge/Download_for_Windows-.exe-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Download incy-download.exe for Windows">
  </a>
  <a href="https://github.com/reza-em/incy-platforms-plus/releases/download/tools-v1.0.0/incy-downloader_1.0.0_all.deb">
    <img src="https://img.shields.io/badge/Download_for_Linux-.deb-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Download incy-downloader .deb for Linux">
  </a>
</p>

## EN — What is this?

`incy-download` fetches INCY installers from the pinned, versioned manifest
(`RELEASE.json`) — no broken `/latest` links — and verifies SHA256
automatically when the manifest carries it.

```console
incy-download list
incy-download get windows-x64 --out incy-setup.exe
incy-download get linux-x64-deb --out incy.deb
incy-download get android --out Incy.apk
```

- Windows: run `incy-download.exe` (no install needed)
- Linux: `sudo dpkg -i incy-downloader_1.0.0_all.deb` (needs `python3`), then run `incy-download`
- Full docs: [README.md](https://github.com/reza-em/incy-platforms-plus#readme) · [راهنمای فارسی](https://github.com/reza-em/incy-platforms-plus/blob/main/README.fa.md)

> The real INCY app binaries (setup.exe / .deb / .apk) are linked version-pinned
> from upstream in the README download buttons — this tool just fetches them safely.

## FA — این چیه؟

`incy-download` فایل نصب اینسی را از روی manifest ورژن‌دار می‌گیرد و SHA256 را
خودکار چک می‌کند. دکمه‌های گرافیکی بالا مستقیم دانلود می‌کنند.
