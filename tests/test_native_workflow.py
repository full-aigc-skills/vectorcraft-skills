"""真实原生工程、多格式导出与选择性改色回归。"""
import importlib.util
import sys

# 宿主技能快照必须保持不可变；动态导入也不写字节码。
sys.dont_write_bytecode = True
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ['CRAFT_INSTALLED_SKILL_ROOT']).resolve() if os.environ.get('CRAFT_INSTALLED_SKILL_ROOT') else ROOT / 'skills/vectorcraft-use'
SCRIPT = SKILL / 'scripts/workflow.py'


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
        plan = json.loads((SKILL / 'examples/brand-assets.json').read_text())
        next(o for o in plan['operations'] if o['command']=='paint.setFill')['params']['color']='#2366e8'
        next(o for o in plan['operations'] if o['command']=='text.create')['params']['color']='#2366e8'
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
            # 初始品牌图形与图标的配色必须独立，避免依赖原生 CLI 的隐式选择。
            from PIL import Image
            with Image.open(first / 'artboard-1.png') as brand, Image.open(first / 'artboard-2.png') as icon_image:
                brand_colors={color for count,color in brand.convert('RGBA').getcolors(brand.width*brand.height)}
                icon_colors={color for count,color in icon_image.convert('RGBA').getcolors(icon_image.width*icon_image.height)}
                self.assertIn((35,102,232,255),brand_colors)
                self.assertNotIn((239,91,54,255),brand_colors)
                self.assertIn((239,91,54,255),icon_colors)
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
            # 用户拿到的交换格式也必须更新品牌色，不能只修改原生 JSON。
            from PIL import Image
            with Image.open(first / 'artboard-1.png') as old_image, Image.open(second / 'artboard-1.png') as new_image:
                old_colors={color for count,color in old_image.convert('RGBA').getcolors(old_image.width*old_image.height)}
                new_colors={color for count,color in new_image.convert('RGBA').getcolors(new_image.width*new_image.height)}
                self.assertIn((23,92,206,255),new_colors)
                self.assertNotIn((23,92,206,255),old_colors)
                self.assertNotEqual(old_image.tobytes(),new_image.tobytes())
            updated_svg=(second / 'artboard-1.svg').read_text().lower().replace(' ','')
            self.assertTrue('#175cce' in updated_svg or 'rgb(23,92,206)' in updated_svg,
                            'exported SVG must contain the revised brand color')
            # 旧摘要必须失败；既有交付不能被替换。
            revision['expectedProjectSha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'revision_conflict'):
                module.execute(revision, root / 'bad', source=first)
            with self.assertRaisesRegex(ValueError, 'output_exists'):
                module.execute(plan, first)
            self.assertEqual(module.sha(first / 'project.vectorcraft'), manifest['files']['project.vectorcraft'])

if __name__ == '__main__':
    unittest.main()
