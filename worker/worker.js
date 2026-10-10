/**
 * INCY per-platform latest redirect (Cloudflare Worker).
 *
 * GitHub gives only one global /releases/latest, so Android must not use it.
 * Deploy this worker (see wrangler.toml) and point users at stable routes:
 *
 *   https://dl.incy.cc/android            -> Incy.apk (current android.download)
 *   https://dl.incy.cc/android.json       -> latest-android.json
 *   https://dl.incy.cc/desktop            -> windows x64 setup (default)
 *   https://dl.incy.cc/desktop/windows    -> incy-windows-setup.exe
 *   https://dl.incy.cc/desktop/macos-arm  -> arm64 dmg
 *   https://dl.incy.cc/desktop/linux-x64  -> .deb
 *   https://dl.incy.cc/health             -> {android, desktop, ios} versions
 *
 * Source of truth is RELEASE.json on main (5-min cache).
 */
const MANIFEST_URL =
  'https://raw.githubusercontent.com/INCY-DEV/incy-platforms/main/RELEASE.json';

let cache = { at: 0, data: null };

async function manifest() {
  if (cache.data && Date.now() - cache.at < 5 * 60 * 1000) return cache.data;
  const r = await fetch(MANIFEST_URL, { cf: { cacheTtl: 300, cacheEverything: true } });
  if (!r.ok) throw new Error('manifest fetch failed: ' + r.status);
  cache = { at: Date.now(), data: await r.json() };
  return cache.data;
}

function redirect(url, permanent = false) {
  return Response.redirect(url, permanent ? 301 : 302);
}

export default {
  async fetch(request) {
    const u = new URL(request.url);
    const p = u.pathname.replace(/\/+$/, '') || '/';
    try {
      const m = await manifest();
      const d = m.desktop;
      const routes = {
        '/android': m.android.download,
        '/android.json': null, // served as JSON below
        '/desktop': d.windows.x64,
        '/desktop/windows': d.windows.x64,
        '/desktop/windows-portable': d.windows.x64_portable,
        '/desktop/macos-arm': d.macos.arm64,
        '/desktop/macos-intel': d.macos.intel,
        '/desktop/linux-x64': d.linux.x64_deb,
        '/desktop/linux-arm64': d.linux.arm64_deb,
        '/ios': m.ios.AppStore,
      };
      if (p === '/health') {
        return Response.json({
          android: m.android.version, desktop: d.version, ios: m.ios.version,
        });
      }
      if (p === '/android.json') {
        const { version, tag, download, name, sha256 } = m.android;
        return Response.json({ platform: 'android', version, tag, download, name, sha256 });
      }
      if (p === '/desktop.json') {
        const { version, tag, name, windows, macos, linux, sha256 } = d;
        return Response.json({ platform: 'desktop', version, tag, name, windows, macos, linux, sha256 });
      }
      if (p in routes && routes[p]) return redirect(routes[p]);
      return new Response('Not found. Try /android, /desktop, /health', { status: 404 });
    } catch (e) {
      return new Response('Upstream manifest unavailable', { status: 502 });
    }
  },
};
