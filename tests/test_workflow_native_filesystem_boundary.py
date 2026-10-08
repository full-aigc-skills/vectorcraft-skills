"""真实工作流不能借完整命令入口扩展文件权限。"""
import importlib.util
import os
import platform
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get('VECTORCRAFT_PERMISSION_BINARY')
SOURCE = os.environ.get('VECTORCRAFT_PERMISSION_SOURCE')

@unittest.skipUnless(platform.system() == 'Darwin' and BINARY and SOURCE, 'explicit native permission probe required')
class WorkflowNativeFilesystemTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('workflow_permissions', ROOT / 'skills/vectorcraft-use/scripts/workflow.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temporary = tempfile.TemporaryDirectory(prefix='vectorcraft workflow scope ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.seed = self.root / 'outside.vectorcraft'
        shutil.copyfile(SOURCE, self.seed)
        self.runtime = Path(BINARY).parents[2]

    def plan(self, command=None, params=None):
        return {'document': {'width': 64, 'height': 64, 'units': 'Pixels'},
                'operations': [] if command is None else [{'command': 'native.command', 'params': {'command': command, 'params': params}}]}

    def test_normal_creation_save_and_independent_reopen(self):
        output = self.root / 'delivery'
        result = self.module.execute(self.plan(), output, self.runtime)
        self.assertTrue((output / 'project.vectorcraft').is_file())
        self.assertIn('project.vectorcraft', result['files'])

    def test_model_command_cannot_open_undeclared_project(self):
        with self.assertRaises((ValueError, RuntimeError)):
            self.module.execute(self.plan('file.open', {'path': str(self.seed)}), self.root / 'delivery', self.runtime)

    def test_model_command_cannot_save_outside_stage(self):
        escaped = self.root / 'escaped.vectorcraft'
        with self.assertRaises((ValueError, RuntimeError)):
            self.module.execute(self.plan('file.save', {'path': str(escaped)}), self.root / 'delivery', self.runtime)
        self.assertFalse(escaped.exists())

if __name__ == '__main__':
    unittest.main()
