"""真实签名桌面和桥接CLI共享文件边界；不以监听就绪代替保存重开。"""
import importlib.util
import json
import os
import platform
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get('VECTORCRAFT_PERMISSION_BINARY')
SOURCE = os.environ.get('VECTORCRAFT_PERMISSION_SOURCE')

@unittest.skipUnless(platform.system() == 'Darwin' and BINARY and SOURCE and os.environ.get('VECTORCRAFT_PERMISSION_DESKTOP') == '1', 'explicit signed desktop permission probe required')
class NativeDesktopFilesystemTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('desktop_permissions', ROOT / 'skills/vectorcraft-use/scripts/desktop_session.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.tmp = tempfile.TemporaryDirectory(prefix='vectorcraft desktop scope ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.seed = self.root / 'outside.vectorcraft'
        shutil.copyfile(SOURCE, self.seed)
        self.runtime = Path(BINARY).parents[2]

    def check(self, plan, result):
        output = self.root / 'delivery'
        receipt = self.module.run(plan, output, self.runtime)
        self.assertEqual(receipt['result'], result, receipt.get('error'))
        proof = json.loads((output / 'desktop-session.json').read_text())
        self.assertTrue(proof['ownedProcessesStopped'])
        self.assertTrue(proof['listenerOwnedByPID'])
        return output

    def test_normal_gui_native_save_reopen_and_export(self):
        plan = json.loads((ROOT / 'skills/vectorcraft-use/examples/desktop-first-use.json').read_text())
        output = self.check(plan, 'PASS')
        self.assertTrue((output / 'project.vectorcraft').is_file())
        self.assertIn('<svg', (output / 'preview.svg').read_text())

    def test_gui_command_cannot_open_undeclared_project(self):
        self.check({'schema': 'craft-command-plan/v1', 'operations': [{'command': 'file.open', 'params': {'path': str(self.seed)}}]}, 'FAIL')

    def test_gui_command_cannot_write_outside_delivery(self):
        escaped = self.root / 'escaped.vectorcraft'
        self.check({'schema': 'craft-command-plan/v1', 'operations': [
            {'command': 'file.new', 'params': {'width': 64, 'height': 64, 'units': 'Pixels'}},
            {'command': 'file.save', 'params': {'path': str(escaped)}}]}, 'FAIL')
        self.assertFalse(escaped.exists())

if __name__ == '__main__':
    unittest.main()
