"""真实原始 CLI：文件能力由可信包装参数绑定，不从原生命令推断。"""
import os
import platform
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get('VECTORCRAFT_PERMISSION_BINARY')
SOURCE = os.environ.get('VECTORCRAFT_PERMISSION_SOURCE')

@unittest.skipUnless(platform.system() == 'Darwin' and BINARY and SOURCE, 'explicit native permission probe required')
class NativeCliFilesystemTests(unittest.TestCase):
    def invoke(self, target, *scope):
        return subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'skills/vectorcraft-use/scripts/cli.py'),
            '--runtime-home', str(Path(BINARY).parents[2]), *scope, '--', 'convert', SOURCE, str(target)],
            capture_output=True, text=True, timeout=30)

    def test_unbound_native_arguments_cannot_grant_read_or_write(self):
        with tempfile.TemporaryDirectory(prefix='cli scope ') as temporary:
            target = Path(temporary) / 'outside.svg'
            result = self.invoke(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())

    def test_read_permission_does_not_imply_write_permission(self):
        with tempfile.TemporaryDirectory(prefix='cli scope ') as temporary:
            target = Path(temporary) / 'outside.svg'
            result = self.invoke(target, '--read-root', str(Path(SOURCE).parent))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())

    def test_explicit_roots_allow_native_conversion(self):
        with tempfile.TemporaryDirectory(prefix='cli scope ') as temporary:
            target = Path(temporary) / 'authorized.svg'
            result = self.invoke(target, '--read-root', str(Path(SOURCE).parent), '--write-root', temporary)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('<svg', target.read_text())

if __name__ == '__main__':
    unittest.main()
