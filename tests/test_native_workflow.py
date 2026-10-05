"""真实原生工程、多格式导出与选择性改色回归。"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/vectorcraft-use/scripts/workflow.py'


def objects(value):
    found = {}
    if isinstance(value, dict):
        if 'id' in value and 'kind' in value:
            found[value['id']] = value
        for child in value.values():
            found.update(objects(child))
    elif isinstance(value, list):
        for child in value:
            found.update(objects(child))
    return found


@unittest.skipUnless(os.environ.get('CRAFT_LIVE_TEST') == '1', 'real CLI workflow requires explicit live test')
class NativeWorkflowTests(unittest.TestCase):
    def test_boolean_artboards_exports_and_targeted_recolor(self):
        spec = importlib.util.spec_from_file_location('workflow', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        plan = json.loads((ROOT / 'skills/vectorcraft-use/examples/brand-assets.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / 'v1'
            manifest = module.execute(plan, first)
            native = json.loads((first / 'native.json').read_text())
            self.assertEqual(len(native['artboards']), 2)
            before = objects(native['layers'])
            self.assertNotIn(manifest['bindings']['square']['id'], before)
            self.assertNotIn(manifest['bindings']['circle']['id'], before)
            self.assertIn(manifest['bindings']['logo']['ids'][0], before)
            for item in manifest['outputs']:
                file = first / item['path']
                self.assertEqual(module.sha(file), manifest['files'][file.name])
                if file.suffix == '.svg':
                    tree = ET.parse(file)
                    self.assertEqual(tree.getroot().tag, '{http://www.w3.org/2000/svg}svg')
                    self.assertFalse(tree.findall('.//{http://www.w3.org/2000/svg}image'))
                elif file.suffix == '.png':
                    self.assertEqual(file.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
                else:
                    self.assertTrue(file.read_bytes().startswith(b'%PDF-'))
            revision = {'expectedProjectSha256': manifest['files']['project.vectorcraft'],
                        'operations': [{'command': 'paint.setFill', 'params': {'ids': [{'$ref': 'logo.ids.0'}, {'$ref': 'wordmark.id'}], 'color': '#175cce'}}],
                        'exports': plan['exports']}
            second = root / 'v2'
            changed = module.execute(revision, second, source=first)
            after = objects(json.loads((second / 'native.json').read_text())['layers'])
            self.assertEqual(before[manifest['bindings']['icon']['id']], after[manifest['bindings']['icon']['id']])
            self.assertNotEqual(before[manifest['bindings']['logo']['ids'][0]], after[manifest['bindings']['logo']['ids'][0]])
            self.assertEqual((first / 'artboard-2.png').read_bytes(), (second / 'artboard-2.png').read_bytes())
            self.assertEqual(changed['sourceProjectSha256'], manifest['files']['project.vectorcraft'])
            # 旧摘要必须失败；既有交付不能被替换。
            revision['expectedProjectSha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'revision_conflict'):
                module.execute(revision, root / 'bad', source=first)
            with self.assertRaisesRegex(ValueError, 'output_exists'):
                module.execute(plan, first)
            self.assertEqual(module.sha(first / 'project.vectorcraft'), manifest['files']['project.vectorcraft'])

if __name__ == '__main__':
    unittest.main()
