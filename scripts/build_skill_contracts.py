#!/usr/bin/env python3
"""生成各独立技能的操作合同及宿主调用策略；--check 不写文件。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(check=False):
    suite = json.loads((ROOT/'skill-suite.json').read_text())
    manifest = json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
    if suite['version'] != manifest['version']:
        raise ValueError('source_manifest_version_drift')
    drift = []
    for entry in suite['skills']:
        root = ROOT/'skills'/entry['name']
        suffix = entry['name'].removeprefix('vectorcraft-cli-')
        create, revise = 'brand-token-assets.json', 'operation-revise.json'
        if suffix in ('shapes', 'paths', 'project'):
            create, revise = 'object-layout-create.json', 'object-layout-revise.json'
        elif suffix == 'selection':
            create, revise = 'selection-brand-create.json', 'selection-brand-revise.json'
        elif suffix == 'appearance':
            create, revise = 'appearance-gradient-create.json', 'appearance-gradient-revise.json'
        contract = {
            'schema': 'vectorcraft-skill-operation-contract/v1', 'skill': entry['name'],
            'kind': entry['kind'], 'purpose': entry['description'],
            'inputs': ['已确认的任务与授权范围', '源工程与素材摘要（返工必须绑定当前版本）', '新输出目录及目标对象／画板'],
            'preconditions': ['Python 3.11+；当前固定平台 macOS arm64',
                '本技能 runtime.lock.json 与实际二进制版本／摘要一致',
                '同一会话实时 enabled、活动选择、锁定／隐藏状态与真实对象回执',
                '文档单位与坐标明确；artboard 从0、range从1，不以预览像素推断几何'],
            'sideEffects': ['安装缺失的锁定运行时到声明目录', '在新暂存工程内执行已授权修改及另存导出；不覆盖源交付'],
            'results': ['原生 .vectorcraft、依赖、导出及摘要清单', '重开与逐步原生回执；交换损失和实际验收状态分别记录'],
            'recovery': ['前置错误不安装／不创建输出', '副作用后unknown保留原位置工程、调用与检查点；先核验再决定继续，不重放'],
            'acceptance': ['目标对象／字段达到请求值，非目标对象与画板保持', '原生重开、字体素材、导出范围／解码及相关像素检查', '目录与计划check仅证明静态结构；创作质量单独评审'],
            'references': ['references/business-scenes.md', 'references/command-usage.md'],
            'examples': {} if entry['kind']=='setup' else {
                'create': {'path':'examples/'+create, 'format': 'craft-command-plan/v1' if 'reopen' in create or 'layout' in create or 'selection' in create else 'vectorcraft-workflow'},
                'revise': {'path':'examples/'+revise, 'format': 'craft-command-plan/v1' if revise in ('object-layout-revise.json','selection-brand-revise.json') else 'vectorcraft-workflow',
                           'requires': '来自当前创建回执的源工程摘要；完整命令返工用 --input project=工程路径 --input target=对象JSON，其中target.id必须来自当前原生回执；不能把示例当作真实对象身份'},
            },
            'hostPolicy': {'allowImplicitInvocation': entry['kind']=='router', 'scope':'支持agents/openai.yaml的宿主；其他宿主记录不适用，显式调用始终可用'},
        }
        if entry['kind']=='setup':
            contract['sideEffects'] = ['仅检查／安装锁定运行时；不创建或编辑用户工程']
            contract['results'] = ['executable、版本、摘要、安装或依赖诊断回执']
            contract['acceptance'] = ['安装来源、摘要、实际版本与复用检查；不声称创作完成']
        files = {
            root/'references/operation-contract.json': json.dumps(contract, ensure_ascii=False, indent=2)+'\n',
            root/'agents/openai.yaml': 'policy:\n  allow_implicit_invocation: '+str(entry['kind']=='router').lower()+'\n',
        }
        for path, content in files.items():
            if check:
                if not path.is_file() or path.read_text() != content:
                    drift.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if drift:
        raise ValueError('operation_contract_drift: '+', '.join(drift))
    print(json.dumps({'skills':len(suite['skills']), 'check':check}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
