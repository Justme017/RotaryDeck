import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import model

DEFAULT = Path(__file__).parent / 'profiles' / 'default.json'

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = model.load_profile(DEFAULT)

    def test_default(self):
        self.assertEqual(len(self.profile['apps']), 6)
        self.assertEqual(len(self.profile['actions']), 6)

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            self.assertIsNone(model.save_profile(self.profile, path))
            self.assertEqual(model.load_profile(path), self.profile)

    def test_duplicate_slots(self):
        self.profile['apps'][1]['slot'] = 1
        with self.assertRaises(model.ProfileError):
            model.validate(self.profile)

    def test_boolean_slot(self):
        self.profile['apps'][0]['slot'] = True
        with self.assertRaises(model.ProfileError):
            model.validate(self.profile)

    def test_unknown_fields(self):
        self.profile['apps'][0]['shell'] = True
        with self.assertRaises(model.ProfileError):
            model.validate(self.profile)

    def test_bad_labels(self):
        for value in ('', '   ', 'x' * 17, 'bad\nlabel'):
            self.profile['apps'][0]['label'] = value
            with self.assertRaises(model.ProfileError):
                model.validate(self.profile)

    def test_bad_urls(self):
        for value in ('file:///tmp/x', 'javascript:alert(1)', 'https://', 'https://a b.com', 'https://user:pass@example.com'):
            with self.assertRaises(model.ProfileError):
                model.valid_url(value)

    def test_good_url(self):
        self.assertEqual(model.valid_url('https://www.netflix.com'), 'https://www.netflix.com')

    def test_bad_builtin(self):
        self.profile['actions'][0]['builtin_action'] = 'execute_shell'
        with self.assertRaises(model.ProfileError):
            model.validate(self.profile)

    def test_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            path.write_text('{"schema_version":1,"schema_version":2}', encoding='utf-8')
            with self.assertRaises(model.ProfileError):
                model.load_profile(path)

    def test_backup_retention(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            model.save_profile(self.profile, path)
            for _ in range(12):
                model.save_profile(self.profile, path)
            backups = list((Path(directory) / 'backups').glob('*.json'))
            self.assertEqual(len(backups), 10)
            self.assertEqual(model.load_profile(backups[0]), self.profile)

    def test_failed_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'profile.json'
            model.save_profile(self.profile, path)
            original = path.read_bytes()
            self.profile['profile_name'] = 'Changed'
            with patch('model.os.replace', side_effect=OSError('denied')):
                with self.assertRaises(OSError):
                    model.save_profile(self.profile, path)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(list(Path(directory).glob('*.tmp')), [])

    def test_requires_confirmation(self):
        with self.assertRaises(model.ProfileError):
            model.test_action(self.profile['apps'][1])

    def test_unsupported_execution(self):
        with self.assertRaises(model.ProfileError):
            model.test_action(self.profile['apps'][0], confirmed=True)

    def test_no_execution_on_load_save(self):
        with patch('model.test_action', side_effect=AssertionError('must not execute')):
            with tempfile.TemporaryDirectory() as directory:
                model.save_profile(model.load_profile(DEFAULT), Path(directory) / 'profile.json')

if __name__ == '__main__':
    unittest.main(verbosity=2)
