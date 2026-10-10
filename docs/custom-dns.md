# Custom DNS in INCY / تنظیم DNS دستی در اینسی

## EN

INCY travels with your subscription's DNS by default. To use your own DNS,
import one of the ready `dns` blocks as a **full Xray config**:

| File | Use when |
|:-----|:---------|
| [`configs/dns/dns-default.json`](../configs/dns/dns-default.json) | sane default (Cloudflare + Google, IPv4) |
| [`configs/dns/dns-iran.json`](../configs/dns/dns-iran.json) | inside Iran — Shecan resolvers (`178.22.122.100`, `185.51.200.2`) for sanctioned domains |
| [`configs/dns/dns-doh.json`](../configs/dns/dns-doh.json) | encrypted DNS-over-HTTPS (needs a recent Xray-core) |

Steps:

1. Open the file, copy the whole `"dns": {...}` object.
2. In INCY: import your server as **full Xray JSON** (full config import),
   replace its top-level `"dns"` section with the copied one.
3. Reconnect. Verify: `1.1.1.1/help` (Cloudflare) or `dnsleaktest.com`.

Manual edits: `"servers"` accepts plain IPs (`"8.8.8.8"`), and objects
(`{"address": "9.9.9.9", "port": 53, "domains": [...]}`). Keep
`"queryStrategy": "UseIPv4"` unless you know you have clean IPv6.

## FA

اینسی به‌صورت پیش‌فرض از DNS سابسکریپشن استفاده می‌کند. برای DNS دستی:

1. یکی از فایل‌های بالا را باز کنید و آبجکت `"dns"` را کپی کنید:
   - `dns-default.json` — پیش‌فرض (کلادفلر + گوگل)
   - `dns-iran.json` — داخل ایران (شکن: `178.22.122.100`)
   - `dns-doh.json` — رمزنگاری‌شده (DoH)
2. در اینسی سرور را به‌صورت **full Xray JSON** ایمپورت کنید و بخش `"dns"` را جای‌گذاری کنید.
3. وصل شوید و با `dnsleaktest.com` تست بگیرید.
