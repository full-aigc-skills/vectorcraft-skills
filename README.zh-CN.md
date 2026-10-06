# VectorCraft 独立技能

当前正在实现，尚未完成插件发布验收。

`vectorcraft-use` 自带 Python 3.11+ 安装器，固定官方 macOS arm64 CLI 制品，校验压缩包和二进制，保留许可证，原子安装新版本，复用完整的已有版本。技能目录可独立复制，不依赖兄弟技能或插件私有路径。

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

当前技能源 dev.7 的完整原生回归 42 项全部通过，零跳过（111.204 秒），包含九个独立任务场景、品牌色板与中文文字。任务场景使用全新公开缓存；命令发现和基线原生工作流明确复用已核验缓存。[证据](docs/evidence/dev7-full-native-suite.json)。

固定已安装插件 dev.8／技能源 dev.7 的补充验收验证四种矩形布尔操作、原生复合孔洞方向、SVG／PNG／PDF 独立解码、原交付保全和无效选择拒绝；不扩展为任意几何或编辑器往返支持。[验收记录](docs/VectorCraft-Boolean-Geometry-Acceptance.zh_CN.md)。

固定 dev.8 首次使用已知缺口：无关画板 SVG 保留画板外品牌路径，品牌色修订后发生内容变化，其 PNG／PDF 保持不变。尚未发布修复。[复现与修复边界](docs/VectorCraft-Artboard-Export-Gap.zh_CN.md)。

本地维护版 CLI 候选 `0.2.0-craft.1` 已通过 954 项引擎测试、12 项 CLI 集成测试及三画板单技能隔离安装任务；品牌改色后，无关 SVG／PNG／PDF 保持字节一致。12 个源技能安装器已支持维护版版本识别与来源记录。公开运行时安装锁尚未改变，修复尚未发布。[候选证据](docs/evidence/native-artboard-svg-candidate-20261006.json)。
