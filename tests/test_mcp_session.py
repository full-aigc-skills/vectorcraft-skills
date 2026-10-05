"""用独立子进程验证协议失败与超时不重试。"""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'skills/vectorcraft-use/scripts/mcp_session.py'
FAKE = '''import json,sys,time
from pathlib import Path
for line in sys.stdin:
 request=json.loads(line)
 if 'id' not in request: continue
 with Path(sys.argv[1]).open('a') as f: f.write(request['method']+'\\n')
 if request['method']=='initialize': result={'protocolVersion':'2024-11-05','capabilities':{}}
 elif sys.argv[2]=='timeout': time.sleep(10); continue
 else: result={'isError':True,'content':[{'type':'text','text':'missing object'}]}
 print(json.dumps({'jsonrpc':'2.0','id':request['id'],'result':result}),flush=True)
'''

class SessionTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('session', MODULE)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_tool_error_is_not_a_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'calls'
            with self.module.Session([sys.executable, '-u', '-c', FAKE, str(log), 'error']) as session:
                with self.assertRaisesRegex(RuntimeError, 'command_failed'):
                    session.command('shape.rectangle', {})
            self.assertEqual(log.read_text().splitlines(), ['initialize', 'tools/call'])

    def test_timeout_does_not_repeat_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'calls'
            with self.module.Session([sys.executable, '-u', '-c', FAKE, str(log), 'timeout']) as session:
                session.timeout = 0.1
                with self.assertRaisesRegex(TimeoutError, 'outcome_unknown'):
                    session.command('shape.rectangle', {})
            self.assertEqual(log.read_text().splitlines(), ['initialize', 'tools/call'])

if __name__ == '__main__':
    unittest.main()
