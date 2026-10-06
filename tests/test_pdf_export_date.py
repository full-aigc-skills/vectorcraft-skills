"""PDF 导出日期绑定原生创建日期或完整性已核验的历史导出记录。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pdf_date_workflow',ROOT/'skills/vectorcraft-use/scripts/workflow.py')
workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)

class PdfExportDateTests(unittest.TestCase):
    def test_native_creation_date_wins_over_current_clock(self):
        result=workflow.pdf_export_date({'metadata':{'created':946684800}})
        self.assertEqual(result['created'],946684800)
        self.assertEqual(result['binding'],'native-document-created')

    def test_missing_native_date_reuses_verified_initial_delivery_date(self):
        with patch('time.time',return_value=1700000000):
            first=workflow.pdf_export_date({'metadata':{}})
        self.assertEqual(first['created'],1700000000)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'pdf-export-date.json';p.write_text(json.dumps(first))
            prior={'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()}}
            with patch('time.time',return_value=1800000000):
                self.assertEqual(workflow.pdf_export_date({'metadata':{}},root,prior),first)
            p.write_text(json.dumps({**first,'created':1800000000}))
            with self.assertRaisesRegex(ValueError,'pdf_date_digest_mismatch'):
                workflow.pdf_export_date({'metadata':{}},root,prior)
            p.unlink()
            with self.assertRaisesRegex(ValueError,'pdf_date_digest_mismatch'):
                workflow.pdf_export_date({'metadata':{}},root,prior)

    def test_invalid_native_timestamp_is_rejected(self):
        for value in (True,'2026-10-06',1.5,2**63):
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'invalid_native_pdf_created'):
                workflow.pdf_export_date({'metadata':{'created':value}})
