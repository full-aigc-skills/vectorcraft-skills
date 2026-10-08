# VectorCraft 独立技能

开发版34加入严格协议解析、品牌字段范围检查、13份独立操作合同和可选持久执行控制。原生候选验证通过；固定安装、宿主派发及完整V1验收分别记录。[架构](docs/VectorCraft-Brand-Gateway-Export-Architecture.zh_CN.md)。

固定插件36／技能源32通过13项独立原生冷安装、26项真实工作流测试和52个误改拒绝案例。64安装身份保持；51项未变技能复用已复核的历史冷启动证据。Art内置升级与完整V1仍开放。[固定验收](docs/VectorCraft-Fixed-Brand-Guard-Architecture.zh_CN.md)。

固定安装外观技能新增“同色但未绑定 token”验收：仅已绑定消费者更新，非消费者原生属性、无关 SVG／PNG／PDF 与原交付保持不变。本轮复用运行时，不关闭新增 V1 任务。[验收架构](docs/VectorCraft-Same-Color-Token-Architecture.zh_CN.md)。

Logo、图标与品牌图形需求进入，交付 `.vectorcraft` 及适用的 SVG、PDF、PNG。

当前技能源：`0.1.0-dev.44`；配套已发布插件：`0.1.0-dev.63`；13 个独立技能。

源40支持显式稳定artboardId与创建回执ID绑定，返工旧索引身份偏移、未知ID、冲突范围和重复输出在首次导出前拒绝；清单记录画板名称、尺寸、当前顺序与PNG预览顺序。公开旧53的两类静默偏移已原生复现，候选三类成功／四类拒绝通过。固定54完整VC-DM-004验收已完成，见文末四场景证据；GUI／模型／完整V1保持独立。

配套公开固定插件53／源39完成VC-DM-003全部四场景，插件任务4.7–4.9完成。真实品牌误改注入、同色非消费者隔离、中文修订及独立重开、两种SVG文字模式与18项入口拒绝通过；13技能摘要保持。源39不可变标签未改，完整V1仍开放。[逐场景证据](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-brand-text-fixed53-20261009.json)。

配套公开插件51／源38已完成路径几何4.3与组合／布尔4.6固定验收：六组原生几何保存／重开与18份导出，24组布尔工作流／Harness／SDK边界；七项几何与17项目标源测试通过。已知／未知失败为真实原生成功后的显式注入，不代表引擎缺陷。独立技能快照未改，完整V1仍开放。 [Geometry](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-geometry-fixed51-20261009.json) · [Boolean](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-boolean-fixed51-20261009.json).

配套公开插件51／技能源38已完成VC-TX-003全部五场景：五组真实原生验收、115项Node与43项Python回归通过，13技能摘要保持、13个登记进程组停止；插件任务3.9完成。独立技能源38与快照未改，不重发标签。完整V1仍开放。[固定取消与预算证据](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-budget-cancel-fixed51-20261009.json)。

源38在重命名前持久登记真实交付目录inode、device和清单摘要，覆盖链接素材打包子目录；公开固定插件50／实际宿主源38已通过全部七个VC-TX-002场景，插件任务3.6完成，完整V1仍开放。[固定逐场景证据](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-task-recovery-fixed50-20261009.json)。仅增加可选Harness控制记录，独立工作流不依赖插件。

已验证首次使用平台：macOS arm64、Python 3.11+。固定运行时安装在用户数据目录，技能文件保留在宿主加载目录。当前为开发版本；完整首版验收及通用 Skills CLI 实际安装仍未完成。

## 首次使用

在宿主中调用 **`vectorcraft-use`**。直接使用 CLI 时，将 `SKILL_DIR` 设为宿主实际加载的 `SKILL.md` 所在绝对目录；可能位于用户／项目 `.agents/skills`、插件内部或宿主缓存，以实际路径为准。以下入口在调用前安装并核验固定运行时。

<!-- CRAFT_FIRST_USE_START -->
```bash
: "${SKILL_DIR:?Set to the actual loaded skill directory}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands
```
<!-- CRAFT_FIRST_USE_END -->

实际制作、所需输入、原生工程和局部修改参见[可编辑工作流](skills/vectorcraft-use/references/workflow.md)。[安装与技能入口](skills/vectorcraft-use/SKILL.md) · [版本绑定历史](RELEASE-HISTORY.zh-CN.md)。版本与命令查询验证安装和发现，不代表创作完成。

