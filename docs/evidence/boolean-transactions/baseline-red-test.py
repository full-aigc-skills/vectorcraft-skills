"""布尔事务行为：会话替身仅用于故障注入，不替代真实原生验收。"""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'skills/vectorcraft-use/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location('boolean_test_'+name, SCRIPTS/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def document():
    return {'next_id': 10, 'metadata': {'modified': 1}, 'units': 'Points',
            'layers': [{'id': 1, 'kind': {'type': 'layer', 'children': [
                {'id': i, 'kind': {'type': 'path', 'path': {'subpaths': []}}, 'name': str(i)}
                for i in [2, 3, 4]]}}]}


class Session:
    def __init__(self, mode):
        self.mode = mode
        self.doc = document()
        self.selected = [2, 3]
        self.calls = []
        self.before = copy.deepcopy(self.doc)

    def command(self, command, params=None):
        self.calls.append(command)
        if command == 'document.inspect':
            return {'selection': list(self.selected)}
        if command == 'document.json':
            return copy.deepcopy(self.doc)
        if command == 'document.save':
            Path(params['path']).write_text(json.dumps(self.doc))
            return {'saved': True}
        if command == 'document.open':
            if self.mode == 'restore-fails':
                raise RuntimeError('semantic_error: reopen failed')
            self.doc = json.loads(Path(params['path']).read_text())
            return {'opened': True}
        if command == 'select.set':
            self.selected = params['ids']
            return {}
        raise AssertionError(command)

    def request(self, method, params):
        self.calls.append('mutation')
        children = self.doc['layers'][0]['kind']['children']
        self.doc['layers'][0]['kind']['children'] = [v for v in children if v['id'] not in self.selected]
        if self.mode in ('known-failure', 'restore-fails'):
            raise RuntimeError('semantic_error: deleted then failed')
        if self.mode == 'unknown':
            raise RuntimeError('outcome_unknown: lost reply')
        if self.mode == 'group':
            self.doc['layers'][0]['kind']['children'].insert(0, {'id': 10, 'kind': {'type':'group', 'children': children[:2]}})
            result = {'id': 10}
        elif self.mode == 'empty':
            result = {'ids': []}
        else:
            self.doc['layers'][0]['kind']['children'].insert(0, {'id': 10, 'kind': {'type':'path','path':{'subpaths':[]}}})
            result = {'ids': [10]}
        if self.mode == 'bad-result':
            result = {'ids': [999]}
        if self.mode == 'unselected-drift':
            self.doc['layers'][0]['kind']['children'][-1]['name'] = 'corrupt'
        return {'content':[{'type':'text','text':json.dumps(result)}]}


class BooleanTransactionTests(unittest.TestCase):
    def execute(self, session, stage, command='object.pathfinder.unite'):
        module = load('native_workflow')
        rows = [{**row, 'enabled': True} for row in module.commands.catalog()['commands']]
        with patch.object(module.commands, 'runtime_rows', return_value=rows):
            return module.execute(session, {'command':command,'params':{}}, {}, [], stage)

    def test_known_partial_delete_restores_original_objects_without_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            session = Session('known-failure')
            with self.assertRaisesRegex(RuntimeError, 'non_atomic_operation_defect'):
                self.execute(session, Path(temporary))
            self.assertEqual(session.doc, session.before)
            self.assertEqual(session.calls.count('mutation'), 1)
            self.assertEqual(session.calls.count('document.open'), 1)
            proof = json.loads((Path(temporary)/'boolean-transactions.json').read_text())['operations'][0]
            self.assertEqual(proof['participantIds'], [2,3])
            self.assertEqual(proof['status'], 'restored_after_failure')
            self.assertTrue((Path(temporary)/proof['checkpoint']).is_file())
