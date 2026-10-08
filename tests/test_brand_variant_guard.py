"""品牌依赖守卫：以原生对象关系识别错误更新，不按颜色推断依赖。"""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    paint = {'color': '#2366e8', 'swatch': 'Brand Primary', 'type': 'solid'}
    return {'layers': [{'id': 1, 'kind': {'type': 'layer', 'children': [
        {'id': 2, 'kind': {'type': 'path', 'path': {'closed': True}}, 'paint': paint},
        {'id': 3, 'kind': {'type': 'path'}, 'paint': {'color': '#2366e8', 'type': 'solid'}},
        {'id': 4, 'kind': {'type': 'text', 'runs': [{'style': {'fill': copy.deepcopy(paint)}, 'text': 'NOVA'}]}}
    ]}}], 'artboards': [{'id': 10, 'rect': [0, 0, 256, 256]}]}


class BrandVariantGuardTests(unittest.TestCase):
    def setUp(self):
        path = ROOT/'skills/vectorcraft-use/scripts/brand_variants.py'
        spec = importlib.util.spec_from_file_location('brand_variants_test', path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_linked_shapes_and_text_only_change(self):
        before = fixture(); after = copy.deepcopy(before)
        after['layers'][0]['kind']['children'][0]['paint']['color'] = '#175cce'
        after['layers'][0]['kind']['children'][2]['kind']['runs'][0]['style']['fill']['color'] = '#175cce'
        report = self.module.inspect_update(before, after, 'Brand Primary')
        self.assertEqual(report['status'], 'passed')
        self.assertEqual(report['consumerIds'], [2, 4])
        self.assertEqual(report['affectedObjectIds'], [])

    def test_same_rgb_nonconsumer_changes_report_wrong_edge(self):
        before = fixture(); after = copy.deepcopy(before)
        after['layers'][0]['kind']['children'][1]['paint']['color'] = '#175cce'
        report = self.module.inspect_update(before, after, 'Brand Primary')
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['affectedObjectIds'], [3])
        self.assertEqual(report['unexpectedDependencies'], [{'token': 'Brand Primary', 'objectId': 3,
                                                            'reason': 'unbound_object_changed'}])

    def test_new_deleted_objects_and_container_property_changes_rejected(self):
        before = fixture()
        for mode, expected in [('new', [1, 8]), ('delete', [1, 3]), ('container', [1])]:
            with self.subTest(mode=mode):
                after = copy.deepcopy(before)
                children = after['layers'][0]['kind']['children']
                if mode == 'new': children.append({'id': 8, 'kind': {'type': 'path'}})
                if mode == 'delete': children.pop(1)
                if mode == 'container': after['layers'][0]['name'] = 'Unexpected rename'
                report = self.module.inspect_update(before, after, 'Brand Primary')
                self.assertEqual(report['status'], 'failed')
                self.assertEqual(report['affectedObjectIds'], expected)

    def test_artboard_change_rejected(self):
        before = fixture(); after = copy.deepcopy(before)
        after['artboards'][0]['rect'] = [0, 0, 512, 512]
        report = self.module.inspect_update(before, after, 'Brand Primary')
        self.assertEqual(report['status'], 'failed')
        self.assertTrue(report['artboardsChanged'])

    def test_consumer_container_cannot_reorder_children(self):
        before = fixture(); before['layers'][0]['paint'] = {'swatch': 'Brand Primary'}
        after = copy.deepcopy(before)
        after['layers'][0]['kind']['children'].reverse()
        report = self.module.inspect_update(before, after, 'Brand Primary')
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['affectedObjectIds'], [1])

    def test_duplicate_or_invalid_native_id_fails_closed(self):
        for invalid in [True, 2, None]:
            before = fixture(); before['layers'][0]['kind']['children'][1]['id'] = invalid
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, 'invalid_brand_snapshot'):
                self.module.inspect_update(before, before, 'Brand Primary')

    def test_consumer_deleted_is_not_a_legal_color_update(self):
        before = fixture(); after = copy.deepcopy(before)
        after['layers'][0]['kind']['children'].pop(0)
        report = self.module.inspect_update(before, after, 'Brand Primary')
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['affectedObjectIds'], [1, 2])


if __name__ == '__main__':
    unittest.main()
