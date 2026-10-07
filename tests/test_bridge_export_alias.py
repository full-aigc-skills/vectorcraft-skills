"""官方桌面没有 CLI 导出别名时，仍执行经核对的引擎命令并保留漂移门禁。"""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
 p=ROOT/'skills/vectorcraft-use/scripts/commands.py';s=importlib.util.spec_from_file_location('bridge_commands',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class BridgeExportAlias(unittest.TestCase):
 def test_bridge_alias_uses_engine_and_receipt_retains_identity(self):
  m=load();calls=[]
  class Session:
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def request(self,method,params):
    if method=='tools/list':return {'tools':[{'name':n} for n in m.ROUTES[m.DOMAIN][:2]]}
    if params['name']=='list_commands':return {'content':[{'type':'text','text':json.dumps([{**r,'enabled':True} for r in m.catalog()['commands'] if r['id']!='file.export'])}]}
    calls.append(params);return {'content':[{'type':'text','text':'{"written":true}'}]}
  with tempfile.TemporaryDirectory() as td:
   proof=m.execute({'schema':'craft-command-plan/v1','operations':[{'command':'file.export','params':{'format':'svg'}}]},Path(td)/'output',mode='bridge',connect='127.0.0.1:54321',installer=lambda *a:{'executable':'native','binarySha256':'a'*64},session_factory=lambda *a:Session())
   self.assertEqual(proof['result'],'PASS');self.assertEqual(calls[0]['arguments']['command'],'document.export');self.assertEqual(proof['steps'][0]['command'],'file.export');self.assertEqual(proof['steps'][0]['backendCommand'],'document.export')
 def test_other_missing_command_still_rejected(self):
  m=load()
  class Session:
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def request(self,method,params):
    if method=='tools/list':return {'tools':[{'name':n} for n in m.ROUTES[m.DOMAIN][:2]]}
    return {'content':[{'type':'text','text':json.dumps([{**r,'enabled':True} for r in m.catalog()['commands'] if r['id'] not in ('file.export','file.new')])}]}
  with tempfile.TemporaryDirectory() as td:
   proof=m.execute({'schema':'craft-command-plan/v1','operations':[{'command':'file.export','params':{}}]},Path(td)/'output',mode='bridge',connect='127.0.0.1:54321',installer=lambda *a:{'executable':'native','binarySha256':'a'*64},session_factory=lambda *a:Session())
   self.assertEqual(proof['result'],'FAIL');self.assertEqual(proof['steps'],[])
 def test_verified_desktop_place_duplicate_uses_engine_context(self):
  m=load()
  rows=[{'id':'file.place','enabled':False,'params':'engine'}, {'id':'file.place','enabled':True,'ui':True,'params':'dialog'}]
  class Session:
   def request(self,*args):return {'content':[{'type':'text','text':json.dumps(rows)}]}
  actual=m.runtime_rows(Session(),mode='bridge');self.assertEqual(len(actual),1);self.assertFalse(actual[0]['enabled']);self.assertEqual(actual[0]['params'],'engine')
  with self.assertRaisesRegex(RuntimeError,'unexpected_registry'):m.runtime_rows(Session())
 def test_unrecognized_duplicate_keeps_rejection(self):
  m=load()
  class Session:
   def request(self,*args):return {'content':[{'type':'text','text':json.dumps([{'id':'file.new','enabled':True},{'id':'file.new','enabled':True,'ui':True}])}]}
  with self.assertRaisesRegex(RuntimeError,'unexpected_registry'):m.runtime_rows(Session(),mode='bridge')
