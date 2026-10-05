# VectorCraft Skills

Independent VectorCraft skills. Implementation is in progress; this repository is not a completed plugin release.

The `vectorcraft-use` skill contains a self-contained Python 3.11+ bootstrap installer for the pinned official macOS arm64 CLI. It verifies the archive and executable, retains license files, atomically installs a new version, and reuses an intact installation without downloading again.

Run tests with `python3 -m unittest discover -s tests -v`. Full creative workflow and host acceptance remain pending.

Normative requirements and implementation tracking: [VectorCraft plugin OpenSpec](https://github.com/full-aigc-plugins/vectorcraft-plugin/tree/main/openspec/changes/establish-v1-plugin).

[简体中文](README.zh-CN.md)

The `vectorcraft-use` workflow helper now executes a bounded native plan in one headless MCP session, preserves source revisions, exports two artboards, and validates targeted recoloring in live tests. Run all live tests with `CRAFT_LIVE_TEST=1 python3 -m unittest discover -s tests -v`. Full plugin Harness and host acceptance remain pending.

Development version `0.1.0-dev.1` fixes concurrent first-use/reuse install-lock contention: wait up to 120 seconds, then verify and reuse; timeout preserves installations and never replays editing tasks.
