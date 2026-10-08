"""血缘必须支持移动重关联，并拒绝重签文件表后的语义错配。"""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def module():
    spec=importlib.util.spec_from_file_location('lineage',ROOT/'skills/vectorcraft-use/scripts/exchange_loss.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class ArtifactLineageTests(unittest.TestCase):
    def fixture(self,root):
        for name,data in {'project.vectorcraft':b'native','plan.json':b'{}','art.svg':b'<svg/>','assets/logo.svg':b'<svg/>'}.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        m=module()
        return {'files':{p.relative_to(root).as_posix():m.sha(p) for p in root.rglob('*') if p.is_file()},'outputs':[{'path':'art.svg'}],
                'assets':{'logo':{'path':'assets/logo.svg','sha256':m.sha(root/'assets/logo.svg')}},'sourceProjectSha256':None}
    def test_move_preserves_identity_and_all_dependencies(self):
        m=module()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'original';root.mkdir();manifest=self.fixture(root)
            result=m.write_lineage(root,manifest,'execution-1')
            moved=Path(d)/'moved package';shutil.move(root,moved)
            self.assertEqual(m.verify_lineage(moved,manifest),result)
            self.assertEqual(result['sourceTask']['id'],'execution-1')
            self.assertEqual(result['assets']['logo']['path'],'assets/logo.svg')
    def test_revision_retains_logical_id_and_parent_version(self):
        m=module()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest=self.fixture(root);old=m.write_lineage(root,manifest,'first')
            (root/'art.svg').write_text('<svg><path/></svg>');manifest['files']['art.svg']=m.sha(root/'art.svg')
            manifest['files'].pop('lineage.json');manifest['sourceProjectSha256']=old['native']['sha256']
            new=m.write_lineage(root,manifest,'second',old)
            self.assertEqual(new['logicalId'],old['logicalId']);self.assertNotEqual(new['version'],old['version'])
            self.assertEqual(new['parent']['version'],old['version']);m.verify_lineage(root,manifest)
    def test_file_replacement_invalidates_without_renaming(self):
        m=module()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest=self.fixture(root);m.write_lineage(root,manifest,'task')
            (root/'art.svg').write_text('replaced')
            with self.assertRaisesRegex(ValueError,'lineage'):m.verify_lineage(root,manifest)
    def test_rehashed_missing_dependency_task_native_or_version_is_rejected(self):
        m=module()
        for fault in ['assets','task','native','version','files']:
            with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
                root=Path(d);manifest=self.fixture(root);r=m.write_lineage(root,manifest,'task')
                if fault=='assets':r['assets']={}
                elif fault=='task':r['sourceTask']['id']=''
                elif fault=='native':r['native']['sha256']='0'*64
                elif fault=='version':r['version']='0'*64
                else:r['files'].pop('art.svg')
                (root/'lineage.json').write_text(json.dumps(r));manifest['files']['lineage.json']=m.sha(root/'lineage.json');manifest['lineage']['sha256']=m.sha(root/'lineage.json')
                with self.assertRaisesRegex(ValueError,'lineage'):m.verify_lineage(root,manifest)
    def test_symlink_dependency_is_rejected(self):
        m=module()
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest=self.fixture(root);m.write_lineage(root,manifest,'task')
            asset=root/'assets/logo.svg';asset.unlink();asset.symlink_to(root/'art.svg')
            with self.assertRaisesRegex(ValueError,'lineage'):m.verify_lineage(root,manifest)

if __name__=='__main__':unittest.main()
