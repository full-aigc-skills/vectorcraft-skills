"""素材替换仅允许登记消费者子树变化；重排和非消费者误改必须拒绝。"""
import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def fixture():
 return {'artboards':[{'id':10,'width':96,'height':80}], 'layers':[{'id':1,'kind':{'type':'layer','children':[
  {'id':2,'name':'Logo','kind':{'type':'image','width':12,'height':8,'key':'old'}},
  {'id':3,'name':'Control','kind':{'type':'path','path':'original'}}]}}]}
def inspected(ids):
 return {'layers':[{'id':i,'bounds':{'x':12,'y':16,'width':60,'height':40}} for i in ids]}
class BrandAssetDependenciesTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('asset_dependencies',ROOT/'skills/vectorcraft-use/scripts/brand_variants.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def check(self,before,after,mapping,bounds_after=None):
  return self.m.inspect_asset_update(before,after,'Logo',mapping,inspected(mapping),bounds_after or inspected([i for ids in mapping.values() for i in ids]))
 def test_raster_identity_retained_and_explicit_dependency_recorded(self):
  before=fixture();after=copy.deepcopy(before);after['layers'][0]['kind']['children'][0]['kind']['key']='new'
  row=self.check(before,after,{2:[2]});self.assertEqual(row['status'],'passed');self.assertEqual(row['consumerIds'],[2]);self.assertEqual(row['replacementIds'],[2]);self.assertEqual(row['asset'],'Logo')
 def test_vector_subtree_identity_can_change_without_touching_control(self):
  before=fixture();before['layers'][0]['kind']['children'][0]={'id':2,'kind':{'type':'group','children':[{'id':4,'kind':{'type':'path','path':'old'}}]}}
  after=copy.deepcopy(before);after['layers'][0]['kind']['children'][0]={'id':5,'kind':{'type':'group','children':[{'id':6,'kind':{'type':'path','path':'new'}}]}}
  self.assertEqual(self.check(before,after,{2:[5]})['status'],'passed')
 def test_unrelated_properties_and_new_objects_are_refused(self):
  for fault in ['property','new-object','missing-object','root-order','child-order','artboard']:
   with self.subTest(fault=fault):
    before=fixture();after=copy.deepcopy(before)
    if fault=='property':after['layers'][0]['kind']['children'][1]['name']='changed'
    elif fault=='new-object':after['layers'][0]['kind']['children'].append({'id':4,'kind':{'type':'path'}})
    elif fault=='missing-object':after['layers'][0]['kind']['children'].pop()
    elif fault=='root-order':after['layers'].append({'id':5,'kind':{'type':'layer','children':[]}})
    elif fault=='child-order':after['layers'][0]['kind']['children'].reverse()
    else:after['artboards'][0]['width']=100
    row=self.check(before,after,{2:[2]});self.assertEqual(row['status'],'failed');self.assertTrue(row['unexpectedDependencies'] or row['artboardsChanged'])
 def test_instance_bounds_change_is_not_hidden_by_valid_mapping(self):
  before=fixture();after=copy.deepcopy(before);bounds=inspected([2]);bounds['layers'][0]['bounds']['width']=30
  row=self.check(before,after,{2:[2]},bounds);self.assertEqual(row['status'],'failed');self.assertEqual(row['boundsMismatchObjectIds'],[2])
 def test_unknown_overlapping_and_unbound_targets_refused(self):
  for mapping in [{99:[2]},{2:[3]},{2:[]},{2:[2,2]},{2:[99]},{}]:
   with self.subTest(mapping=mapping),self.assertRaisesRegex(ValueError,'asset_dependency_mapping'):
    self.check(fixture(),fixture(),mapping)
 def test_replacement_cannot_reparent_an_unrelated_object(self):
  before=fixture();after=copy.deepcopy(before);control=after['layers'][0]['kind']['children'].pop();after['layers'][0]['kind']['children'][0]={'id':5,'kind':{'type':'group','children':[control]}}
  with self.assertRaisesRegex(ValueError,'asset_dependency_mapping'):self.check(before,after,{2:[5]})
if __name__=='__main__':unittest.main()