[首次使用入口证据](docs/evidence/craft-readme-first-use-navigation-20261007.json)。

固定安装路径验收：独立技能及 Art 混合工作流在含中文和空格的路径下，通过原生创建与重开、定点返工及导出；Art 另验证移动交付包。技能与运行时身份保持不变。该结果仅覆盖 macOS arm64 的本次首次使用场景。 [路径验收证据](docs/evidence/craft-fixed-unicode-path-first-use-20261007.json).

固定发行前的历史源码候选：结构损坏的 runtime／Node 锁在写运行时目录或下载前返回本地恢复诊断。五项候选原生首次使用通过；发布插件快照保持不变，新不可变发行安装需另行验收。 [锁诊断候选](docs/VectorCraft-Lock-Shape-Architecture.zh_CN.md).

---

固定原生首次安装与完整命令恢复验收通过：新版五插件58技能逐项独立冷安装，十个Art技能分别安装四领域；四个原生下载半包SSL EOF恢复、72个原生保存后故障、四个健康命令返工及混合HD返工／恢复／移动包通过，全部安装摘要保全。仅关闭领域2.10／8.11与Art4.10；2639条命令逐项、GUI、模型、通用Skills CLI及完整V1仍开放。 [版本及证据](docs/evidence/codex-native-download-first-use-20261007.json).

固定发布前的候选记录：原生下载恢复候选：最多三次只读重试并丢弃半包；此前固定版本冷安装遇到SSL EOF失败，修复后的固定安装验收仍开放。

历史发行记录：当前独立技能源：`0.1.0-dev.19`；包含渐变／多重外观计划，12 项固定安装冷启动场景通过；Art 更新分发待验证，完整 V1 仍开放。

当前固定失败暂存验收：插件 dev.17、独立技能源 dev.15。全部58项独立CLI冷启动、24个原暂存原生故障案例及37原生场景＋6合同检查通过；Art77领域包升级仍开放。[证据](docs/evidence/codex-failed-stage-first-use-20261007.json)。

固定领域客户端首用复验：Film 插件 dev.16／技能源 dev.15，Effect／Photo／Vector 插件 dev.15／技能源 dev.14。隔离 Codex 发现58项零错误；实际安装副本24类保存后故障、四个健康公开工作流和已发布 Art 引擎＋安装后 Vector 客户端六类故障通过，全部58项安装摘要保全。Art dev.75 内置旧领域分发包尚需升级，全量命令／GUI／模型验收仍开放。[版本绑定证据](docs/evidence/codex-public-workflow-session-first-use-20261007.json)。
独立技能源元数据：`0.1.0-dev.14`。公开工作流 Session 结构检查已纳入此源码；固定插件／Art 分发及实际安装验收另行记录。
先前固定版本协议故障首用复验通过：48个独立技能源共288例，实际安装副本24例及四领域健康返工通过；58项安装摘要保持一致。验收范围与固定标签见 [协议故障验收记录](docs/evidence/codex-protocol-fault-first-use-20261007.json)。全量逐命令／GUI验收以及Art领域包升级仍开放。

协议故障修复候选：本领域12项技能逐个单独复制、空运行时公开安装后，原生保存成功再注入六种坏回复全部通过（72例，零跳过）。不重放、未知回执、工程重开与交付／技能保全均已检查。[证据](docs/evidence/protocol-fault-first-use-20261007.json)。固定安装副本与Art领域包升级仍为独立门禁。

固定插件 0.1.0-dev.13／技能源 0.1.0-dev.12 已通过安装后的返工门禁：隔离 Codex 发现全部58项技能零加载错误，本领域安装技能从空运行时直接执行文档创建／返工计划、保存重开与非目标保全。全部58项安装摘要不变，当前固定发行CI通过。[固定返工证据](docs/evidence/codex-complete-command-revision-first-use-20261007.json)。全量命令／GUI／模型验收保持开放。

本领域 12 个技能逐个单独复制、从各自空运行时公开安装后，配套返工计划全部通过（79.101 秒，零跳过）。[返工证据](docs/evidence/complete-command-revision-first-use-20261007.json)。更新快照的真实固定宿主安装另设门禁。

