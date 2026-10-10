import ipaddress
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parents[1]


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


class ConfigsTest(unittest.TestCase):
    def test_dns_blocks_have_usable_servers(self):
        for name in ('configs/dns/dns-default.json', 'configs/dns/dns-iran.json',
                     'configs/dns/dns-doh.json'):
            dns = load(name)['dns']
            self.assertTrue(dns['servers'], name)
            for srv in dns['servers']:
                addr = srv['address'] if isinstance(srv, dict) else srv
                try:
                    ipaddress.ip_address(addr)
                except ValueError:
                    self.assertTrue(urlparse(addr).scheme in ('https', 'quic', 'tcp'),
                                    f"{name}: bad server {addr!r}")

    def test_iran_dns_uses_shecancdn(self):
        dns = load('configs/dns/dns-iran.json')['dns']
        flat = [s if isinstance(s, str) else s.get('address', '') for s in dns['servers']]
        self.assertIn('178.22.122.100', flat)

    def test_telegram_config_structure(self):
        cfg = load('configs/telegram/telegram-socks5.json')
        inbounds = {i['tag']: i for i in cfg['inbounds']}
        self.assertEqual(inbounds['telegram-in']['protocol'], 'socks')
        self.assertEqual(inbounds['telegram-in']['listen'], '127.0.0.1')
        port = inbounds['telegram-in']['port']
        self.assertTrue(1024 <= port <= 65535)
        outbounds = {o['tag']: o for o in cfg['outbounds']}
        self.assertIn('proxy', outbounds)
        rules = cfg['routing']['rules']
        self.assertTrue(any('telegram-in' in r.get('inboundTag', []) for r in rules))
        # Must stay a template: no real server baked in.
        text = (ROOT / 'configs/telegram/telegram-socks5.json').read_text(encoding='utf-8')
        self.assertIn('YOUR_SERVER_ADDRESS_HERE', text)
        self.assertIn('YOUR_UUID_HERE', text)

    def test_docs_exist_and_link_configs(self):
        for doc in ('docs/custom-dns.md', 'docs/telegram-proxy.md'):
            text = (ROOT / doc).read_text(encoding='utf-8')
            self.assertIn('configs/', text, doc)


if __name__ == '__main__':
    unittest.main()
