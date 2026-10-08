"""证据对应当前源码；报告存在或自称PASS不够。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class OptimizationEvidenceTests(unittest.TestCase):
    def test_report_and_source_replacement_invalidates_evidence(self):
        spec=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/verify_optimization_evidence.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);(root/'code.py').write_text('original')
            report={'result':'PASS','fingerprints':{'code.py':module.sha(root/'code.py')},'skills':{}}
            self.assertEqual(module.verify(root,report),[])
            (root/'code.py').write_text('replaced')
            self.assertEqual(module.verify(root,report),['stale: code.py'])
            report['result']='NOT_RUN'
            self.assertIn('report_not_pass',module.verify(root,report))

    def test_external_evidence_paths_are_rejected(self):
        spec=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/verify_optimization_evidence.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            self.assertIn('invalid: ../outside.py',module.verify(Path(temporary),{'result':'PASS','fingerprints':{'../outside.py':'0'*64},'skills':{}}))
