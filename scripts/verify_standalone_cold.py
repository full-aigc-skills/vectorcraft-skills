#!/usr/bin/env python3
"""显式验收14候选技能：执行实现收敛在 vectorcraft-harness；领域技能单独复制不再自带脚本，冷安装与命令发现经 harness 入口完成。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def skill_digest(root):
    files=sorted((p for p in root.rglob('*') if p.is_file()),key=lambda p:p.relative_to(root).as_posix())
    return hashlib.sha256(''.join(p.relative_to(root).as_posix()+'\0'+sha(p)+'\n' for p in files).encode()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();suite=json.loads((ROOT/'skill-suite.json').read_text());records=[]
    environment=dict(os.environ,PATH='/usr/bin:/bin')
    for key in ('CRAFT_RUNTIME_HOME','CRAFT_NODE_ARCHIVE','CRAFT_BUNDLE_DIRECTORY','CRAFT_NATIVE_ARCHIVE_DIRECTORY'):
        environment.pop(key,None)
    harness_name=suite['pluginId']+'-harness'
    for entry in suite['skills']:
        with tempfile.TemporaryDirectory(prefix='vectorcraft cold standalone ') as temporary:
            root=Path(temporary);skill=root/'.agents/skills'/entry['name'];shutil.copytree(ROOT/'skills'/entry['name'],skill,ignore=shutil.ignore_patterns('__pycache__'))
            if entry['name']!=harness_name:
                assert not (skill/'scripts').exists(),entry['name']+' must not carry scripts after harness convergence'
            harness=root/'.agents/skills'/harness_name;shutil.copytree(ROOT/'skills'/harness_name,harness,ignore=shutil.ignore_patterns('__pycache__'))
            before=skill_digest(skill);runtime=root/'fresh runtime';assert not runtime.exists()
            def run(*arguments):
                result=subprocess.run([sys.executable,'-I','-B',str(harness/'scripts/cli.py'),'--runtime-home',str(runtime),'--',*arguments],env=environment,capture_output=True,text=True,timeout=240)
                if result.returncode:raise RuntimeError(entry['name']+': '+result.stdout+result.stderr)
                return result.stdout
            version=run('--version').strip();rows=json.loads(run('commands','--json'));assert len(rows)==585
            lock=json.loads((harness/'scripts/runtime.lock.json').read_text());binary=runtime/'vectorcraft'/lock['resolvedVersion']/'vectorcraft-cli'
            assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256']
            assert lock['resolvedVersion'] in version and before==skill_digest(skill)
            records.append({'skill':entry['name'],'skillSha256':before,'version':version,'runtimeSha256':sha(binary),'commandsDiscovered':len(rows),'freshRuntime':True,'spaceInPath':True,'skillUnchanged':True,'executionViaHarness':entry['name']!=harness_name})
            print('PASS',entry['name'],flush=True)
    proof={'schema':'vectorcraft-candidate-standalone-cold/v1','result':'PASS','sourceCandidateVersion':suite['version'],'level':'native-candidate','scope':'14 individually copied candidate skills (execution via vectorcraft-harness; domain skills carry no scripts) and empty native-runtime directories; public locked downloads and 585-command discovery; not fixed plugin installation, host routing or exhaustive execution','driverSha256':sha(Path(__file__)),'cases':records}
    args.output.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
