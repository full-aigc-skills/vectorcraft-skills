"""计划边界和对象引用测试，不需要安装原生 CLI。"""
import importlib.util
from pathlib import Path
import unittest
import json
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / 'skills/vectorcraft-use/scripts/workflow.py'

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('workflow', SOURCE)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_resolve_only_explicit_references(self):
        value = {'ids': [{'$ref': 'logo.id'}], 'text': 'logo.id'}
        self.assertEqual(self.module.resolve(value, {'logo': {'id': 12}}), {'ids': [12], 'text': 'logo.id'})

    def test_unknown_reference_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'unresolved_reference'):
            self.module.resolve({'$ref': 'missing.id'}, {})

    def test_file_side_effect_commands_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsupported_command'):
            self.module.validate({'operations': [{'command': 'document.save', 'params': {'path': '/outside'}}]})

    def test_brand_revision_rejects_untrusted_export_plan_before_runtime(self):
        for mode in ('modified', 'symlink'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source = root / 'source'
                source.mkdir()
                project = source / 'project.vectorcraft'
                project.write_bytes(b'project fixture')
                original = json.dumps({'exports': [{'format': 'png', 'artboard': 0}]})
                plan_path = source / 'plan.json'
                plan_path.write_text(original)
                manifest = {'files': {'project.vectorcraft': self.module.sha(project), 'plan.json': self.module.sha(plan_path)}, 'bindings': {}}
                (source / 'manifest.json').write_text(json.dumps(manifest))
                if mode == 'modified':
                    plan_path.write_text('{}')
                else:
                    external = root / 'external.json'
                    external.write_text(original)
                    plan_path.unlink()
                    plan_path.symlink_to(external)
                revision = {'expectedProjectSha256': manifest['files']['project.vectorcraft'], 'operations': [{'command': 'swatch.edit', 'params': {'name': 'Brand Primary', 'color': '#175cce'}}]}
                output = root / 'revision'
                runtime = root / 'runtime'
                with self.assertRaisesRegex(ValueError, 'brand_source_plan_digest_mismatch'):
                    self.module.execute(revision, output, source=source, runtime_home=runtime)
                self.assertFalse(output.exists())
                self.assertFalse(runtime.exists())
                self.assertEqual(project.read_bytes(), b'project fixture')

    def test_duplicate_alias_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate_alias'):
            self.module.validate({'operations': [{'command': 'shape.rectangle', 'as': 'logo'}, {'command': 'shape.ellipse', 'as': 'logo'}]})

    def test_export_range_and_format_rejected(self):
        for output in [{'format': 'exe', 'artboard': 0}, {'format': 'png', 'artboard': -1}]:
            with self.assertRaises(ValueError):
                self.module.validate({'operations': [], 'exports': [output]})

if __name__ == '__main__':
    unittest.main()
