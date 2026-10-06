"""完整命令外观场景：冷安装、真实渐变/多填色、源修订和无关对象保全。"""
import hashlib,json,os,shutil,subprocess,sys,tempfile,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RecipeContract(unittest.TestCase):
 def test_every_standalone_skill_contains_valid_documented_pair(self):
  rows={r['id']:r for r in json.loads((ROOT/'skills/vectorcraft-use/references/command-coverage.json').read_text())['commands']};ids=set(rows)
  for skill in (ROOT/'skills').iterdir():
   if not (skill/'SKILL.md').is_file():continue
   for name in ['appearance-gradient-create.json','appearance-gradient-revise.json']:
    path=skill/'examples'/name;self.assertTrue(path.is_file(),f'missing public first-use recipe: {path}');plan=json.loads(path.read_text())
    for op in plan['operations']:
     command=op['params']['command'] if op['command']=='native.command' else op['command'];self.assertIn(command,ids);self.assertIn('examples/'+name,rows[command].get('usageRecipes',[]))
   self.assertTrue((skill/'references/appearance-gradient.md').is_file())
   self.assertIn('references/appearance-gradient.md',(skill/'SKILL.md').read_text())
@unittest.skipUnless(os.environ.get('CRAFT_VECTOR_APPEARANCE_FIRST_USE')=='1','explicit public native opt-in')
class AppearanceNativeFirstUse(unittest.TestCase):
 def test_gradient_native_reopening_revision_and_control_preservation(self):
  from PIL import Image
  source=Path(os.environ.get('CRAFT_VECTOR_APPEARANCE_SKILL',ROOT/'skills/vectorcraft-cli-appearance'))
  def files(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
  baseline=files(source)
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary);skill=root/'.agents/skills'/source.name;shutil.copytree(source,skill,ignore=shutil.ignore_patterns('__pycache__'));home=root/'empty-runtime';self.assertFalse(home.exists())
   copied_baseline=files(skill)
   def run(plan,destination,original=None,success=True):
    f=root/(destination.name+'.json');f.write_text(json.dumps(plan));argv=[sys.executable,'-I','-B',str(skill/'scripts/workflow.py'),str(f),'--output',str(destination),'--runtime-home',str(home)]
    if original:argv+=['--source',str(original)]
    result=subprocess.run(argv,env=dict(os.environ,PATH='/usr/bin:/bin'),capture_output=True,text=True,timeout=600)
    if not success:self.assertNotEqual(result.returncode,0);self.assertIn('give both',result.stdout);self.assertFalse((destination/'manifest.json').exists());return None
    self.assertEqual(result.returncode,0,result.stdout+result.stderr);manifest=json.loads((destination/'manifest.json').read_text())
    for f,sha in manifest['files'].items():self.assertEqual(hashlib.sha256((destination/f).read_bytes()).hexdigest(),sha)
    self.assertTrue((destination/'project.vectorcraft').is_file());self.assertTrue((destination/'native.json').is_file());self.assertTrue((destination/'exchange-loss.json').is_file())
    self.assertTrue((destination/'artboard-1.pdf').read_bytes().startswith(b'%PDF-'))
    tree=ET.parse(destination/'artboard-1.svg');self.assertGreaterEqual(len(tree.findall('.//{http://www.w3.org/2000/svg}linearGradient')),1)
    with Image.open(destination/'artboard-1.png') as img:img.load();self.assertEqual(img.size,(128,64))
    return manifest,json.loads((destination/'native.json').read_text())
   plan=json.loads((skill/'examples/appearance-gradient-create.json').read_text());first=root/'original';manifest,native=run(plan,first);original_files=files(first)
   def objects(model):
    result={}
    def visit(node):
     result[node['id']]=node
     for child in node.get('kind',{}).get('children',[]):visit(child)
    for node in model['layers']:visit(node)
    return result
   target=manifest['bindings']['badge']['id'];control=manifest['bindings']['control']['id'];before=objects(native);self.assertEqual(len(before[target]['appearance']['items']),3)
   self.assertEqual(before[target]['appearance']['items'][0]['paint']['type'],'gradient');self.assertEqual(before[target]['appearance']['items'][2]['paint']['type'],'solid')
   with Image.open(first/'artboard-1.png') as img:
    image=img.convert('RGBA');left=image.getpixel((16,32));right=image.getpixel((52,32));control_pixels=image.crop((82,16,114,48)).tobytes();self.assertNotEqual(left,right)
   revision=json.loads((skill/'examples/appearance-gradient-revise.json').read_text());revision['expectedProjectSha256']=manifest['files']['project.vectorcraft'];second=root/'revised';updated,new_native=run(revision,second,first);after=objects(new_native)
   self.assertEqual(before[control],after[control]);self.assertEqual(before[target]['kind'],after[target]['kind']);self.assertEqual(set(before),set(after));self.assertEqual(len(after[target]['appearance']['items']),3)
   self.assertNotEqual(before[target]['appearance']['items'][0]['paint'],after[target]['appearance']['items'][0]['paint']);self.assertEqual(before[target]['appearance']['items'][2],after[target]['appearance']['items'][2])
   self.assertEqual(original_files,files(first));self.assertNotEqual(manifest['files']['project.vectorcraft'],updated['files']['project.vectorcraft'])
   with Image.open(second/'artboard-1.png') as img:
    image=img.convert('RGBA');self.assertNotEqual(left,image.getpixel((16,32)));self.assertEqual(control_pixels,image.crop((82,16,114,48)).tobytes())
   bad=json.loads(json.dumps(revision));bad['operations']=[{'command':'select.set','params':{'ids':[{'$ref':'badge.id'}]}},{'command':'native.command','params':{'command':'paint.setGradientGeom','params':{'ids':[{'$ref':'badge.id'}],'item':0,'start':[8,8]}}}];run(bad,root/'rejected',first,False);self.assertEqual(original_files,files(first))
   self.assertEqual(baseline,files(source));self.assertEqual(files(skill),copied_baseline);self.assertFalse(list(skill.rglob('*.pyc')))
   if os.environ.get('CRAFT_VECTOR_APPEARANCE_REPORT'):
    Path(os.environ['CRAFT_VECTOR_APPEARANCE_REPORT']).write_text(json.dumps({'schema':'vectorcraft-native-appearance-first-use/v1','result':'PASS','skill':source.name,'nativeProjectSha256':manifest['files']['project.vectorcraft'],'revisionSha256':updated['files']['project.vectorcraft'],'originalPreserved':True,'controlNodeAndPixelsUnchanged':True,'geometryAndIdsUnchanged':True,'threeAppearanceItemsPreserved':True,'gradientSwatchRevisionPersisted':True,'svgGradientObserved':True,'png128x64Decoded':True,'pdfHeaderObserved':True,'invalidGradientRejected':True,'skillIdentityUnchanged':True,'scope':'native gradient/multiple-fill sample; no exhaustive command, GUI, PDF visual equivalence or fullV1 acceptance'},indent=2)+'\n')
