"""已安装单项布尔技能：真实孔洞、原生路径和交换导出，保留原工程。"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
sys.dont_write_bytecode = True


def objects(value):
    result = {}
    if isinstance(value, dict):
        if 'id' in value and 'kind' in value:
            result[value['id']] = value
        for child in value.values():
            result.update(objects(child))
    elif isinstance(value, list):
        for child in value:
            result.update(objects(child))
    return result


@unittest.skipUnless(os.environ.get('CRAFT_VECTOR_BOOLEAN_FIRST_USE') == '1',
                     'requires installed skill, public CLI archives, existing Pillow and PyMuPDF')
class BooleanGeometryFirstUseTests(unittest.TestCase):
    def test_four_native_operations_preserve_holes_and_unselected_shape(self):
        from PIL import Image
        import fitz
        with tempfile.TemporaryDirectory(prefix='craft-vector-boolean-') as temporary:
            root = Path(temporary)
            skill = root / '.agents/skills/vectorcraft-cli-boolean'
            shutil.copytree(os.environ['CRAFT_INSTALLED_VECTOR_BOOLEAN_SKILL'], skill,
                            ignore=shutil.ignore_patterns('__pycache__'))
            self.assertEqual(len(list(skill.parent.iterdir())), 1)
            spec = importlib.util.spec_from_file_location('isolated_boolean_workflow', skill / 'scripts/workflow.py')
            workflow = importlib.util.module_from_spec(spec); spec.loader.exec_module(workflow)
            runtime = root / 'empty-runtime'
            self.assertFalse(runtime.exists())
            operations = []
            for name, x, y, width, height, color in [
                ('outer', 16, 16, 80, 80, '#175cce'),
                ('inner', 40, 40, 32, 32, '#175cce'),
                ('sentinel', 110, 16, 8, 8, '#ef5b36')]:
                operations.extend([
                    {'command': 'shape.rectangle', 'params': {'x': x, 'y': y, 'width': width, 'height': height}, 'as': name},
                    {'command': 'paint.setFill', 'params': {'ids': [{'$ref': name + '.id'}], 'color': color}},
                    {'command': 'paint.setStroke', 'params': {'ids': [{'$ref': name + '.id'}], 'none': True}}])
            exports = [{'format': fmt, 'artboard': 0} for fmt in ['svg', 'png', 'pdf']]
            source = root / 'operands'
            first = workflow.execute({'document': {'name': 'Boolean assets', 'width': 128, 'height': 128, 'units': 'Pixels'},
                                      'operations': operations, 'exports': exports}, source, runtime_home=runtime)
            before = {p.name: workflow.sha(p) for p in source.iterdir() if p.is_file()}
            original = objects(json.loads((source / 'native.json').read_text())['layers'])
            sentinel = first['bindings']['sentinel']['id']
            ids = [first['bindings'][name]['id'] for name in ['outer', 'inner']]
            cases = [('unite', True, True, False), ('minusFront', True, False, True),
                     ('intersect', False, True, False), ('exclude', True, False, True)]
            for operation, outer_visible, center_visible, hole in cases:
                with self.subTest(operation=operation):
                    destination = root / operation
                    revised = workflow.execute({'expectedProjectSha256': first['files']['project.vectorcraft'],
                        'operations': [
                            {'command': 'select.set', 'params': {'ids': ids}},
                            {'command': 'object.pathfinder.' + operation, 'as': 'result'},
                            {'command': 'paint.setFill', 'params': {'ids': {'$ref': 'result.ids'}, 'color': '#175cce'}},
                            {'command': 'paint.setStroke', 'params': {'ids': {'$ref': 'result.ids'}, 'none': True}}],
                        'exports': exports}, destination, runtime_home=runtime, source=source)
                    native = objects(json.loads((destination / 'native.json').read_text())['layers'])
                    self.assertEqual(native[sentinel], original[sentinel])
                    self.assertTrue(set(ids).isdisjoint(native))
                    result_ids = revised['bindings']['result']['ids']
                    self.assertEqual(len(result_ids), 1)
                    kind = native[result_ids[0]]['kind']
                    if hole:
                        self.assertEqual(kind['type'], 'compound')
                        self.assertEqual(kind['rule'], 'NonZero')
                        paths = [path for child in kind['children'] for path in child['kind']['path']['subpaths']]
                        self.assertEqual(len(paths), 2)
                        areas = []
                        for path in paths:
                            points = [anchor['p'] for anchor in path['anchors']]
                            areas.append(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:] + points[:1])) / 2)
                        self.assertLess(areas[0] * areas[1], 0)
                        self.assertEqual(sorted(abs(area) for area in areas), [1024, 6400])
                    else:
                        self.assertEqual(kind['type'], 'path')
                        paths = kind['path']['subpaths']
                    self.assertTrue(all(path['closed'] for path in paths))
                    self.assertGreaterEqual(len(paths), 2 if hole else 1)
                    svg = (destination / 'artboard-1.svg').read_text()
                    self.assertNotIn('<image', svg.lower())
                    self.assertIn('<path', svg)
                    with fitz.open(destination / 'artboard-1.svg') as svg_document:
                        self.assertEqual(len(svg_document), 1)
                        rect = svg_document[0].rect
                        pixmap = svg_document[0].get_pixmap(matrix=fitz.Matrix(128 / rect.width, 128 / rect.height), alpha=True)
                        self.assertEqual((pixmap.width, pixmap.height), (128, 128))
                        self.check_pixels(Image.frombytes('RGBA', (128, 128), pixmap.samples), outer_visible, center_visible)
                    with Image.open(destination / 'artboard-1.png') as image:
                        rgba = image.convert('RGBA')
                        self.assertEqual(rgba.size, (128, 128))
                        self.check_pixels(rgba, outer_visible, center_visible)
                    with fitz.open(destination / 'artboard-1.pdf') as pdf:
                        self.assertEqual(len(pdf), 1)
                        self.assertTrue(pdf[0].get_drawings())
                        self.assertEqual(pdf[0].get_images(), [])
                        rect = pdf[0].rect
                        pixmap = pdf[0].get_pixmap(matrix=fitz.Matrix(128 / rect.width, 128 / rect.height), alpha=True)
                        self.assertEqual((pixmap.width, pixmap.height), (128, 128))
                        self.check_pixels(Image.frombytes('RGBA', (128, 128), pixmap.samples), outer_visible, center_visible)
                    self.assertEqual({p.name: workflow.sha(p) for p in source.iterdir() if p.is_file()}, before)
                    self.assertEqual(revised['sourceProjectSha256'], first['files']['project.vectorcraft'])
            with self.assertRaises((ValueError, RuntimeError)):
                workflow.execute({'expectedProjectSha256': first['files']['project.vectorcraft'],
                    'operations': [{'command': 'select.set', 'params': {'ids': [999999999]}},
                                   {'command': 'object.pathfinder.minusFront'}], 'exports': exports},
                    root / 'invalid-selection', runtime_home=runtime, source=source)
            self.assertFalse((root / 'invalid-selection').exists())
            self.assertEqual({p.name: workflow.sha(p) for p in source.iterdir() if p.is_file()}, before)
            self.assertFalse(any(skill.rglob('*.pyc')))

    def check_pixels(self, image, outer_visible, center_visible):
        for position, visible in [((24, 24), outer_visible), ((56, 56), center_visible), ((8, 8), False)]:
            pixel = image.getpixel(position)
            self.assertEqual(pixel[3], 255 if visible else 0, (position, pixel))
            if visible:
                self.assertTrue(all(abs(a - b) <= 2 for a, b in zip(pixel[:3], (23, 92, 206))), (position, pixel))
        pixel = image.getpixel((114, 20))
        self.assertEqual(pixel[3], 255)
        self.assertTrue(all(abs(a - b) <= 2 for a, b in zip(pixel[:3], (239, 91, 54))), pixel)


if __name__ == '__main__':
    unittest.main()
