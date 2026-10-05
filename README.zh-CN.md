# VectorCraft 独立技能

当前正在实现，尚未完成插件发布验收。

`vectorcraft-use` 自带 Python 3.11+ 安装器，固定官方 macOS arm64 CLI 制品，校验压缩包和二进制，保留许可证，原子安装新版本，复用完整的已有版本。技能目录可独立复制，不依赖兄弟技能或插件私有路径。

运行测试：`python3 -m unittest discover -s tests -v`。完整创作流程和宿主验收仍待完成。

规范和任务：[VectorCraft 插件 OpenSpec](https://github.com/full-aigc-plugins/vectorcraft-plugin/tree/main/openspec/changes/establish-v1-plugin)。

[English](README.md)

`vectorcraft-use` 的工作流助手已支持在同一 headless MCP 会话中执行受限原生计划、保留源修订、双画板导出，并有定向改色的真实回归测试。执行完整实测：`CRAFT_LIVE_TEST=1 python3 -m unittest discover -s tests -v`。插件 Harness 与宿主验收仍待完成。