完整命令入口补充了配套的创建／返工 JSON 示例、重新打开后的显式选择前置条件，以及原生保存重开、非目标对象与像素检查。每个独立技能均包含两个可执行计划。[调用指南](skills/vectorcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision)。全量逐命令及 GUI 验收保持开放。

先前固定 Codex 快照首用通过：五插件／58 技能发现、58 项安装技能分别空运行时公开安装、四领域完整命令代表样例、Art HD 返工／恢复／移动包、安装摘要保全与固定发行 CI。[证据](docs/evidence/codex-complete-command-first-use-20261007.json)。这是有范围的原生验收；通用 Skills CLI 安装和全命令／GUI 验收仍开放。

## 完整原生命令入口

全部 12 项独立技能分别从空运行时使用公开锁定 CLI 附件安装，随后完成创建、保存重开、领域参数及渲染检查（74.946 秒，零跳过）。[逐技能冷首用证据](docs/evidence/complete-commands-cold-first-use-20261007.json)。本轮覆盖每项技能的完整命令代表样例；全命令／GUI 和实际宿主安装另行验收。

已发布开发快照：skills dev.11 / plugin dev.12；固定宿主首用代表门禁通过。

585 条命令现在均有逐项参数说明、技能归属与同会话调用入口。运行 `commands.py list / describe / check / run`；原生状态按实时 enabled 校验。旧工作流的 27 项交付合同保留。GUI 命令需显式 bridge，命令目录覆盖不代表全量验收。

[架构与操作指南](docs/VectorCraft-Complete-Commands-Architecture.zh_CN.md) · [逐项参考](skills/vectorcraft-use/references/command-reference.md) · [可运行示例](skills/vectorcraft-use/examples/commands-advanced.json)

当前正在实现，尚未完成插件发布验收。

`vectorcraft-use` 自带 Python 3.11+ 安装器，锁定维护版 macOS arm64 CLI 制品，校验压缩包和二进制，保留许可证，原子安装新版本，复用完整的已有版本。技能目录可独立复制，不依赖兄弟技能或插件私有路径。

运行测试：`python3 -m unittest discover -s tests -v`。完整创作流程和宿主验收仍待完成。

