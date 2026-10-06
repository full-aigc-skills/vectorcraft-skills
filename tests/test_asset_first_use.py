"""公开单素材技能冷安装、链接迁移与栅格／矢量定点替换。"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(os.environ.get('CRAFT_INSTALLED_VECTOR_ASSET_SKILL', ROOT/'skills/vectorcraft-cli-assets'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def files(root):
    return {str(p.relative_to(root)): digest(p) for p in Path(root).rglob('*') if p.is_file()}


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


@unittest.skipUnless(os.environ.get('CRAFT_VECTOR_ASSET_FIRST_USE') == '1', 'explicit public native cold-install acceptance')
class AssetFirstUse(unittest.TestCase):
    def test_copied_alone_assets_move_and_targeted_replacements(self):
        from PIL import Image
        with tempfile.TemporaryDirectory(prefix='vector-assets-first-use-') as temporary:
            root = Path(temporary)
            skill = root/'single-skill'
            shutil.copytree(SKILL, skill)
            installed_before = files(SKILL); skill_before = files(skill)
            source = root/'provided'; source.mkdir()
            Image.new('RGB', (32, 24), '#ed3412').save(source/'product.png')
            Image.new('RGB', (64, 48), '#175cce').save(source/'new.jpg', quality=100)
            (source/'logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><rect width="24" height="24" fill="#ed3412"/></svg>')
            (source/'new.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><rect width="24" height="24" fill="#175cce"/></svg>')
            provided_before = files(source)
            runtime = root/'empty-runtime'
            def run(plan, name, assets=None, prior=None):
                path = root/(name+'.json');path.write_text(json.dumps(plan))
                output = root/name
                argv = [sys.executable, '-I', '-B', str(skill/'scripts/workflow.py'), str(path), '--output', str(output), '--runtime-home', str(runtime)]
                for alias, location in (assets or {}).items():
                    argv += ['--asset', alias+'='+str(source/location)]
                if prior:
                    argv += ['--source', str(prior)]
                result = subprocess.run(argv, text=True, capture_output=True, timeout=180, env={**os.environ, 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin'})
                self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                return output, json.loads(result.stdout)
            plan = {'document': {'name': 'Registered assets', 'width': 120, 'height': 120}, 'operations': [
                {'command': 'asset.place', 'params': {'asset': 'product', 'rect': [8, 8, 32, 24]}, 'as': 'productObject'},
                {'command': 'asset.place', 'params': {'asset': 'logo', 'rect': [60, 8, 24, 24]}, 'as': 'logoObject'},
                {'command': 'asset.place', 'params': {'asset': 'product', 'rect': [8, 45, 32, 24]}, 'as': 'productVariant'},
                {'command': 'asset.place', 'params': {'asset': 'logo', 'rect': [60, 45, 24, 24]}, 'as': 'logoVariant'},
                {'command': 'asset.place', 'params': {'asset': 'embedded', 'rect': [8, 85, 32, 24], 'link': False}, 'as': 'embeddedObject'},
                {'command': 'shape.rectangle', 'params': {'x': 90, 'y': 50, 'width': 15, 'height': 15, 'fill': '#21c563'}, 'as': 'unrelated'}],
                'exports': [{'format': 'png'}, {'format': 'svg'}, {'format': 'pdf'}]}
            first, manifest = run(plan, 'first', {'product': 'product.png', 'logo': 'logo.svg', 'embedded': 'product.png'})
            self.assertTrue(manifest['assets']['product']['linked'])
            self.assertFalse(manifest['assets']['logo']['linked'])
            self.assertFalse(manifest['assets']['embedded']['linked'])
            self.assertEqual(len(manifest['assets']['product']['ids']), 2)
            self.assertEqual(len(manifest['assets']['logo']['ids']), 2)
            for entry in manifest['assets'].values():
                self.assertEqual(manifest['files'][entry['path']], entry['sha256'])
            self.assertEqual(Image.open(first/'artboard-1.png').convert('RGB').getpixel((20, 20)), (237, 52, 18))
            moved = root/'moved';shutil.copytree(first, moved)
            before = files(first); moved_before = files(moved)
            old_model = objects(json.loads((first/'native.json').read_text()))
            revision = {'expectedProjectSha256': manifest['files']['project.vectorcraft'], 'operations': [
                {'command': 'asset.replace', 'params': {'asset': 'product', 'replacement': 'replacement'}},
                {'command': 'asset.replace', 'params': {'asset': 'embedded', 'replacement': 'embeddedReplacement'}},
                {'command': 'asset.replace', 'params': {'asset': 'logo', 'replacement': 'newLogo'}}], 'exports': plan['exports']}
            revised, updated = run(revision, 'revised', {'replacement': 'new.jpg', 'newLogo': 'new.svg', 'embeddedReplacement': 'new.jpg'}, moved)
            self.assertEqual(updated['assets']['product']['ids'], manifest['assets']['product']['ids'])
            self.assertEqual(updated['assets']['embedded']['ids'], manifest['assets']['embedded']['ids'])
            self.assertFalse(updated['assets']['embedded']['linked'])
            self.assertNotEqual(updated['assets']['logo']['ids'], manifest['assets']['logo']['ids'])
            new_model = objects(json.loads((revised/'native.json').read_text()))
            unrelated = manifest['bindings']['unrelated']['id']
            self.assertEqual(new_model[unrelated], old_model[unrelated])
            pixel = Image.open(revised/'artboard-1.png').convert('RGB')
            self.assertTrue(all(abs(a-b)<=2 for a,b in zip(pixel.getpixel((20,20)), (23,92,206))))
            self.assertEqual(pixel.getpixel((70,20)), (23,92,206))
            self.assertEqual(pixel.getpixel((70,55)), (23,92,206))
            self.assertTrue(all(abs(a-b)<=2 for a,b in zip(pixel.getpixel((20,55)), (23,92,206))))
            self.assertTrue(all(abs(a-b)<=2 for a,b in zip(pixel.getpixel((20,95)), (23,92,206))))
            self.assertEqual(Image.open(first/'artboard-1.png').convert('RGB').getpixel((95,55)), pixel.getpixel((95,55)))
            relocated = root/'relocated';shutil.copytree(revised, relocated)
            # 原暂存路径已删除；直接从迁移交付打开，不借工作流重链接掩盖缺失。
            cli = next(runtime.glob('vectorcraft/*/vectorcraft-cli'))
            sys.path.insert(0, str(skill/'scripts'))
            from mcp_session import Session
            with Session([str(cli), 'mcp', '--headless']) as session:
                session.command('document.open', {'path': str(relocated/'project.vectorcraft')})
                checked = session.command('links.check', {})
                self.assertEqual((checked['missing'], checked['modified']), (0, 0))
                session.command('document.export', {'path': str(root/'relocated.png'), 'format': 'png', 'artboard': 0})
            self.assertEqual(Image.open(root/'relocated.png').convert('RGB').tobytes(), pixel.tobytes())
            self.assertEqual(files(first), before);self.assertEqual(files(moved), moved_before)
            self.assertEqual(files(source), provided_before);self.assertEqual(files(skill), skill_before);self.assertEqual(files(SKILL), installed_before)
            evidence = {'schema': 'vectorcraft-assets-first-use/v1', 'result': 'passed', 'mode': 'copied-alone skill; empty runtime; default public download', 'runtimeSha256': manifest['runtimeSha256'], 'skillFiles': skill_before, 'inputs': ['linked PNG', 'embedded PNG', 'embedded SVG', 'JPEG replacement retaining link/embed mode', 'SVG replacement'], 'nativeRelocation': checked, 'rasterIdentity': 'retained', 'vectorIdentity': 'replaced', 'unrelatedObjectPreserved': True, 'sourceAndSkillsPreserved': True, 'excluded': ['fixed new plugin release', 'model dispatch', 'GUI', 'complete asset format coverage', 'font portability']}
            # 公开证据不包含测试工作目录。
            evidence['nativeRelocation'] = {'missing': checked['missing'], 'modified': checked['modified'], 'links': len(checked['links'])}
            if os.environ.get('CRAFT_VECTOR_ASSET_EVIDENCE'):
                Path(os.environ['CRAFT_VECTOR_ASSET_EVIDENCE']).write_text(json.dumps(evidence, indent=2)+'\n')


if __name__ == '__main__':
    unittest.main()
