"""权限策略来自可信调用层，拒绝路径与策略注入并保留系统别名边界。"""
import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / 'skills/vectorcraft-use/scripts/filesystem_scope.py'))

class FilesystemScopeTests(unittest.TestCase):
    def test_unknown_model_policy_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'invalid_filesystem_policy'):
            MODULE['profile']('/usr/bin/true', {'allowDefault': True})

    def test_relative_control_character_and_non_path_roots_are_rejected(self):
        for value in ['relative', '/tmp/a\n(allow default)', 12, '']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODULE['profile']('/usr/bin/true', {'writeRoots': [value]})

    def test_quotes_are_escaped_and_system_aliases_only_grant_metadata(self):
        with tempfile.TemporaryDirectory(prefix='filesystem " scope ') as temporary:
            text = MODULE['profile']('/usr/bin/true', {'writeRoots': [temporary]})
            self.assertIn('(subpath ' + json.dumps(str(Path(temporary).resolve()), ensure_ascii=False) + ')', text)
            if temporary.startswith('/var/'):
                self.assertIn('(literal "/var")', text)
            self.assertNotIn('(subpath "/var")', text)
            self.assertNotIn('(subpath "/System")', text)
            self.assertNotIn('(subpath "/usr")', text)
            self.assertNotIn('(allow default)', text)

    def test_only_explicit_loopback_ports_are_allowed(self):
        text = MODULE['profile']('/usr/bin/true', {'ports': [32000]})
        self.assertIn('localhost:32000', text)
        self.assertNotIn('network-outbound', MODULE['profile']('/usr/bin/true', {}))
        for port in [True, 80, 65536, '32000']:
            with self.subTest(port=port), self.assertRaisesRegex(ValueError, 'invalid_filesystem_ports'):
                MODULE['profile']('/usr/bin/true', {'ports': [port]})

    def test_graphics_capability_is_explicit_and_limited(self):
        self.assertNotIn('iokit-open', MODULE['profile']('/usr/bin/true', {}))
        text = MODULE['profile']('/usr/bin/true', {'graphics': True})
        self.assertIn('AGXDeviceUserClient', text)
        self.assertNotIn('(allow iokit-open)', text)
        with self.assertRaisesRegex(ValueError, 'invalid_filesystem_graphics'):
            MODULE['profile']('/usr/bin/true', {'graphics': 'true'})

    def test_write_command_cannot_use_read_only_root(self):
        with self.assertRaisesRegex(ValueError, 'filesystem_write_outside_root'):
            MODULE['authorize_command']('file.save', {'path': '/input/project.vectorcraft'}, {'readRoots': ['/input'], 'writeRoots': ['/output']})

    def test_geometry_path_is_not_a_filesystem_path(self):
        MODULE['authorize_command']('text.createInPath', {'path': 2}, {})
        MODULE['authorize_command']('imageTrace.make', {'params': {'paths': 12}}, {})

    def test_file_queue_and_parent_traversal_obey_canonical_roots(self):
        policy = {'readRoots': ['/input'], 'writeRoots': ['/output']}
        MODULE['authorize_command']('file.place.queue', {'paths': ['/input/first.svg', '/input/second.svg']}, policy)
        with self.assertRaisesRegex(ValueError, 'filesystem_read_outside_root'):
            MODULE['authorize_command']('file.place.queue', {'paths': ['/input/../outside.svg']}, policy)

    def test_aliased_executable_keeps_only_ancestor_metadata(self):
        text = MODULE['profile']('/var/folders/example/vectorcraft-cli', {})
        self.assertIn('(literal "/var")', text)
        self.assertNotIn('(subpath "/var")', text)

    def test_unqualified_platform_does_not_fall_back_to_unconfined_launch(self):
        with patch('platform.system', return_value='Linux'):
            with self.assertRaisesRegex(ValueError, 'filesystem_adapter_platform_unqualified'):
                MODULE['launch'](['/usr/bin/true'], {})

if __name__ == '__main__':
    unittest.main()