规范和任务：[VectorCraft 插件 OpenSpec](https://github.com/full-aigc-plugins/vectorcraft-plugin/tree/main/openspec/changes/establish-v1-plugin)。

[English](README.md)

`vectorcraft-use` 的工作流助手已支持在同一 headless MCP 会话中执行受限原生计划、保留源修订、双画板导出，并有定向改色的真实回归测试。执行完整实测：`CRAFT_LIVE_TEST=1 python3 -m unittest discover -s tests -v`。插件 Harness 与宿主验收仍待完成。

开发版本 `0.1.0-dev.1` 修复并行首次安装/复用时的安装锁竞争：等待最多 120 秒，再核验复用；超时不覆盖安装或重放编辑任务。

开发版本 dev.2 的原生交付包含摘要绑定的 exchange-loss.json，区分格式损失、结构观察与未验证字体/效果保真；导出派生物不替代原生工程。

## CLI 与场景技能体系

[VectorCraft Skill Suite Architecture](docs/VectorCraft-Skill-Suite-Architecture.zh_CN.md)

| 技能 | 用途 |
| :--- | :--- |
| `vectorcraft-use` | 组合多个本工具能力并保留可编辑原生交付 |
| `vectorcraft-cli` | 查询实际命令参数和能力，调用公开 CLI、MCP 与诊断 |
| `vectorcraft-cli-setup` | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| `vectorcraft-cli-project` | 建立和重开 vectorcraft，整理图层与文档属性 |
| `vectorcraft-cli-paths` | 创建锚点、控制柄、闭合和编辑矢量路径 |
| `vectorcraft-cli-shapes` | 建立几何形状并组合、变换品牌图形 |
| `vectorcraft-cli-boolean` | 使用 Pathfinder、复合路径与形状构建工具 |
| `vectorcraft-cli-text` | 设置 Logo 和品牌文字，处理字体与导出轮廓 |
| `vectorcraft-cli-appearance` | 修改品牌色、填充描边、透明与外观变体 |
| `vectorcraft-cli-artboards` | 制作 Logo 图标多画板与画板尺寸变体 |
| `vectorcraft-cli-assets` | 放置素材、管理链接、符号与已有图像描摹 |
| `vectorcraft-cli-export` | 输出矢量交换、预览和多画板资产包 |

`npx skills add full-aigc-skills/vectorcraft-skills --skill <skill-name>`

命令统一使用 `SKILL_DIR`，其值为宿主实际加载的 `SKILL.md` 所在绝对目录。支持用户级、项目级 `.agents/skills` 及插件内部或缓存目录；CLI 运行时另外安装到用户数据目录。每个技能单独复制到三种含空格的布局后，文档中的脚本入口均可运行 `--help`。[路径验证](docs/evidence/installed-skill-paths.json)。既有宿主缓存需更新后才会收到修正文档。

dev.5 补齐分组/布尔/符号的显式选择前置及资产技能的公开图像导入。九类场景技能各自冷安装并执行原生几何、文字、外观、画板和资产操作，核验真实 SVG/PDF/PNG；完整回归 38 项、零跳过。[证据](docs/evidence/task-skill-first-use.json)。全部 585 命令、完整交换保真及创作/GUI/模型验收仍未完成。

补充安装后品牌导出验证通过：选定 Logo／字标改色后，SVG 色值与 PNG 解码像素同时更新；无关图标属性及第二画板 PNG 保持不变。本次使用已核验运行时缓存，不是新的冷安装，也不证明自动推导 token 依赖。[证据](docs/evidence/brand-export-color.json)。插件及技能源发布标签保持不变。

原生 RGB 全局品牌色板工作流已通过单独复制 appearance 技能的首次在线冷启动验证，脚本与示例均来自同一技能；关联 SVG／PNG 更新、独立图标与旧工程保留有真实原生证据。独立技能源 v0.1.0-dev.6 已发布，插件 v0.1.0-dev.7 已发布；实际宿主安装后的单技能在线冷启动原生验证通过（6.487 秒），全部 58 个安装技能摘要保持一致。实际 npx 独立安装和模型派发仍待验证。详见 [品牌色架构](docs/VectorCraft-Brand-Tokens-Architecture.zh_CN.md) 与 [验证记录](docs/evidence/native-brand-token-first-use.json)。

原生中文文字修订通过单技能冷启动：明确对象修改保留首样式、独立页脚与旧工程；缺失字体停止交付，可用字体依赖写入清单。技能源 dev.7 与插件 dev.8 已发布；实际安装后的单技能在线冷启动原生验证通过（8.275 秒），全部 58 个安装摘要不变。[架构](docs/VectorCraft-Chinese-Text-Architecture.zh_CN.md)、[证据](docs/evidence/native-chinese-text.json)。

较早技能源 dev.7 的完整原生回归 42 项全部通过，零跳过（111.204 秒），包含九个独立任务场景、品牌色板与中文文字。任务场景使用全新公开缓存；命令发现和基线原生工作流明确复用已核验缓存。[证据](docs/evidence/dev7-full-native-suite.json)。

固定已安装插件 dev.8／技能源 dev.7 的补充验收验证四种矩形布尔操作、原生复合孔洞方向、SVG／PNG／PDF 独立解码、原交付保全和无效选择拒绝；不扩展为任意几何或编辑器往返支持。[验收记录](docs/VectorCraft-Boolean-Geometry-Acceptance.zh_CN.md)。

历史固定 dev.8 首次使用缺口，已由 dev.9 修复：无关画板 SVG 保留画板外品牌路径，品牌色修订后发生内容变化，其 PNG／PDF 保持不变。维护版原生运行时已发布，修复版不可变技能／插件快照尚待发布。[复现与修复边界](docs/VectorCraft-Artboard-Export-Gap.zh_CN.md)。

本地维护版 CLI 候选 `0.2.0-craft.1` 已通过 954 项引擎测试、12 项 CLI 集成测试及三画板单技能隔离安装任务；品牌改色后，无关 SVG／PNG／PDF 保持字节一致。12 个源技能安装器已支持维护版版本识别与来源记录。此段记录较早的本地候选阶段；维护版运行时现已发布，固定技能／插件验收仍待完成。[候选证据](docs/evidence/native-artboard-svg-candidate-20261006.json)。

已发布的维护版原生运行时通过工作区单技能 HTTPS 冷安装任务（4.970 秒）。不可变技能／插件发布和 ArtCraft 接入仍待完成。[证据](docs/evidence/public-artboard-svg-runtime-20261006.json)。

技能源 dev.8 锁定维护版运行时 `0.2.0-craft.1`，并启用单画板 SVG 隔离。当前完整原生回归 46 项全部通过、零跳过（86.570 秒）。固定插件 dev.9 宿主验收及 ArtCraft bundle 更新仍待完成。[完整原生回归](docs/evidence/maintained-full-native-suite-20261006.json)。

固定公开插件 dev.9／技能源 dev.8 已通过 Codex 发现全部 58 个技能，以及实际安装后的单导出技能公开冷启动原生验收（4.985 秒）。全部 58 个安装技能摘要不变。OpenSpec 4.22 的领域验收已完成，ArtCraft bundle 更新与完整 V1 验收仍待完成。[固定安装证据](docs/evidence/codex-vectorcraft9-artboard-first-use-20261006.json).

技能源 dev.9 锁定维护版 CLI craft.2，绑定 PDF 日期，并为缺少创建日期的旧工程保存摘要绑定的首次导出日期。完整原生回归 49 项全部通过、零跳过（91.950 秒）。固定插件 dev.10 与 ArtCraft bundle 验收仍待完成。[日期架构](docs/VectorCraft-PDF-Date-Architecture.zh_CN.md)、[原生回归](docs/evidence/craft2-full-native-suite-20261006.json)。

固定 ArtCraft dev.50／VectorCraft dev.10 的 Codex 0.153.4 隔离首次使用通过：五插件 58 技能发现、零加载错误；单导出技能空运行时跨秒原生验收 1 项通过（8.108 秒），混合品牌返工 2 项通过（51.409 秒），全部安装摘要保留。[发行绑定证据](docs/evidence/codex-release50-vector10-stable-export-first-use-20261006.json)。通用 Skills CLI 安装、模型／GUI、完整领域与创作验收仍开放。

本次更新的 22 个技能逐项公开冷启动全部通过（159.811 秒）：每项只复制自身目录到 .agents/skills，独立空运行时完成版本与命令合同检查，目录摘要和全部宿主安装摘要保留。该证据不代表通用 Skills CLI 安装或全部创作场景。

登记素材技能源候选：公开工作流已接入 PNG 链接、SVG 嵌入、JPEG／SVG 替换、原生依赖收集与迁移。[架构](docs/VectorCraft-Asset-Handoff-Architecture.zh_CN.md)。既有固定插件快照未改动；新版发布与安装宿主复验仍待完成。

技能源 dev.10 纳入登记素材：链接／嵌入 PNG、自包含 SVG、JPEG／SVG 替换、依赖收集与迁移，继续固定维护版 CLI `0.2.0-craft.2`。固定插件安装与 ArtCraft 接入分别验收；技能源候选证据不替代宿主安装回执。

固定插件 dev.11／技能源 dev.10 已通过 Codex 0.153.4 公开标签安装与发现：58 项技能、零加载错误。安装后的素材／导出单技能空运行时原生测试 2 项通过、零跳过（4.855 秒、6.743 秒）；12 项 VectorCraft 技能逐项独立冷安装通过（56.275 秒）。实际核验链接／嵌入 PNG、SVG、JPEG／SVG 替换、移动后直接重开原生工程及无关画板保全，全部 58 项安装摘要保持不变。[固定证据](docs/evidence/codex-vectorcraft11-assets-first-use-20261006.json)。ArtCraft 仍消费旧 Vector bundle，分发升级与混合首次使用仍待完成。

公开工作流回复检查已同步领域技能源候选，并通过有界原生／Art 协议验证。新的固定领域和 Art 分发包仍待发行与实际安装验收。[候选架构](docs/VectorCraft-Complete-Commands-Architecture.zh_CN.md) · [证据](docs/evidence/public-workflow-session-candidate-20261007.json)。

失败暂存候选：公开工作流保留原生暂存原路径、依赖摘要、最后提交请求与已完成回执，禁止重放；固定发行与安装副本验收仍开放。[架构](docs/VectorCraft-Failed-Stage-Architecture.zh_CN.md)。

固定领域失败暂存首用门禁已通过：Film插件18／源16，其他领域插件17／源15；五插件58技能发现零错误，全部58项独立空运行时CLI冷启动通过（417.646秒），实际安装副本24个真实保存后故障直接重开产品保留的原工程及依赖，四个健康创作／返工通过。全部安装摘要和16项固定插件CI保持通过；源仓未提供CI运行，仅有本地回归。只关闭领域OpenSpec3.12；Art77内置旧领域源，4.9升级和完整V1仍开放。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).

