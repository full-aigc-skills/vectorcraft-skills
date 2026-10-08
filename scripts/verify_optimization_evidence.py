#!/usr/bin/env python3
"""校验候选证据与当前源码／独立技能摘要；不生成或升级验收结论。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def skill_digest(root):
    """候选安装载荷摘要：与冷启动复制一致，排除本地Python字节码缓存。"""
    files=sorted((p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'),key=lambda p:p.relative_to(root).as_posix())
    if root.is_symlink() or any(p.is_symlink() for p in root.rglob('*')):raise ValueError('linked_skill')
    return hashlib.sha256(''.join(p.relative_to(root).as_posix()+'\0'+sha(p)+'\n' for p in files).encode()).hexdigest()

def verify(root,report):
    errors=[]
    if report.get('result')!='PASS':errors.append('report_not_pass')
    for name,digest in report.get('fingerprints',{}).items():
        path=root/name
        if (not isinstance(name,str) or '\\' in name or Path(name).is_absolute() or any(p in ('','.','..') for p in name.split('/'))
                or not path.resolve().is_relative_to(root.resolve()) or path.is_symlink()):errors.append('invalid: '+name)
        elif not path.is_file() or sha(path)!=digest:errors.append('stale: '+name)
    for name,digest in report.get('skills',{}).items():
        if '/' in name or '\\' in name or name in ('','.','..'):errors.append('invalid_skill: '+name);continue
        try:
            if skill_digest(root/'skills'/name)!=digest:errors.append('stale_skill: '+name)
        except (ValueError,OSError):errors.append('stale_skill: '+name)
    if not report.get('fingerprints'):errors.append('missing_source_fingerprints')
    return errors

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true',required=True);parser.add_argument('--report',default='docs/evidence/permissions-candidate45-20261009.json');args=parser.parse_args()
    report=json.loads((ROOT/args.report).read_text())
    errors=verify(ROOT,report);print(json.dumps({'result':'FAIL' if errors else 'PASS','scope':'current candidate source and skill fingerprint integrity only','errors':errors}));raise SystemExit(bool(errors))
