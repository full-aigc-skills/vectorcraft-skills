# VectorCraft Skills

Independent VectorCraft skills. Implementation is in progress; this repository is not a completed plugin release.

The `vectorcraft-use` skill contains a self-contained Python 3.11+ bootstrap installer for the pinned official macOS arm64 CLI. It verifies the archive and executable, retains license files, atomically installs a new version, and reuses an intact installation without downloading again.

Run tests with `python3 -m unittest discover -s tests -v`. Full creative workflow and host acceptance remain pending.

Normative requirements and implementation tracking: [VectorCraft plugin OpenSpec](https://github.com/full-aigc-plugins/vectorcraft-plugin/tree/main/openspec/changes/establish-v1-plugin).

[简体中文](README.zh-CN.md)

The `vectorcraft-use` workflow helper now executes a bounded native plan in one headless MCP session, preserves source revisions, exports two artboards, and validates targeted recoloring in live tests. Run all live tests with `CRAFT_LIVE_TEST=1 python3 -m unittest discover -s tests -v`. Full plugin Harness and host acceptance remain pending.

Development version `0.1.0-dev.1` fixes concurrent first-use/reuse install-lock contention: wait up to 120 seconds, then verify and reuse; timeout preserves installations and never replays editing tasks.

Development version dev.2 includes hash-bound exchange-loss.json with every native delivery. Reports distinguish format losses, observed structure and unknown font/effect fidelity; exported derivatives never replace the retained native project.

## CLI and task skill suite

[VectorCraft Skill Suite Architecture](docs/VectorCraft-Skill-Suite-Architecture.md)

| Skill | Purpose |
| :--- | :--- |
| `vectorcraft-use` | use |
| `vectorcraft-cli` | cli |
| `vectorcraft-cli-setup` | cli setup |
| `vectorcraft-cli-project` | cli project |
| `vectorcraft-cli-paths` | cli paths |
| `vectorcraft-cli-shapes` | cli shapes |
| `vectorcraft-cli-boolean` | cli boolean |
| `vectorcraft-cli-text` | cli text |
| `vectorcraft-cli-appearance` | cli appearance |
| `vectorcraft-cli-artboards` | cli artboards |
| `vectorcraft-cli-assets` | cli assets |
| `vectorcraft-cli-export` | cli export |

`npx skills add full-aigc-skills/vectorcraft-skills --skill <skill-name>`

Commands use `SKILL_DIR`, the absolute directory of the `SKILL.md` actually loaded by the host. User/project `.agents/skills` and plugin-internal/cache layouts are supported; the CLI runtime is installed separately in the user data directory. Each skill was copied alone into all three layouts, including paths with spaces, and its documented script entry points ran `--help`. [Path verification](docs/evidence/installed-skill-paths.json). Existing host caches need an explicit update to receive the corrected documentation.

Version dev.5 adds explicit selection prerequisites for grouping/boolean/symbols and public image placement to the asset skill. Nine task skills independently cold-installed and edited native geometry, type, appearance, artboards and assets, with real SVG/PDF/PNG checks. Full regression: 38 passed, no skips. [Evidence](docs/evidence/task-skill-first-use.json). All 585 commands, complete interchange fidelity and final creative/GUI/model acceptance remain pending.

Additional installed-skill brand export verification passed: changing selected logo/wordmark objects updates both SVG color and decoded PNG pixels; unrelated icon properties and the second artboard PNG stay unchanged. This used existing verified runtime caches, not a new cold install. It does not prove automatic token dependency inference. [Evidence](docs/evidence/brand-export-color.json). Plugin and skill release tags are unchanged.

The native RGB global brand-swatch workflow passed a first-use public cold install from one copied appearance skill, including its own script and example. Linked SVG/PNG variants update while the unrelated icon and original project stay unchanged. Skill source v0.1.0-dev.6 is published; plugin v0.1.0-dev.7 is published. Actual host-installed single-skill public cold native acceptance also passes (6.487 seconds); all 58 installed skill hashes remain unchanged. Actual npx independent installation and model dispatch remain unverified. See [architecture](docs/VectorCraft-Brand-Tokens-Architecture.md) and [evidence](docs/evidence/native-brand-token-first-use.json).

Native Chinese text revision now has a single-skill cold test: explicit object edit keeps the first style, unrelated footer and original project; missing fonts stop delivery and successful font dependencies are recorded. Source working tree only, publication/host validation pending. [Architecture](docs/VectorCraft-Chinese-Text-Architecture.md), [evidence](docs/evidence/native-chinese-text.json).
