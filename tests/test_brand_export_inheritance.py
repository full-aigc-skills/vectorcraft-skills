"""品牌返工两条入口都在安装前核验并继承原变体导出；显式空列表仍有效。"""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class Observed(Exception):pass
class BrandExportInheritanceTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('inheritance_workflow',ROOT/'skills/vectorcraft-use/scripts/workflow.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def fixture(self,root):
  source=root/'source';source.mkdir();(source/'project.vectorcraft').write_bytes(b'fixed native');previous={'operations':[],'exports':[{'format':'svg','artboard':0},{'format':'png','artboard':0},{'format':'pdf','artboard':0}]};(source/'plan.json').write_text(json.dumps(previous));files={n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in ['project.vectorcraft','plan.json']};(source/'manifest.json').write_text(json.dumps({'files':files,'bindings':{}}));return source,files,previous['exports']
 def revision(self,sha,mode):
  edit={'command':'swatch.edit','params':{'name':'Brand Primary','color':'#175cce'}}
  return {'expectedProjectSha256':sha,'operations':[edit if mode=='direct' else {'command':'native.command','params':edit}]}
 def test_both_entries_inherit_verified_exports_before_installation(self):
  for mode in ['direct','native-gateway']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
    root=Path(t);source,files,exports=self.fixture(root);seen=[]
    def preflight(plan,*args):seen.append(plan);raise Observed()
    module=self.m.asset_module()
    with patch.object(self.m,'asset_module',return_value=module),patch.object(module,'preflight',side_effect=preflight):
     with self.assertRaises(Observed):self.m.execute(self.revision(files['project.vectorcraft'],mode),root/'out',source=source,runtime_home=root/'runtime')
    self.assertEqual(seen[0].get('exports'),exports);self.assertFalse((root/'runtime').exists());self.assertFalse((root/'out').exists())
 def test_both_entries_reject_tampered_prior_plan_before_preflight(self):
  for mode in ['direct','native-gateway']:
   with self.subTest(mode=mode),tempfile.TemporaryDirectory() as t:
    root=Path(t);source,files,exports=self.fixture(root);(source/'plan.json').write_text('{}');module=self.m.asset_module()
    with patch.object(self.m,'asset_module',return_value=module),patch.object(module,'preflight',side_effect=Observed) as preflight:
     with self.assertRaisesRegex(ValueError,'brand_source_plan_digest_mismatch'):self.m.execute(self.revision(files['project.vectorcraft'],mode),root/'out',source=source,runtime_home=root/'runtime')
    preflight.assert_not_called();self.assertFalse((root/'runtime').exists())
 def test_explicit_empty_exports_are_not_replaced_by_inheritance(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);source,files,exports=self.fixture(root);(source/'plan.json').write_text('{}');plan=self.revision(files['project.vectorcraft'],'native-gateway');plan['exports']=[];seen=[];module=self.m.asset_module()
   def preflight(value,*args):seen.append(value);raise Observed()
   with patch.object(self.m,'asset_module',return_value=module),patch.object(module,'preflight',side_effect=preflight):
    with self.assertRaises(Observed):self.m.execute(plan,root/'out',source=source,runtime_home=root/'runtime')
   self.assertEqual(seen[0]['exports'],[])
 def test_asset_replacement_inherits_and_checks_prior_export_plan(self):
  for corrupt in [False,True]:
   with self.subTest(corrupt=corrupt),tempfile.TemporaryDirectory() as t:
    root=Path(t);source,files,exports=self.fixture(root);seen=[];module=self.m.asset_module()
    if corrupt:(source/'plan.json').write_text('{}')
    plan={'expectedProjectSha256':files['project.vectorcraft'],'operations':[{'command':'asset.replace','params':{'asset':'logo','replacement':'newLogo'}}]}
    def preflight(value,*args):seen.append(value);raise Observed()
    with patch.object(self.m,'asset_module',return_value=module),patch.object(module,'preflight',side_effect=preflight):
     if corrupt:
      with self.assertRaisesRegex(ValueError,'brand_source_plan_digest_mismatch'):self.m.execute(plan,root/'out',source=source,runtime_home=root/'runtime')
     else:
      with self.assertRaises(Observed):self.m.execute(plan,root/'out',source=source,runtime_home=root/'runtime')
      self.assertEqual(seen[0].get('exports'),exports)
    self.assertFalse((root/'out').exists());self.assertFalse((root/'runtime').exists())
if __name__=='__main__':unittest.main()