固定安装场景矩阵通过37个原生场景及6个合同检查，零跳过。Photo测试已从安装后的技能锁读取维护版原生版本，CLI与安装技能未修改。 [Evidence](docs/evidence/codex-failed-stage-first-use-20261007.json).


完整命令内层JSON修复候选：非有限值、溢出和重复键在绑定返回值前记录unknown，真实保存后九类故障与原工程重开通过。这是候选技能源证据，固定发布与实际安装复验尚未完成；逐命令／GUI门禁仍开放。

渐变与多重外观：12 项独立技能的源候选冷启动与原生返工验证已通过；固定安装与 Art 分发待验证。 [Architecture](docs/VectorCraft-Appearance-Gradient-Architecture.zh_CN.md).

固定安装渐变／多重外观：12 项技能通过，控制对象与原交付保全；Art 更新分发仍开放。 [Evidence](docs/evidence/codex-vectorcraft-gradient-first-use-20261007.json).

命令计划 JSON 源候选：重复键在安装和创建输出前被拒绝，全部 13 个领域技能的独立副本拒绝测试与有效计划校验通过，3 项专项测试通过。固定插件发布和安装后复验仍为 NOT_RUN。[证据](docs/evidence/command-plan-json-candidate-20261007.json)。

严格计划解析的固定安装复验通过：64 个 CLI 探测、54 个独立安装领域技能的 324 次重复键拒绝、54 次有效计划结构检查，以及四领域空缓存原生保存／重开／渲染实例通过；执行后全部 64 个安装技能摘要不变。仅关闭本次修复的发布门禁；通用 Skills CLI、Art 领域包升级、全部命令上下文和完整首版仍开放。[证据](docs/evidence/command-plan-json-fixed-first-use-20261007.json)。

