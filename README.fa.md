<div align="center">

# اینسی‌پلاس | INCY+ — فیلترشکن و پروکسی Xray برای اندروید، ویندوز، مک و لینوکس

**دانلود مستقیم INCY با VLESS و Reality، VMess، Trojan، Shadowsocks، Hysteria2 و WireGuard**

[English README](README.md) · [نصب اندروید با Obtainium](obtainium.json) · [فید نسخه‌ها](RELEASE.json) · [تاریخچه](CHANGELOG.md)

</div>

## دانلود

<p align="center">
  <a href="https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-windows-setup.exe">
    <img src="https://img.shields.io/badge/دانلود_ویندوز_.exe-3.8.8-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="دانلود اینسی برای ویندوز">
  </a>
  <a href="https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-linux-x64.deb">
    <img src="https://img.shields.io/badge/دانلود_لینوکس_.deb-3.8.8-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="دانلود اینسی برای لینوکس">
  </a>
</p>

### موبایل و تلویزیون

| پلتفرم | لینک |
|:---------|:-----|
| آیفون / اپل تی‌وی / مک (اپ‌استور) | [App Store](https://apps.apple.com/ru/app/incy/id6756943388) |
| اندروید / اندروید تی‌وی (گوگل‌پلی) | [Google Play](https://play.google.com/store/apps/details?id=llc.itdev.incy) |
| فایل APK اندروید (نصب مستقیم) | [Download APK](https://github.com/INCY-DEV/incy-platforms/releases/download/android-v3.7.0/Incy.apk) |

### دسکتاپ (ویندوز، مک، لینوکس)

> نسخه دسکتاپ **پیش‌آلفا** است؛ برای استفاده روزمره خوب است ولی ممکن است تغییر کند.

| پلتفرم | نصبی | پرتابل |
|:---------|:----------|:---------|
| ویندوز | [Setup](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-windows-setup.exe) | [ZIP](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-windows-portable.zip) |
| مک اپل سیلیکون | [DMG](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-macos-arm64.dmg) | — |
| مک اینتل | [DMG](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-macos-intel.dmg) | — |
| لینوکس | [DEB](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-linux-x64.deb) | [ZIP](https://github.com/INCY-DEV/incy-platforms/releases/download/desktop-v3.8.8/incy-linux-x64-portable.zip) |

## آپدیت اندروید با Obtainium

ریلیزهای اندروید با تگ **`android-vX.Y.Z`** و دسکتاپ با **`desktop-vX.Y.Z`** منتشر می‌شوند (نسخه‌ها مستقل‌اند).
فایل [`obtainium.json`](obtainium.json) را در Obtainium ایمپورت کنید یا دستی:

| تنظیم | مقدار |
|:--------|:------|
| Source | `https://github.com/INCY-DEV/incy-platforms` |
| Filter release titles | `^Android v[0-9]+\.[0-9]+\.[0-9]+$` |
| Filter APKs | `^[Ii]ncy\.apk$` |
| Verify Latest Tag | **خاموش** |

## پروتکل‌ها

`VLESS (Reality)` `VMess` `Trojan` `Shadowsocks` `Hysteria2` `SOCKS5` `WireGuard`

## راهنماها

- [DNS دستی](docs/custom-dns.md) — پیش‌فرض / ایران (شکن) / رمزنگاری‌شده برای ایمپورت full Xray
- [پروکسی تلگرام](docs/telegram-proxy.md) — SOCKS5 محلی جدا (`127.0.0.1:10808`) مستقل از سابسکریپشن

## چرا این فورک (incy-plus)؟

- فید نسخه تفکیک‌شده بدون باگ `/latest` گلوبال: [`RELEASE.json`](RELEASE.json)، [`latest-android.json`](latest-android.json)، [`latest-desktop.json`](latest-desktop.json)
- چک‌سام `SHA256`، تست خودکار لینک‌ها، چنج‌لاگ خودکار ([`CHANGELOG.md`](CHANGELOG.md))
- ورک‌فلوهای انتشار اندروید، دسکتاپ و iOS + ریدایرکت اختیاری Cloudflare (`worker/`)
- روش انتشار: [RELEASING.md](RELEASING.md)

## سئو / Keywords

INCY+ download, دانلود اینسی پلاس, دانلود اینسی, فیلترشکن قوی اندروید و ویندوز, VLESS Reality client, Xray-core proxy, Shadowsocks, Hysteria2, Trojan, WireGuard, Obtainium APK.
