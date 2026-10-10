import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('ios', Path(__file__).parents[1] / 'scripts/update_ios.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class IosTest(unittest.TestCase):
    def test_update_sets_version_build_name(self):
        data = {'ios': {'version': '2.4.5', 'build': '2007260046',
                        'AppStore': 'https://apps.apple.com/us/app/incy/id6756943388', 'name': 'INCY 2.4.5'}}
        self.assertTrue(m.update_ios(data, '2.4.6', '2007260047'))
        self.assertEqual(data['ios']['version'], '2.4.6')
        self.assertEqual(data['ios']['name'], 'INCY 2.4.6')

    def test_downgrade_refused(self):
        data = {'ios': {'version': '2.4.5', 'build': '2007260046',
                        'AppStore': 'https://apps.apple.com/us/app/incy/id6756943388', 'name': 'INCY 2.4.5'}}
        self.assertFalse(m.update_ios(data, '2.4.4', '999'))
        self.assertFalse(m.update_ios(data, '2.4.5', '2007260046'))
        self.assertEqual(data['ios']['version'], '2.4.5')

    def test_bad_inputs_rejected(self):
        data = {}
        with self.assertRaises(ValueError):
            m.update_ios(data, '2.4', '123')
        with self.assertRaises(ValueError):
            m.update_ios(data, '2.4.6', 'build!')
        with self.assertRaises(ValueError):
            m.update_ios(data, '2.4.6', '123', appstore='https://evil.example/incy')
        self.assertEqual({}, data)


if __name__ == '__main__':
    unittest.main()