四域共六个场景目录示例已修正；本包运行时身份与每个随附运行时锁一致。原生CLI制品保持原摘要。

新场景自身目录已通过固定安装复验；64项宿主身份匹配。完整V1仍开放。 [Evidence / 证据](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json).

独立安装依赖边界：当前摘要一致的冷安装记录与 128 项新固定副本安装器／CLI 失败检查验收四领域 SK-002。Art 与通用 Skills CLI 安装继续开放。[设计与证据](docs/Craft-Independent-Setup-Boundary-Architecture.zh_CN.md)。

当前固定协议引用发行矩阵（Film／Effect dev.37、Photo dev.36、Vector dev.34、Art dev.107）已通过隔离 Codex 安装／发现 64 项技能、16 项实际安装所有者文件摘要核对，以及五个全新领域缓存下的 64 项独立公开 CLI 探测。原生场景证据仅对字节一致的技能复用，完整首版仍开放。[固定发行证据](docs/evidence/craft-protocol-authority-fixed-first-use-20261008.json)。

固定插件 dev.37／技能源 dev.33：13 个实际安装技能副本各自空缓存安装原生 CLI，直接与网关返工均继承并导出三画板九份 SVG／PNG／PDF；关联颜色改变，无关图形及原交付字节保持，显式空列表与篡改拒绝通过。其余51项复核未变身份并沿用历史首用记录。Art116 内置 Vector32 尚未升级；完整 V1 未完成。[固定验收证据](docs/evidence/craft-vector37-gateway-export-fixed-first-use-20261008.json)。

## 布尔事务源码候选

技能源dev.36之后的未发布增量加入原生检查点保留、实时参与／结果ID、未选对象树检查与明确部分失败后的恢复；unknown不重放。三个公开入口共用守卫，包含链接素材检查点收集。当前已发布插件dev.40仍锁定dev.36，候选需另行发布和安装验收。[候选架构](docs/VectorCraft-Boolean-Transactions.zh-CN.md)。

## 开发版37结构授权

显式structure授权支持受控分组／解组／布尔返工和精确选择，逐项核对参与子树ID、实际选择、结果ID及未选模型属性。dev.37包含此前布尔事务增量，固定插件安装验收另行记录。

