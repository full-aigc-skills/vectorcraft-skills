"""普通工作流与完整命令入口的严格解析必须具有相同边界。"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/vectorcraft-use/scripts'


def module(name):
    spec = importlib.util.spec_from_file_location('parity_' + name, SCRIPTS / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


SERVER = r'''
import json, sys
from pathlib import Path
for line in sys.stdin:
    r = json.loads(line)
    if 'id' not in r:
        continue
    if r['method'] == 'initialize':
        print(json.dumps({'id': r['id'], 'result': {}}), flush=True)
        continue
    with Path(sys.argv[2]).open('a') as f:
        f.write(line)
    value = sys.argv[1].replace('REQUEST_ID', str(r['id']))
    print(value, flush=True)
'''


class EntryParityTests(unittest.TestCase):
    def test_workflow_plan_rejected_before_install_or_output(self):
        values = ['{"document":{},"document":{}}', '{"value":NaN}',
                  '{"value":Infinity}', '{"value":1e999}',
                  '{"operations":[{"params":{"x":1,"x":2}}]}']
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for text in values:
                with self.subTest(text=text):
                    plan = root / 'plan.json'; plan.write_text(text)
                    result = subprocess.run([sys.executable, '-I', '-B', str(SCRIPTS/'workflow.py'),
                        str(plan), '--output', str(root/'out'), '--runtime-home', str(root/'runtime')],
                        capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertRegex(json.loads(result.stdout)['error'], 'duplicate_json_key|nonfinite_json_value')
                    self.assertFalse((root/'runtime').exists())
                    self.assertFalse((root/'out').exists())

    def test_sent_reply_ambiguity_is_unknown_without_replay(self):
        texts = ['{"id":1,"id":2}', '{"value":NaN}', '{"value":Infinity}', '{"value":1e999}']
        replies = [json.dumps({'id': 'REQUEST_ID', 'result': {'content': [{'type':'text', 'text': t}]}})
                   .replace('"REQUEST_ID"', 'REQUEST_ID') for t in texts]
        replies += ['{"id":REQUEST_ID,"id":REQUEST_ID,"result":{"content":[]}}',
                    '{"id":REQUEST_ID,"result":{"value":1e999}}',
                    '{"id":999,"result":{"content":[]}}',
                    '{"id":REQUEST_ID,"result":{},"error":{"message":"ambiguous"}}',
                    '{"id":REQUEST_ID,"error":null}',
                    '{"id":REQUEST_ID,"error":{"code":true,"message":"bad"}}',
                    '{"id":REQUEST_ID,"error":{"code":-32600,"message":7}}']
        for reply in replies:
            with self.subTest(reply=reply), tempfile.TemporaryDirectory() as temporary:
                log = Path(temporary)/'calls'
                with module('mcp_session').Session([sys.executable, '-I', '-B', '-u', '-c',
                        SERVER, reply, str(log)], timeout=.3) as session:
                    with self.assertRaisesRegex(RuntimeError, 'outcome_unknown'):
                        session.command('document.save', {'path':'unused'})
                self.assertEqual(len(log.read_text().splitlines()), 1)

    def test_native_error_and_business_error_field_are_distinct(self):
        session_type = module('mcp_session').Session
        # 原生 run_command 的失败合同是仅有 error 的信封；对象业务数据可含 error。
        for payload, failed in [({'error':'native edit failed'}, True),
                                ({'id':7, 'error':'a business field'}, False),
                                ({'id':7, 'value':1.5}, False)]:
            reply = json.dumps({'id':'REQUEST_ID', 'result': {'content':[
                {'type':'text', 'text':json.dumps(payload)}]}}).replace('"REQUEST_ID"', 'REQUEST_ID')
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temporary:
                with session_type([sys.executable, '-I', '-B', '-u', '-c', SERVER, reply,
                        str(Path(temporary)/'calls')]) as session:
                    if failed:
                        with self.assertRaisesRegex(RuntimeError, 'semantic_error'):
                            session.command('edit', {})
                    else:
                        self.assertEqual(session.command('query', {}), payload)
                command_reply = {'content':[{'type':'text', 'text':json.dumps(payload)}]}
                if failed:
                    with self.assertRaisesRegex(RuntimeError, 'semantic_error'):
                        module('commands').parse_reply(command_reply)
                else:
                    self.assertEqual(module('commands').parse_reply(command_reply), payload)
