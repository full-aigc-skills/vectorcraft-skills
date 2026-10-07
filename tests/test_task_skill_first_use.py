"""VectorCraft 九类独立场景技能首次安装、原生结构及真实导出验收。"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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


class TaskSkillContractTests(unittest.TestCase):
    def test_shapes_and_boolean_carry_explicit_selection(self):
        for task in ('shapes', 'boolean'):
            rows = json.loads((ROOT / 'skills' / ('vectorcraft-cli-' + task) / 'references/commands.json').read_text())['commands']
            self.assertIn('select.set', {row['id'] for row in rows})

    def test_assets_carry_placement_and_symbol_selection(self):
        rows = json.loads((ROOT / 'skills/vectorcraft-cli-assets/references/commands.json').read_text())['commands']
        self.assertTrue({'file.place', 'select.set', 'links.embed', 'symbol.new'}.issubset({row['id'] for row in rows}))


@unittest.skipUnless(os.environ.get('CRAFT_TASK_FIRST_USE') == '1',
                     'requires macOS arm64, public archives and Pillow')
class TaskSkillFirstUseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='vectorcraft-task-fixture-')
        cls.fixture = Path(cls.temporary.name)
        skill = ROOT / 'skills/vectorcraft-use'
        spec = importlib.util.spec_from_file_location('vector_task_fixture', skill / 'scripts/workflow.py')
        workflow = importlib.util.module_from_spec(spec); spec.loader.exec_module(workflow)
        result = workflow.execute(json.loads((skill / 'examples/brand-assets.json').read_text()),
                                  cls.fixture / 'base', runtime_home=cls.fixture / 'fixture-runtime')
        cls.project = cls.fixture / 'base/project.vectorcraft'
        cls.project_sha = digest(cls.project)
        cls.logo = result['bindings']['logo']['ids'][0]
        cls.text = result['bindings']['wordmark']['id']
        cls.icon = result['bindings']['icon']['id']

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='vectorcraft-task-single-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runtime = self.root / 'fresh-runtime'
        self.environment = dict(os.environ, PATH='/usr/bin:/bin')
        self.addCleanup(lambda: self.assertEqual(digest(self.project), self.project_sha))

    def install_only(self, task):
        self.skill = self.root / '.agents/skills' / ('vectorcraft-cli-' + task)
        shutil.copytree(ROOT / 'skills' / self.skill.name, self.skill,
                        ignore=shutil.ignore_patterns('__pycache__'))
        self.assertEqual(len(list((self.root / '.agents/skills').iterdir())), 1)
        self.assertFalse(self.runtime.exists())

    def cli(self, *arguments, success=True):
        result = subprocess.run([sys.executable, '-I', '-B', str(self.skill / 'scripts/cli.py'),
                                 '--runtime-home', str(self.runtime), '--', *map(str, arguments)],
                                env=self.environment, capture_output=True, text=True, timeout=240)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            lock = json.loads((self.skill / 'scripts/runtime.lock.json').read_text())
            binary = self.runtime / 'vectorcraft' / lock['resolvedVersion'] / 'vectorcraft-cli'
            self.assertTrue(binary.is_file())
            self.assertEqual(digest(binary), lock['artifacts']['darwin-arm64']['binarySha256'])
            receipt = json.loads((binary.parent / 'installation.json').read_text())
            self.assertEqual(receipt['version'], lock['resolvedVersion'])
        else:
            self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(self.skill.rglob('*.pyc')))
        return result

    def execute(self, operations, target, source=None, new=False):
        argv = ['run'] if new else ['run', '--in', str(source or self.project)]
        for command, params in operations:
            argv += ['--cmd', command, '--params', json.dumps(params)]
        result = self.cli(*argv, '--export', target)
        rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        commands = [row for row in rows if row.get('step') == 'cmd']
        self.assertEqual([row['command'] for row in commands], [command for command, _ in operations])
        return [row['result'] for row in commands]

    def native(self, project):
        result = self.cli('run', '--in', project, '--cmd', 'document.json')
        return next(json.loads(line)['result'] for line in result.stdout.splitlines()
                    if json.loads(line).get('command') == 'document.json')

    def object(self, project, identifier):
        return objects(self.native(project)['layers'])[identifier]

    def render(self, project, artboard=0, name='frame.png'):
        target = self.root / name
        self.cli('convert', project, target, '--artboard', artboard)
        return target

    def same_board(self, before, after, artboard):
        from PIL import Image
        with Image.open(self.render(before, artboard, 'before.png')) as a, Image.open(self.render(after, artboard, 'after.png')) as b:
            self.assertEqual(a.convert('RGBA').tobytes(), b.convert('RGBA').tobytes())

    def test_project_creates_and_reopens_native_geometry(self):
        self.install_only('project'); target = self.root / 'new.vectorcraft'
        result = self.execute([('file.new', {'name': 'Standalone', 'width': 64, 'height': 48, 'units': 'Pixels'}),
                               ('shape.rectangle', {'x': 8, 'y': 8, 'width': 20, 'height': 20})], target, new=True)
        native = self.native(target)
        self.assertEqual(len(native['artboards']), 1)
        self.assertEqual(native['artboards'][0]['rect'], {'x0': 0.0, 'y0': 0.0, 'x1': 64.0, 'y1': 48.0})
        self.assertIn('path', self.object(target, result[1]['id'])['kind'])
        self.cli('invented-subcommand', success=False)

    def test_selection_targets_icon_before_move_and_preserves_brand_board(self):
        from PIL import Image
        self.install_only('selection')
        target = self.root / 'selected-icon.vectorcraft'
        before = self.object(self.project, self.icon)
        self.execute([('select.none', {}), ('select.set', {'ids': [self.icon]}),
                      ('object.move', {'dx': 8, 'dy': 0})], target)
        self.assertNotEqual(self.object(target, self.icon), before)
        self.assertEqual(self.object(target, self.logo), self.object(self.project, self.logo))
        self.assertEqual(self.object(target, self.text), self.object(self.project, self.text))
        self.same_board(self.project, target, 0)
        with Image.open(self.render(self.project, 1, 'before-selection.png')) as old, \
                Image.open(self.render(target, 1, 'after-selection.png')) as new:
            self.assertNotEqual(old.convert('RGBA').tobytes(), new.convert('RGBA').tobytes())

    def test_paths_keep_control_handle_and_change_only_icon_board(self):
        from PIL import Image
        self.install_only('paths'); target = self.root / 'path.vectorcraft'
        self.execute([('path.setAnchors', {'id': self.icon, 'subpaths': [{'anchors': [
            {'x': 344, 'y': 64, 'out': [380, 30]}, {'x': 456, 'y': 64}, {'x': 400, 'y': 176}], 'closed': True}]})], target)
        path = self.object(target, self.icon)['kind']['path']['subpaths'][0]
        self.assertEqual(path['anchors'][0]['out'], [380.0, 30.0])
        self.assertTrue(path['closed'])
        self.same_board(self.project, target, 0)
        with Image.open(self.render(self.project, 1, 'old-icon.png')) as before, Image.open(self.render(target, 1, 'new-icon.png')) as after:
            self.assertNotEqual(before.tobytes(), after.tobytes())

    def test_shapes_create_group_and_move_without_changing_existing_logo(self):
        self.install_only('shapes'); shapes, target = self.root / 'shapes.vectorcraft', self.root / 'group.vectorcraft'
        result = self.execute([('shape.rectangle', {'x': 8, 'y': 8, 'width': 20, 'height': 20}),
                               ('shape.ellipse', {'x': 30, 'y': 8, 'width': 20, 'height': 20})], shapes)
        ids = [entry['id'] for entry in result]
        result = self.execute([('select.set', {'ids': ids}), ('object.group', {}),
                               ('object.move', {'dx': 8, 'dy': 0})], target, shapes)
        group = self.object(target, result[1]['id'])
        self.assertEqual({child['id'] for child in group['kind']['children']}, set(ids))
        self.assertEqual(self.object(target, self.logo), self.object(self.project, self.logo))
        self.same_board(self.project, target, 1)

    def test_boolean_union_is_editable_path_and_preserves_existing_icon(self):
        self.install_only('boolean'); shapes, target = self.root / 'bool-shapes.vectorcraft', self.root / 'union.vectorcraft'
        result = self.execute([('shape.rectangle', {'x': 8, 'y': 8, 'width': 24, 'height': 24}),
                               ('shape.ellipse', {'x': 20, 'y': 8, 'width': 24, 'height': 24})], shapes)
        ids = [row['id'] for row in result]
        result = self.execute([('select.set', {'ids': ids}), ('object.pathfinder.unite', {})], target, shapes)
        output = result[1]['ids']
        self.assertEqual(len(output), 1)
        current = objects(self.native(target)['layers'])
        self.assertTrue(set(ids).isdisjoint(current))
        self.assertIn('path', current[output[0]]['kind'])
        self.assertEqual(self.object(target, self.icon), self.object(self.project, self.icon))

    def test_text_revision_preserves_editable_type_and_icon(self):
        self.install_only('text'); target = self.root / 'text.vectorcraft'
        self.execute([('text.setText', {'id': self.text, 'text': 'NOVA PLUS'})], target)
        changed = self.object(target, self.text)
        self.assertEqual(changed['kind']['type'], 'text')
        self.assertEqual(''.join(run['text'] for run in changed['kind']['runs']), 'NOVA PLUS')
        self.assertEqual(self.object(target, self.logo), self.object(self.project, self.logo))
        self.same_board(self.project, target, 1)

    def test_appearance_recolors_brand_and_preserves_icon_pixels(self):
        from PIL import Image
        self.install_only('appearance'); target = self.root / 'blue.vectorcraft'
        self.execute([('paint.setFill', {'ids': [self.logo, self.text], 'color': '#175cce'})], target)
        self.assertNotEqual(self.object(target, self.logo)['appearance'], self.object(self.project, self.logo)['appearance'])
        self.assertEqual(self.object(target, self.icon), self.object(self.project, self.icon))
        self.same_board(self.project, target, 1)
        with Image.open(self.render(self.project, 0, 'old-brand.png')) as before, Image.open(self.render(target, 0, 'new-brand.png')) as after:
            self.assertNotEqual(before.tobytes(), after.tobytes())
            self.assertGreater(after.convert('RGBA').getpixel((70, 70))[2], 150)

    def test_artboards_resize_icon_and_export_correct_dimensions(self):
        from PIL import Image
        self.install_only('artboards'); target = self.root / 'artboards.vectorcraft'
        self.execute([('artboard.setProps', {'index': 1, 'name': 'Icon wide', 'width': 320, 'height': 192})], target)
        native = self.native(target)
        self.assertEqual(native['artboards'][1]['name'], 'Icon wide')
        rect = native['artboards'][1]['rect']
        self.assertEqual((rect['x1'] - rect['x0'], rect['y1'] - rect['y0']), (320, 192))
        self.same_board(self.project, target, 0)
        with Image.open(self.render(target, 1, 'wide-icon.png')) as image:
            self.assertEqual(image.size, (320, 192))

    def test_assets_embed_image_and_create_reusable_symbol(self):
        from PIL import Image
        self.install_only('assets'); image = self.root / 'linked.png'
        Image.new('RGBA', (16, 16), (20, 40, 220, 255)).save(image)
        placed, embedded, symbols = [self.root / (name + '.vectorcraft') for name in ('placed', 'embedded', 'symbols')]
        ids = self.execute([('file.place', {'path': str(image), 'link': True, 'rect': [0, 0, 16, 16]})], placed)[0]['ids']
        result = self.execute([('links.embed', {'ids': ids})], embedded, placed)[0]
        self.assertEqual(result['embedded'], ids); self.assertEqual(result['missing'], [])
        image.unlink()
        with Image.open(self.render(embedded, 0, 'embedded.png')) as frame:
            self.assertEqual(frame.convert('RGBA').getpixel((8, 8)), (20, 40, 220, 255))
        rejected = self.root / 'unselected-symbol.vectorcraft'
        self.cli('run', '--in', self.project, '--cmd', 'symbol.new', '--params',
                 json.dumps({'name': 'No active selection', 'ids': [self.logo]}), '--export', rejected, success=False)
        self.assertFalse(rejected.exists())
        result = self.execute([('select.set', {'ids': [self.logo]}), ('symbol.new', {'name': 'Brand mark'}),
                               ('symbol.place', {'name': 'Brand mark', 'x': 64, 'y': 32})], symbols)
        self.assertEqual(result[1]['name'], 'Brand mark')
        current = objects(self.native(symbols)['layers'])
        self.assertIn(result[1]['id'], current); self.assertIn(result[2]['id'], current)
        self.assertTrue(self.native(symbols)['symbols'])
        self.assertEqual(self.object(symbols, self.icon), self.object(self.project, self.icon))

    def test_export_svg_pdf_png_retains_vector_structure_and_board_scope(self):
        self.install_only('export')
        outputs = {extension: self.root / ('icon.' + extension) for extension in ('svg', 'pdf', 'png')}
        for extension, path in outputs.items():
            self.cli('convert', self.project, path, '--artboard', 1)
        svg = ET.parse(outputs['svg']).getroot()
        self.assertEqual(svg.tag, '{http://www.w3.org/2000/svg}svg')
        self.assertTrue(svg.findall('.//{http://www.w3.org/2000/svg}path'))
        self.assertFalse(svg.findall('.//{http://www.w3.org/2000/svg}image'))
        self.assertTrue(outputs['pdf'].read_bytes().startswith(b'%PDF-'))
        from PIL import Image
        with Image.open(outputs['png']) as image:
            self.assertEqual(image.size, (256, 256))
        reopened = self.root / 'reopened.vectorcraft'
        self.cli('convert', self.project, reopened)
        self.assertEqual(self.object(reopened, self.icon), self.object(self.project, self.icon))


if __name__ == '__main__':
    unittest.main()
