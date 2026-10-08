"""素材内容必须在可信授权根内读取；计划路径和摘要不能自行授权。"""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16"/></svg>'

def load(name):
    spec = importlib.util.spec_from_file_location('asset_permission_' + name, ROOT / 'skills/vectorcraft-use/scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class AssetReadAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.module = load('asset_inputs')
        self.tmp = tempfile.TemporaryDirectory(prefix='asset authorized roots ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.allowed = self.root / 'allowed'
        self.allowed.mkdir()
        self.outside = self.root / 'outside'
        self.outside.mkdir()
        self.asset = self.allowed / 'logo.svg'
        self.asset.write_bytes(SVG)

    def plan(self, path=None):
        return {'assets': {'logo': {'path': str(path or self.asset), 'sha256': hashlib.sha256(SVG).hexdigest()}},
                'operations': [{'command': 'asset.place', 'params': {'asset': 'logo'}}]}

    def test_metadata_path_and_digest_cannot_authorize_content_read(self):
        with patch.object(self.module, 'sha', side_effect=AssertionError('unauthorized bytes were read')):
            with self.assertRaisesRegex(ValueError, 'asset_read_outside_root'):
                self.module.preflight(self.plan())

    def test_explicit_root_allows_preflight_and_collection(self):
        entries = self.module.preflight(self.plan(), read_roots=[self.allowed])
        stage = self.root / 'stage'
        stage.mkdir()
        result = self.module.collect(entries, stage)
        self.assertEqual((stage / result['logo']['path']).read_bytes(), SVG)
        self.assertEqual(set(result['logo']), {'sha256', 'format', 'path'})

    def test_symlinked_parent_cannot_escape_authorized_root(self):
        external = self.outside / 'logo.svg'
        external.write_bytes(SVG)
        alias = self.allowed / 'alias'
        alias.symlink_to(self.outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'asset_read_outside_root'):
            self.module.preflight(self.plan(alias / 'logo.svg'), read_roots=[self.allowed])

    def test_collection_rejects_same_bytes_under_replaced_file_identity(self):
        entries = self.module.preflight(self.plan(), read_roots=[self.allowed])
        replacement = self.allowed / 'replacement.svg'
        replacement.write_bytes(SVG)
        replacement.replace(self.asset)
        stage = self.root / 'stage'
        stage.mkdir()
        with self.assertRaisesRegex(ValueError, 'asset_input_identity_changed'):
            self.module.collect(entries, stage)
        self.assertFalse((stage / 'Assets/logo.svg').exists())

    def test_collection_rechecks_authority_after_parent_replacement(self):
        entries = self.module.preflight(self.plan(), read_roots=[self.allowed])
        external = self.outside / 'logo.svg'
        external.write_bytes(SVG)
        self.allowed.rename(self.root / 'original')
        self.allowed.symlink_to(self.outside, target_is_directory=True)
        stage = self.root / 'stage'
        stage.mkdir()
        with self.assertRaisesRegex(ValueError, 'asset_read_outside_root'):
            self.module.collect(entries, stage)

    def test_plan_metadata_cannot_supply_root_or_extra_command(self):
        plan = self.plan()
        plan['assets']['logo']['readRoots'] = [str(self.root)]
        plan['assets']['logo']['command'] = 'file.open'
        with self.assertRaisesRegex(ValueError, 'asset_record_invalid'):
            self.module.preflight(plan, read_roots=[self.allowed])


class AssetDescriptorTests(unittest.TestCase):
    setUp = AssetReadAuthorizationTests.setUp
    plan = AssetReadAuthorizationTests.plan
    def test_link_swap_between_resolution_and_open_is_refused_before_bytes(self):
        reader = self.module._reader
        roots = reader.normalize_roots([self.allowed])
        (self.outside / 'logo.svg').write_bytes(SVG)
        original_open = reader.os.open
        def swapped(component, *args, **kwargs):
            if component == 'allowed':
                self.allowed.rename(self.root / 'original')
                self.allowed.symlink_to(self.outside, target_is_directory=True)
            return original_open(component, *args, **kwargs)
        with patch.object(reader.os, 'open', side_effect=swapped), patch.object(reader.os, 'read', side_effect=AssertionError('outside bytes were read')):
            with self.assertRaisesRegex(ValueError, 'asset_path_invalid'):
                reader.read_authorized(self.asset, roots)

    def test_non_regular_file_is_refused_without_blocking(self):
        import os
        fifo = self.allowed / 'input.pipe'
        os.mkfifo(fifo)
        with self.assertRaisesRegex(ValueError, 'asset_path_invalid'):
            self.module._reader.read_authorized(fifo, self.module._reader.normalize_roots([self.allowed]))

    def test_invalid_root_shapes_are_refused(self):
        for roots in ['/', [None], ['relative'], ['/tmp/new\nroot']]:
            with self.subTest(roots=roots), self.assertRaisesRegex(ValueError, 'asset_read_roots_invalid'):
                self.module.preflight(self.plan(), read_roots=roots)

class RegisteredCommandInputTests(unittest.TestCase):
    def test_registered_path_swap_cannot_copy_outside_bytes_into_failure_output(self):
        commands = load('commands')
        with tempfile.TemporaryDirectory(prefix='registered command scope ') as temporary:
            root = Path(temporary)
            source = root / 'authorized.svg'
            source.write_bytes(SVG)
            outside = root / 'outside.svg'
            sentinel = b'<svg>synthetic outside content must not be copied</svg>'
            outside.write_bytes(sentinel)
            output = root / 'output'
            def installer(*args):
                source.unlink()
                source.symlink_to(outside)
                return {'executable': '/never-launched-cli', 'binarySha256': '0' * 64}
            plan = {'schema': 'craft-command-plan/v1', 'operations': [{'command': 'file.open', 'params': {'path': {'$ref': 'source.path'}}}]}
            result = commands.execute(plan, output, installer=installer, inputs={'source': source})
            self.assertEqual(result['result'], 'FAIL')
            copied = output / 'inputs/source.svg'
            self.assertFalse(copied.exists(), 'unauthorized outside bytes reached the failure output')

class WorkflowAssetAuthorizationTests(unittest.TestCase):
    setUp = AssetReadAuthorizationTests.setUp
    plan = AssetReadAuthorizationTests.plan

    def test_untrusted_plan_roots_do_not_grant_authority_or_install_runtime(self):
        workflow = load('workflow')
        plan = {**self.plan(), 'document': {'width': 64, 'height': 64}, 'readRoots': [str(self.root)]}
        with self.assertRaisesRegex(ValueError, 'asset_read_outside_root'):
            workflow.execute(plan, self.root / 'delivery', runtime_home=self.root / 'runtime')
        self.assertFalse((self.root / 'runtime').exists())
        self.assertFalse((self.root / 'delivery').exists())

    def test_managed_authorization_roots_override_caller_broadening(self):
        workflow = load('workflow')
        plan = {**self.plan(), 'document': {'width': 64, 'height': 64}}
        class Control:
            expected_plan = plan
            profile = {'authorization': {'readRoots': []}}
            def check(self):
                pass
        with self.assertRaisesRegex(ValueError, 'asset_read_outside_root'):
            workflow.execute(plan, self.root / 'delivery', runtime_home=self.root / 'runtime', control=Control(), read_roots=[self.root])
        self.assertFalse((self.root / 'runtime').exists())

class WorkflowCliAuthorizationTests(unittest.TestCase):
    setUp = AssetReadAuthorizationTests.setUp
    plan = AssetReadAuthorizationTests.plan

    def test_managed_cli_checks_frozen_roots_before_asset_hash(self):
        import json
        import sys
        import time
        workflow = load('workflow')
        plan = {**self.plan(), 'document': {'width': 64, 'height': 64}}
        plan_file = self.root / 'plan.json'
        plan_file.write_text(json.dumps(plan))
        state = self.root / 'state.json'
        state.write_text(json.dumps({'task': 'asset-cli', 'epoch': 1, 'state': 'running'}))
        control = self.root / 'control.json'
        control.write_text(json.dumps({'schema': 'vectorcraft-execution-control/v1', 'task': 'asset-cli',
            'epoch': 1, 'deadline': int(time.time() * 1000) + 60000, 'maxBytes': 1048576,
            'planFile': str(plan_file), 'planHash': hashlib.sha256(plan_file.read_bytes()).hexdigest(),
            'stateFile': str(state), 'authorization': {'readRoots': []}}))
        assets = workflow.asset_module()
        with patch.object(workflow, 'asset_module', return_value=assets), patch.object(assets._reader.os, 'read', side_effect=AssertionError('unauthorized CLI bytes were read')):
            with patch.object(sys, 'argv', ['workflow.py', str(plan_file), '--output', str(self.root / 'delivery'),
                '--control', str(control), '--asset', 'logo=' + str(self.asset)]), self.assertRaises(SystemExit) as result:
                workflow.main()
        self.assertEqual(result.exception.code, 1)
        self.assertFalse((self.root / 'delivery').exists())

    def test_duplicate_cli_bindings_are_refused(self):
        import json
        import sys
        workflow = load('workflow')
        plan_file = self.root / 'plan.json'
        plan_file.write_text(json.dumps({'document': {'width': 64, 'height': 64}, 'operations': []}))
        with patch.object(workflow, 'execute', side_effect=AssertionError('duplicate bindings reached execution')):
            with patch.object(sys, 'argv', ['workflow.py', str(plan_file), '--output', str(self.root / 'delivery'),
                '--asset', 'logo=' + str(self.asset), '--asset', 'logo=' + str(self.asset)]), self.assertRaises(SystemExit) as result:
                workflow.main()
        self.assertEqual(result.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
