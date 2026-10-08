"""固定原生CLI的真实文件读写边界；需显式提供本机运行时及测试工程。"""
import hashlib,importlib.util,json,os,platform,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BINARY=os.environ.get('VECTORCRAFT_PERMISSION_BINARY')
SOURCE=os.environ.get('VECTORCRAFT_PERMISSION_SOURCE')
@unittest.skipUnless(platform.system()=='Darwin' and BINARY and SOURCE,'explicit native permission probe required')
class NativeFilesystemBoundaryTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('native_permission_commands',ROOT/'skills/vectorcraft-use/scripts/commands.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
  self.tmp=tempfile.TemporaryDirectory(prefix='vectorcraft permission roots ');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.project=self.root/'authorized';self.project.mkdir();self.outside=self.root/'outside';self.outside.mkdir();self.seed=self.outside/'seed.vectorcraft';shutil.copyfile(SOURCE,self.seed)
  self.lock=json.loads((ROOT/'skills/vectorcraft-use/scripts/runtime.lock.json').read_text());self.sha=hashlib.sha256(Path(BINARY).read_bytes()).hexdigest();self.assertEqual(self.sha,self.lock['artifacts']['darwin-arm64']['binarySha256'])
 def run_plan(self,operations,inputs=None,alias=False):
  output=self.project/'delivery'
  def installer(*args):
   if alias:(output/'alias.vectorcraft').symlink_to(self.seed)
   return {'executable':BINARY,'binarySha256':self.sha}
  receipt=self.m.execute({'schema':'craft-command-plan/v1','operations':operations},output,installer=installer,inputs=inputs)
  return receipt,output
 def test_loopback_policy_compiles_and_allows_native_discovery(self):
  with self.m.load('mcp_session').Session([BINARY,'mcp','--headless'],filesystem={'ports':[32000]}) as session:
   self.assertTrue(session.request('tools/list',{})['tools'])
 def kernel_session(self):
  # 仅测试绕过Python预检的恶意请求；子进程的内核策略仍然有效。
  session=self.m.load('mcp_session').Session([BINARY,'mcp','--headless'],filesystem={'readRoots':[str(self.project)],'writeRoots':[str(self.project)]})
  session.filesystem=None
  return session
 def test_kernel_denies_outside_read_without_python_precheck(self):
  with self.kernel_session() as session:
   session.command('file.new',{'width':64,'height':64,'units':'Pixels'})
   with self.assertRaisesRegex(RuntimeError,'command_failed'):session.command('file.open',{'path':str(self.seed)})
   self.assertIsNone(session.process.poll())
 def test_kernel_denies_outside_write_without_python_precheck(self):
  escaped=self.outside/'kernel-escaped.vectorcraft'
  with self.kernel_session() as session:
   session.command('file.new',{'width':64,'height':64,'units':'Pixels'})
   with self.assertRaisesRegex(RuntimeError,'command_failed'):session.command('file.save',{'path':str(escaped)})
   self.assertIsNone(session.process.poll())
  self.assertFalse(escaped.exists())
 def test_kernel_denies_symlink_read_without_python_precheck(self):
  alias=self.project/'alias.vectorcraft';alias.symlink_to(self.seed)
  with self.kernel_session() as session:
   with self.assertRaisesRegex(RuntimeError,'command_failed'):session.command('file.open',{'path':str(alias)})
   self.assertIsNone(session.process.poll())
 def test_registered_native_input_is_copied_and_readable(self):
  r,o=self.run_plan([{'command':'file.open','params':{'path':{'$ref':'source.path'}}}],{'source':self.seed});self.assertEqual(r['result'],'PASS',r.get('error'));self.assertTrue((o/'inputs/source.vectorcraft').is_file())
 def test_unregistered_outside_native_input_is_denied(self):
  before=hashlib.sha256(self.seed.read_bytes()).hexdigest();r,o=self.run_plan([{'command':'file.open','params':{'path':str(self.seed)}}]);self.assertEqual(r['result'],'FAIL','native opened an undeclared outside project');self.assertEqual(hashlib.sha256(self.seed.read_bytes()).hexdigest(),before)
 def test_output_placeholder_native_write_is_allowed(self):
  r,o=self.run_plan([{'command':'file.new','params':{'width':64,'height':64,'units':'Pixels'}},{'command':'file.save','params':{'path':{'$output':'authorized.vectorcraft'}}}]);self.assertEqual(r['result'],'PASS',r.get('error'));self.assertTrue((o/'authorized.vectorcraft').is_file())
 def test_raw_outside_native_write_is_denied(self):
  escaped=self.outside/'escaped.vectorcraft';r,o=self.run_plan([{'command':'file.new','params':{'width':64,'height':64,'units':'Pixels'}},{'command':'file.save','params':{'path':str(escaped)}}]);self.assertFalse(escaped.exists(),'native wrote outside the authorized output root');self.assertEqual(r['result'],'FAIL')
 def test_inside_symlink_cannot_grant_outside_native_read(self):
  r,o=self.run_plan([{'command':'file.open','params':{'path':str(self.project/'delivery/alias.vectorcraft')}}],alias=True);self.assertEqual(r['result'],'FAIL','inside symlink exposed an undeclared outside project')
if __name__=='__main__':unittest.main()
