"""真实独立子进程与不可信计划边界；合成秘密不代表模型或原生验收。"""
import importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 p=ROOT/'skills/vectorcraft-use/scripts'/(name+'.py');s=importlib.util.spec_from_file_location('security_test_'+name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
FAKE="""import json,os,sys
for line in sys.stdin:
 r=json.loads(line)
 if 'id' not in r:continue
 if r['method']=='initialize':v={'result':{'protocolVersion':'2024-11-05','capabilities':{}}}
 elif r['method']=='fail':v={'error':{'code':-32000,'message':'synthetic-native-error-secret'}}
 else:v={'result':{'isError':False,'content':[{'type':'text','text':json.dumps({'secretPresent':'VECTORCRAFT_TEST_HOST_SECRET' in os.environ,'pathPresent':bool(os.environ.get('PATH'))})}]}}
 print(json.dumps({'jsonrpc':'2.0','id':r['id'],**v}),flush=True)
"""
class InputSecurityTests(unittest.TestCase):
 def test_session_does_not_inherit_host_secret(self):
  with patch.dict(os.environ,{'VECTORCRAFT_TEST_HOST_SECRET':'synthetic-host-secret'}):
   with load('mcp_session').Session([sys.executable,'-I','-B','-u','-c',FAKE]) as s:
    r=json.loads(s.request('inspect',{})['content'][0]['text']);self.assertTrue(r['pathPresent']);self.assertFalse(r['secretPresent'],'actual MCP process inherited host secret')
 def test_untrusted_protocol_error_is_not_echoed(self):
  with load('mcp_session').Session([sys.executable,'-I','-B','-u','-c',FAKE]) as s:
   with self.assertRaises(RuntimeError) as caught:s.request('fail',{})
   self.assertNotIn('synthetic-native-error-secret',str(caught.exception))
 def test_workflow_rejects_literal_credential(self):
  with self.assertRaisesRegex(ValueError,'literal_secret_forbidden'):load('workflow').validate({'operations':[{'command':'text.setText','params':{'ids':[2],'text':'ordinary text','apiKey':'synthetic'}}]})
 def test_complete_gateway_rejects_literal_credential(self):
  with self.assertRaisesRegex(ValueError,'literal_secret_forbidden'):load('commands').validate({'schema':'craft-command-plan/v1','operations':[{'command':'document.json','params':{'clientSecret':'synthetic'}}]})
 def test_successful_reply_with_literal_credentials_is_not_retained(self):
  reply={'content':[{'type':'text','text':json.dumps({'credentials':{'apiKey':'synthetic-result-secret'}})}]}
  with self.assertRaisesRegex(ValueError,'literal_secret_forbidden'):load('commands').parse_reply(reply)
 def test_tool_error_and_semantic_error_hide_untrusted_diagnostics(self):
  m=load('commands')
  for reply in [{'isError':True,'content':[{'type':'text','text':'synthetic-native-error-secret'}]},{'content':[{'type':'text','text':json.dumps({'error':'synthetic-native-error-secret'})}]}]:
   with self.assertRaises(RuntimeError) as caught:m.parse_reply(reply)
   self.assertNotIn('synthetic-native-error-secret',str(caught.exception))
if __name__=='__main__':unittest.main()
