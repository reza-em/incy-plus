# Telegram proxy, separate from your config / پروکسی تلگرام جدا از کانفیگ

## EN

Telegram has its own proxy setting — you don't have to route the whole phone
through your subscription. The trick: give Telegram its own local door.

Ready full-config: [`configs/telegram/telegram-socks5.json`](../configs/telegram/telegram-socks5.json)
— a local **SOCKS5 on `127.0.0.1:10808`** whose traffic goes through your
server. Your main subscription stays untouched.

Steps:

1. Open `telegram-socks5.json`, replace the placeholders:
   `YOUR_SERVER_ADDRESS_HERE`, `YOUR_UUID_HERE`, and the Reality fields
   (`YOUR_SNI_HERE`, `YOUR_REALITY_PUBLIC_KEY_HERE`, `YOUR_SHORT_ID_HERE`).
   (No Reality on your server? Change `streamSettings` to your transport —
   see `docs.incy.cc` full-Xray reference.)
2. In INCY: **import as full Xray JSON**, connect once to verify.
3. In Telegram: **Settings → Data & Storage → Proxy → Add Proxy → SOCKS5**,
   host `127.0.0.1`, port `10808`, no auth → enable **Use Proxy**.
4. Done — only Telegram uses this tunnel. Toggle it off in Telegram any time.

Notes:

- Already have an MTProto link (`tg://proxy?...`)? Add it natively in the same
  Telegram proxy screen — no INCY involved. The SOCKS5 above is for when you
  want Telegram on *your own* server instead.
- Port `10808` is only an example; any free `127.0.0.1` port works — keep the
  inbound `port` and Telegram's port identical.
- Desktop Telegram (Windows/macOS/Linux) has the same SOCKS5 screen.

## FA

تلگرام تنظیم پروکسی خودش را دارد؛ لازم نیست کل گوشی را داخل تانل ببرید:

1. فایل `telegram-socks5.json` را باز کنید و جاهای `YOUR_SERVER...` و `YOUR_UUID...` را با مشخصات سرور خودتان پر کنید.
2. در اینسی به‌صورت **full Xray JSON** ایمپورت و یک بار وصل شوید.
3. در تلگرام: **Settings → Data & Storage → Proxy → Add Proxy → SOCKS5** با هاست `127.0.0.1` و پورت `10808`.
4. تمام — فقط تلگرام از این تانل استفاده می‌کند و سابسکریپشن اصلی دست نخورده می‌ماند.

اگر لینک MTProto آماده (`tg://proxy`) دارید، همان‌جا در تلگرام اضافه‌اش کنید و نیازی به اینسی نیست.
