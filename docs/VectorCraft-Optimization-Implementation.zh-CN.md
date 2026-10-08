# VectorCraft 独立技能优化

dev.34 为当前源码候选，固定插件仍消费 dev.33；新代码不自动进入安装副本。本轮补齐普通／完整命令入口的严格 JSON、品牌消费者字段允许清单与请求目标值、13项自包含操作合同、宿主调用策略和源仓CI。

## 维护与验证

```bash
python3 -I -B scripts/build_skill_contracts.py --check
python3 -I -B scripts/build_command_coverage.py --check
python3 -I -B scripts/build_scenario_catalog.py --check
python3 -I -B scripts/sync_skill_suite.py --check
python3 -I -B -m unittest discover -s tests -v
```

公共脚本在 vectorcraft-use 维护并确定性同步；operation-contract.json 按技能独立生成，不被共享参考同步覆盖。仅支持调用策略的宿主使用 agents/openai.yaml：use 默认隐式路由，其余技能显式可用。其他宿主按实际能力记录不适用。

严格 JSON 对计划、协议信封及约定的 JSON 文本拒绝重复键、非有限及溢出。普通文本和图片工具保留原合同；原生仅含 error 的错误信封与合法业务 error 字段分别处理。未知回复不绑定成功引用、不执行后续步骤或重放，失败工程与依赖保留原位置。

品牌改色只允许目标 token 绑定的颜色字段变化；消费者的文字、路径闭合性、几何、透明度和非目标外观仍受保护。检查目标色板与每个绑定字段达到请求值，区分未生效、无消费者与 verified_noop。保留RGB／CMYK／Gray／Lab作者模型及原生tint语义；非RGB模型的单元验证不能冒充其全部原生／跨编辑器验收。导出继承、显式空列表、原计划摘要、PDF日期和无关输出字节合同保持。

技能源码拥有执行行为；插件消费固定标签并拥有编排、评审和证据索引。插件公共协议仍由ArtCraft持有；research只读。本轮对应插件OpenSpec第9节，源码／原生候选／固定安装／宿主与完整V1逐层记录；条件跳过不作为通过。


## 执行控制增量（2026-10-08）

当前源候选加入可选的 execution_control：原生每次请求前检查撤销、截止时间、epoch、源工程摘要和累计输出预算，先fsync调用意图；原生子进程受单文件大小上限约束。托管返工按真实对象及字段授权核验，全球色板的每个消费者均需授权；未分类返工命令拒绝。几何、文字、其他色板及画板保持严格比较，原生保存产生的metadata.modified单独核验。

插件的独立进程组在启动门禁放行前记录PID／PGID／启动时间／任务nonce。进程组身份不能确认时保留占用，父进程退出后仍检查后代；TERM无效才对已验证归属的进程组升级KILL。cancel只请求撤销，reconcile必须观察原生停止、原位置目录inode、全部文件摘要，并用固定原生引擎只读重开工程和检查链接后，才能转为cancelled或interrupted_verified。未知结果不会升级为review_ready，不自动重放。恢复后的旧epoch回执单独审计隔离。

```bash
node src/cli.ts cancel STATE.sqlite TASK.json
node src/cli.ts reconcile STATE.sqlite TASK.json
node scripts/acceptance/managed_cancel.ts CONFIG.json
```

TASK含taskId与epoch。CONFIG沿用单轮品牌夹具的skill/source/runtimeHome/output/python/targetColor/authorization；原生取消测试在真实检查点保存后撤销，没有模拟原生写盘。当前固定dev.33技能尚无控制模块，因此托管执行会明确拒绝；独立公开入口仍保持原合同，发布dev.34后再固定同步和安装验证。

当前回归为独立源162项（132通过、30条件跳过），插件15项Node测试。原生候选验证覆盖单轮授权返工、真实检查点后的取消、监督器重启、原位置工程和依赖核验、epoch隔离；不代表完整3.x／6.x、固定安装或完整V1。OpenSpec已勾选3.1／3.2／3.4／3.5／3.7／3.8，完整验收3.3／3.6／3.9继续开放；总表81完成、46开放。