源39候选新增实际SVG文字模式与轮廓文字编辑性损失记录；普通、native.command、完整入口统一显式文字ID约束。13单技能资源同步。候选真实模式、中文定点修订及品牌非消费者边界验证分别记录；固定插件52／源39复验单独执行，完整V1仍开放。

公开固定插件54／源40已通过实际Codex隔离安装、13技能发现、三种稳定画板映射／四种拒绝和14份输出解码，13技能摘要保持。插件任务4.10／4.11最小实现完成，4.12完整画板隔离／PDF验收仍开放。[固定子集](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-artboard-mapping-fixed54-20261009.json)。

固定54／源40的VC-DM-004四个当前场景已完成验收，任务4.12标记完成，当前105项完成／22项开放。31项原生边界、单导出技能空运行时首用、同工程跨秒PDF及局部品牌修改后的无关SVG／PNG／PDF字节一致性通过，13技能摘要保持。未知绘制范围以原生空子图层实测，并结合固定上游源码确认None语义；跨画板群组记录为完整依赖。源回归190项中160通过／30跳过，GUI、模型、其他平台和完整V1仍开放。 [Full scenario evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-artboards-fixed54-20261009.json). 本轮仅修复QA断言及补充验收，生产载荷和发布标签不变。

技能源41增加实际SVG图像局部范围、祖先变换及引用／载荷摘要，区分内嵌栅格、内嵌SVG与未知引用；无损矢量声明禁止，原生工程保留。5项红绿测试、3项原生重开与9份输出独立解码通过；195项源回归165通过／30条件跳过。旧源40证据按原身份保留，当前候选见[证据](docs/evidence/exchange-candidate41-20261009.json)，新插件固定验收仍待执行。

历史子集：公开固定插件55／源41通过Codex0.153.4隔离安装与13技能发现，实际安装副本的三类原生重开、九份SVG／PDF／PNG解码和四类披露拒绝通过，13技能摘要保持，运行时复用。仅关闭4.13／4.14，107项完成／20项开放；4.15仍缺不可交换实时效果的自动导出退化或明确拒绝，以及原始效果工程保全验收。显式effect.expandAppearance案例不代替该证据。 [Fixed subset evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-exchange-fixed55-20261009.json).

固定55／源41已覆盖当前VC-DM-005-P／N：自动自由渐变SVG退化与局部栅格范围披露、独立原生重开及渐变编辑、源工程保全、三格式解码和七类异常拒绝通过。任务4.15正式完成，当前108项完成／19项开放；GUI、模型、其他平台和完整V1仍开放。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-exchange-qualified55-20261009.json).

技能源42候选增加已登记素材的品牌变体守卫：按真实栅格／SVG实例身份替换、原生边界校正、无关对象／层次／画板保全与摘要绑定的旧导出清单继承。固定55漏检原生无关图标误改已复现；候选九份输出解码、三份无关输出字节保全及错误依赖拒绝通过。202项源回归中172通过／30跳过；固定新插件及完整VC-DM-006另行验收。 [Candidate evidence](docs/evidence/brand-candidate42-20261009.json).

公开固定插件56／技能源42已通过VC-DM-006六个当前场景：RGB色板两入口、登记栅格／SVG多实例替换、原生边界保全、九份素材导出解码及三份无关输出字节保全；错误依赖、未知色板、损坏／链接清单拒绝并保留原工程与检查点。13项实际安装技能摘要保持。插件任务4.16–4.18完成，当前111项完成／16项开放；GUI、模型、其他平台、跨文件与Art捆绑包、完整V1单独验收。 [Fixed evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-brand-variants-fixed56-20261009.json).


技能源43候选新增摘要绑定的产物血缘、稳定逻辑ID、执行身份、父修订及可移动包内依赖。macOS arm64真实创建／移动重开／修订及五类完整性拒绝通过；默认回归207项中177通过／30跳过。配套固定57验收仍待完成。 [Evidence](docs/evidence/lineage-candidate43-20261009.json).


