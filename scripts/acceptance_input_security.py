#!/usr/bin/env python3
"""实际原生修订与独立重开；不提升为宿主秘密引用或完整权限合同验收。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/vectorcraft-use/scripts'
def load(name):
    spec=importlib.util.spec_from_file_location('permissions_acceptance_'+name,BASE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def obj(model,identifier):
    def walk(value):
        if isinstance(value,dict):
            if value.get('id')==identifier and 'kind' in value:return value
            for child in value.values():
                found=walk(child)
                if found is not None:return found
        elif isinstance(value,list):
            for child in value:
                found=walk(child)
                if found is not None:return found
    found=walk(model)
    if found is None:raise ValueError('native_object_missing')
    return found

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--runtime-home',type=Path,required=True);parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve();source_hash=sha(source/'project.vectorcraft')
    prior=json.loads((source/'native.json').read_text())
    plan={'expectedProjectSha256':source_hash,'operations':[{'command':'paint.setFill','params':{'ids':[2],'color':'#00ff00'}}],
          'exports':[{'format':name,'artboard':0} for name in ['svg','pdf','png']]}
    manifest=load('workflow').execute(plan,args.output,args.runtime_home,source)
    after=json.loads((args.output/'native.json').read_text());target={'type':'solid','color':{'model':'rgb','r':0.0,'g':1.0,'b':0.0}}
    assert obj(after,2)['appearance']['items'][0]['paint']==target
    assert obj(prior,3)==obj(after,3)
    for name,digest in manifest['files'].items():assert sha(args.output/name)==digest
    assert (args.output/'artboard-1.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    assert (args.output/'artboard-1.pdf').read_bytes().startswith(b'%PDF-')
    import xml.etree.ElementTree as ET
    ET.parse(args.output/'artboard-1.svg')
    lock=json.loads((BASE/'runtime.lock.json').read_text());runtime=args.runtime_home/'vectorcraft'/lock['resolvedVersion']/'vectorcraft-cli'
    with load('mcp_session').Session([str(runtime.resolve()),'mcp','--headless']) as session:
        session.command('document.open',{'path':str((args.output/'project.vectorcraft').resolve())})
        reopened=session.command('document.json',{})
        assert obj(reopened,2)['appearance']['items'][0]['paint']==target
        assert obj(reopened,3)==obj(prior,3)
    assert session.process.poll() is not None
    assert sha(source/'project.vectorcraft')==source_hash
    proof={'schema':'vectorcraft-permissions-native-candidate/v1','result':'PASS','level':'native-candidate',
        'sourceCandidateVersion':json.loads((ROOT/'skill-suite.json').read_text())['version'],
        'driverSha256':sha(Path(__file__)),'runtimeSha256':sha(runtime),'sourceProjectSha256':source_hash,
        'sourcePreserved':True,'targetPaint':target,'controlTextPreserved':True,'independentNativeReopen':True,
        'reopenProcessStopped':True,'files':manifest['files'],'exports':[x['format'] for x in manifest['outputs']],
        'scope':'Actual source candidate native revision,three exports and independent reopen under filtered child environments;not host routing,secret-reference resolution,full permission sandbox or fixed plugin qualification'}
    args.report.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','exports':3,'nativeReopen':True}))
if __name__=='__main__':main()
