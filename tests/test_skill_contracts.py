"""十三项独立技能的路由、契约与版本一致性。"""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_source_manifest_and_suite_have_one_version(self):
        suite = json.loads((ROOT/'skill-suite.json').read_text())
        manifest = json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
        self.assertEqual(manifest['version'], suite['version'])

    def test_each_skill_has_self_contained_operation_contract_and_invocation_policy(self):
        suite = json.loads((ROOT/'skill-suite.json').read_text())
        for entry in suite['skills']:
            with self.subTest(skill=entry['name']):
                skill = ROOT/'skills'/entry['name']
                path = skill/'references/operation-contract.json'
                self.assertTrue(path.is_file(), 'missing independently installed operation contract')
                contract = json.loads(path.read_text())
                self.assertEqual(contract['skill'], entry['name'])
                for key in ('inputs', 'preconditions', 'sideEffects', 'results', 'recovery', 'acceptance'):
                    self.assertTrue(contract[key])
                for example in contract['examples'].values():
                    self.assertTrue((skill/example['path']).is_file())
                    script = skill/'scripts'/('commands.py' if example['format']=='craft-command-plan/v1' else 'workflow.py')
                    if script.name == 'commands.py':
                        p = subprocess.run([sys.executable, '-I', '-B', str(script), 'check', str(skill/example['path']), '--input', 'project=source.vectorcraft', '--input', 'target=actual-object.json'], capture_output=True, text=True)
                        self.assertEqual(p.returncode, 0, p.stdout+p.stderr)
                policy = (skill/'agents/openai.yaml').read_text()
                self.assertIn('allow_implicit_invocation: '+str(entry['kind']=='router').lower(), policy)
                self.assertIn('references/operation-contract.json', (skill/'SKILL.md').read_text())
