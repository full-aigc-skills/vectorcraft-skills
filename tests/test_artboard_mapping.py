"""稳定画板身份不能被索引变化或重复选择静默替换。"""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module():
 spec=importlib.util.spec_from_file_location('mapping',ROOT/'skills/vectorcraft-use/scripts/artboard_mapping.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class ArtboardMappingTests(unittest.TestCase):
 def setUp(self):
  self.m=module();self.a={'id':11,'name':'Logo','rect':{'x0':0,'y0':0,'x1':128,'y1':96}};self.b={'id':22,'name':'Icon','rect':{'x0':200,'y0':20,'x1':280,'y1':84}};self.native={'artboards':[self.a,self.b]};self.shifted={'artboards':[self.b,self.a]}
 def test_legacy_create_mapping_preserves_zero_based_index(self):
  rows=self.m.resolve_exports([{'format':'png','artboard':1}],self.native,{})
  self.assertEqual(rows[0]['artboardId'],22);self.assertEqual(rows[0]['artboardIndex'],1);self.assertEqual(rows[0]['artboardName'],'Icon');self.assertEqual(rows[0]['artboardRect'],self.b['rect'])
 def test_stable_id_follows_reordered_board(self):
  rows=self.m.resolve_exports([{'format':'svg','artboardId':11}],self.shifted,{},self.native)
  self.assertEqual(rows[0]['artboardIndex'],1);self.assertEqual(rows[0]['artboardId'],11)
 def test_explicit_ref_resolves_runtime_binding(self):
  rows=self.m.resolve_exports([{'format':'pdf','artboardId':{'$ref':'variant.id'}}],self.native,{'variant':{'id':22}})
  self.assertEqual(rows[0]['artboardId'],22)
 def test_legacy_revision_rejects_changed_index_and_identifies_original(self):
  with self.assertRaisesRegex(ValueError,'artboard_mapping_conflict.*11.*22'):self.m.resolve_exports([{'format':'png','artboard':0}],self.shifted,{},self.native)
 def test_index_id_conflict_and_unknown_id_rejected(self):
  for item,error in [({'format':'svg','artboard':0,'artboardId':22},'artboard_mapping_conflict'),({'format':'svg','artboardId':33},'artboard_id_not_found'),({'format':'svg','artboard':2},'artboard_out_of_range')]:
   with self.subTest(item=item),self.assertRaisesRegex(ValueError,error):self.m.resolve_exports([item],self.native,{})
 def test_duplicate_resolved_output_rejected(self):
  with self.assertRaisesRegex(ValueError,'duplicate_export'):self.m.resolve_exports([{'format':'svg','artboard':0},{'format':'svg','artboardId':11}],self.native,{})
 def test_invalid_selector_shape_rejected_before_runtime(self):
  for item in [None,{'format':'svg','artboard':True},{'format':'png','artboardId':True},{'format':'png','artboardId':0},{'format':'png','artboardId':{'$ref':3}},{'format':'png','artboards':[1]}]:
   with self.subTest(item=item),self.assertRaisesRegex(ValueError,'invalid_export'):self.m.validate_exports([item])
 def test_invalid_native_identity_and_geometry_fail_closed(self):
  for boards in [[self.a,self.a],[{**self.a,'id':True}],[{**self.a,'rect':{**self.a['rect'],'x1':float('nan')}}],[{**self.a,'name':None}],[{**self.a,'rect':{**self.a['rect'],'x0':-1e308,'x1':1e308}}]]:
   with self.subTest(boards=boards),self.assertRaisesRegex(ValueError,'invalid_native_artboard'):self.m.snapshot({'artboards':boards})

 def test_new_board_binding_resolves_actual_native_id_from_index_reply(self):
  self.assertEqual(self.m.bind_created({'index':1},self.native),{'index':1,'id':22})
  for reply in [{'index':True},{'index':9},{'index':1,'id':11}]:
   with self.subTest(reply=reply),self.assertRaisesRegex(ValueError,'invalid_artboard_reply'):self.m.bind_created(reply,self.native)
