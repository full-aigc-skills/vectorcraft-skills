"""真实公开单技能入口的品牌网关变体继承；显式启用原生下载。"""
import os,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
@unittest.skipUnless(os.environ.get('CRAFT_GATEWAY_EXPORT_NATIVE')=='1','requires public native download and Pillow')
class NativeGatewayExportTests(unittest.TestCase):
 def test_inherited_variants_and_unchanged_controls(self):
  with tempfile.TemporaryDirectory() as t:
   origin=Path(os.environ.get('CRAFT_GATEWAY_EXPORT_SKILL',ROOT/'skills/vectorcraft-cli-export'))
   output=Path(os.environ.get('CRAFT_GATEWAY_EXPORT_OUTPUT',Path(t)/'native-case'))
   args=[sys.executable,'-I','-B',str(ROOT/'tests/fixtures/brand_gateway_case.py'),'--skill',str(origin),'--output',str(output)]
   if os.environ.get('CRAFT_GATEWAY_EXPORT_RUNTIME'):args+=['--runtime-home',os.environ['CRAFT_GATEWAY_EXPORT_RUNTIME']]
   r=subprocess.run(args,capture_output=True,text=True,timeout=300)
   self.assertEqual(r.returncode,0,r.stdout+r.stderr)
if __name__=='__main__':unittest.main()
