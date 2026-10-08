# 原生文件边界实验（未验收）

基线：公开源 `v0.1.0-dev.44`，固定 macOS arm64 原生 CLI `0.2.0-craft.2`，二进制 SHA-256 `ac47d32f34b8910dd559cff59d64cafaaade066227714359d1821cb2b0e59d1b`。

真实基线测试共5项：登记输入和输出占位符两项通过；外部读取、外部写入、目录内链接三项失败，说明现有完整命令入口不能作为文件隔离保证。见 `native-red.log.txt`。

原型采用 macOS sandbox-exec 的默认拒绝策略。5项测试中三个拒绝断言通过，两个正向测试失败，错误为 `mcp_disconnected: outcome may be unknown`；原生 `--version` 也终止于信号6。故三个拒绝断言不能算作权限验收通过。见 `native-prototype-failed.log.txt`。诊断发现放开全部文件读取可启动，但此操作违反目标边界，未采纳。

原型和集成补丁仅保存于此实验目录，不进入13个已交付技能的运行路径。`.py.txt` 保存原始实验源码；测试中的仓库根目录计算须在恢复至原测试路径后使用。补丁基于源44，应用前应核实当前文件。不得据此标记 VC-RL-002 或完整发布任务完成。

后续须先让正常原生读取和创建通过，再验证真实越界拒绝，补齐工作流、GUI、原生重开、宿主秘密引用和固定发布安装验收。公开44身份和证据保持不变。

## English

This is an unqualified filesystem-boundary experiment against immutable source44. The baseline passed both positive cases but failed all three escape checks. The sandbox prototype failed both positive cases during native startup; its three negative assertions therefore do not establish confinement. Prototype source and the integration patch are retained as non-shipping evidence. No permission or release acceptance task is completed by this experiment.