配套公开58／源43实际安装于Codex0.153.4 macOS arm64后，通过当前产物血缘三个场景：原生移动重开、父修订及公开七案例完整性检查；13项安装摘要未变。5.1–5.3完成，总体114/127完成，13项开放。 [Fixed qualification](https://github.com/full-aigc-plugins/vectorcraft-plugin/releases/tag/v0.1.0-dev.58).


配套公开59／源43实际安装于Codex0.153.4 macOS arm64后，通过原生工程／交换损失三个场景：独立重开、原生文字／自由渐变仍可编辑、三输出解码及20类拒绝。13项技能摘要不变，5.6关闭；115/127完成，12项开放。 [Qualification](https://github.com/full-aigc-plugins/vectorcraft-plugin/releases/tag/v0.1.0-dev.59).

配套插件60修复只读检查器完整依赖身份及旧检查证据失效。本地118项Node、92项Python通过；独立技能源43与13技能快照未改，保留不可变标签。任务6.3及总计12项任务仍开放。[开发版发布](https://github.com/full-aigc-plugins/vectorcraft-plugin/releases/tag/v0.1.0-dev.60)。

配套公开插件61／源43在实际Codex0.153.4 macOS arm64通过技术／创作证据分离全部三个场景：19项真实原生边界、119项Node及104项Python通过，13技能摘要保持。仅6.3关闭；116/127完成，11项开放。满分回执为明确QA注入，真实创作判断、GUI、其他平台与完整V1分别未验。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-quality-fixed61-20261009.json).

配套公开插件62／源43修复回执到达时预算耗尽的处理，四次共享尝试内保留更高分只读原生候选并持久停止。实际Codex隔离安装确认13技能摘要未变。122项Node、104项Python通过；6.6完整四场景验收仍开放，116/127完成、11项开放。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/main/docs/evidence/vectorcraft-revision-budget-fixed62-20261009.json).

配套插件62／本技能源43补充固定安装验收：三项真实原生修订验证小幅提升停滞、降分保留最佳及轮数上限；独占签名桌面修改源工程后，陈旧建议在修订执行前被拒绝，预算与最佳副本保全。插件114项Python测试通过，含10项证据测试；13项安装技能摘要未变。本库技能字节及开发标签43保持不变。任务仍为116/127完成、11项开放，6.6完整验收继续推进。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/f9a3cc47a3b00a1806de82a6e5f7ad48880ce736/docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json).

配套公开插件63／本技能源43经实际Codex0.153.4 macOS arm64安装后，通过VC-QA-002当前四场景：6次原生修订、15项边界守卫、1次独占签名桌面源工程修改。修复目标变化分支的授权／可信技术来源校验及最新问题记录，保留原目标最佳候选。124项Node、129项Python通过，含15项证据测试与14项重签篡改拒绝；13技能摘要未变。6.6完成，117/127完成、10项开放。QA评分仅测试控制机制，真实创作判断、其他平台、全部命令及完整V1分别未验。本库技能与标签43保持不变。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/0418c7793f8008ff2e060efb986013713c1f5fe4/docs/evidence/vectorcraft-revision-fixed63-20261009.json).

发布仓主分支新增发布者六层证据门禁，分别核验结构、技能源、运行时、宿主、真实任务与原生交付。复用未变化的固定63／源43实际安装及原生证据；本轮未新增原生或模型运行。隔离副本文档及OpenSpec通过仍不能把仅文档证明提升为运行能力。12项门禁与4项证据测试通过，发布仓全量145项Python通过。7.1–7.3完成，120/127完成、7项开放；市场资格仍false，完整宿主支持清单仍空。本库13技能与不可变标签43、插件不可变标签63均未改变。 [Evidence](https://github.com/full-aigc-plugins/vectorcraft-plugin/blob/3d6f433524ef6e543258df4249501b691990b14f/docs/evidence/vectorcraft-release-gate-20261009.json).

开发44修复独立技能的环境继承与不可信原生错误输出，并拒绝计划及成功回复中明确命名的字面凭据。6项目标测试通过；213项回归中183项通过、30项跳过。13项带空格路径与空运行时冷安装、585条命令发现，以及实际原生修订／三导出／独立重开通过。配套公开插件63仍锁定源43；插件候选的宿主秘密引用、完整入口审计和新固定分发另行验收，7.4–7.6尚未关闭，完整V1与市场资格仍开放。此校验不识别任意正文中的秘密，也不声称完整文件系统沙箱。 [Evidence](docs/evidence/permissions-candidate44-20261009.json).
