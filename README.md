# VectorCraft Skills

Fixed domain-client first use: Film plugin dev.16 / source dev.15; Effect/Photo/Vector plugin dev.15 / source dev.14. Codex discovers 58 skills without errors. Actual installed copies pass 24 post-save faults and four healthy public workflows; the published Art engine with the installed Vector client passes six faults. All58 installed identities remain unchanged. Art dev.75 still bundles earlier domain sources; exhaustive command/GUI/model acceptance remains open. [Version-bound evidence](docs/evidence/codex-public-workflow-session-first-use-20261007.json).
Independent source metadata: `0.1.0-dev.14`. This source includes public-workflow Session reply validation; fixed plugin/Art distribution and installed-copy acceptance are tracked separately.
Previous version-bound protocol recovery acceptance passed: 288 cases across 48 standalone source skills, 24 cases in actual installed copies, four healthy revision cases, and 58 unchanged installed skill identities. See [fixed evidence](docs/evidence/codex-protocol-fault-first-use-20261007.json). Exhaustive command/GUI acceptance and the Art domain-bundle upgrade remain open.

Protocol fault repair candidate: all 12 independently copied skills pass separate empty public-runtime installation and six faulty replies after real native save (72 cases; zero skips). Requests are not replayed; unknown receipts, saved-project reopening and delivery/skill preservation are checked. [Evidence](docs/evidence/protocol-fault-first-use-20261007.json). Fixed installed release and Art bundle upgrade remain separate gates.

Fixed plugin 0.1.0-dev.13 / skills 0.1.0-dev.12 installed revision acceptance passes: isolated Codex discovers all 58 skills without loading errors; this installed domain skill completes the documented cold creation/revision plans, saved-project reopening and non-target preservation. All58 installed digests remain unchanged; current fixed release CI passes. [Fixed revision evidence](docs/evidence/codex-complete-command-revision-first-use-20261007.json). Full command/GUI/model acceptance remains open.

All 12 domain skills pass the paired revision plans when copied alone and installed from separate empty public runtimes (79.101 seconds; zero skips). [Revision evidence](docs/evidence/complete-command-revision-first-use-20261007.json). Fixed installation of the updated snapshot remains a separate gate.

The complete-command entry now includes paired executable creation/revision recipes, explicit selection prerequisites after reopening, and native persisted-state/non-target checks. Each standalone skill includes both JSON plans. [Usage](skills/vectorcraft-use/references/command-usage.md#7-可执行局部返工--executable-targeted-revision). Full per-command and GUI acceptance remains open.

Previous fixed Codex snapshot first use passes: five plugins / 58 skills discovered, independent public cold runtime installs for all 58 installed skills, four complete-command native samples, Art HD revision/recovery/package checks, unchanged installed digests and fixed release CI. [Evidence](docs/evidence/codex-complete-command-first-use-20261007.json). This remains bounded native acceptance; generic Skills CLI installation and exhaustive command/GUI acceptance are open.

## Complete native command entry

All 12 standalone skills now pass separate empty-runtime installation from locked public CLI archives, followed by native creation, save/reopen, domain assertions and rendered image checks (74.946 seconds; zero skips). [Cold-first-use evidence](docs/evidence/complete-commands-cold-first-use-20261007.json). This verifies this complete-command sample in every skill; exhaustive command/GUI and actual host installation remain separate.

Published development snapshot: skills dev.11 / plugin dev.12; bounded fixed-host first use passed.

All 585 commands now have verbatim parameters, skill routing, and same-session invocation through `commands.py list / describe / check / run`. Live enabled state is checked; the existing 27-operation delivery workflow remains bounded. GUI commands require explicit bridge mode. Complete registry coverage does not establish full command acceptance.

[Architecture and usage](docs/VectorCraft-Complete-Commands-Architecture.md) · [Complete reference](skills/vectorcraft-use/references/command-reference.md) · [Runnable example](skills/vectorcraft-use/examples/commands-advanced.json)

Independent VectorCraft skills. Implementation is in progress; this repository is not a completed plugin release.

The `vectorcraft-use` skill contains a self-contained Python 3.11+ bootstrap installer for the pinned maintained macOS arm64 CLI. It verifies the archive and executable, retains license files, atomically installs a new version, and reuses an intact installation without downloading again.

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

Native Chinese text revision now has a single-skill cold test: explicit object edit keeps the first style, unrelated footer and original project; missing fonts stop delivery and successful font dependencies are recorded. Skill source dev.7 and plugin dev.8 are published. Actual installed single-skill public cold native testing passes in 8.275 seconds; all 58 installed hashes remain unchanged. [Architecture](docs/VectorCraft-Chinese-Text-Architecture.md), [evidence](docs/evidence/native-chinese-text.json).

Earlier skill source dev.7 full native regression passes all 42 tests with zero skips (111.204 seconds), including nine separately copied task scenes, brand swatches and Chinese text. Native task scenes use fresh public caches; CLI discovery and baseline native workflow explicitly reuse verified caches. [Evidence](docs/evidence/dev7-full-native-suite.json).

Installed plugin dev.8 / skill source dev.7 supplementary acceptance now checks four rectangular boolean operations, native compound-hole winding, independently decoded SVG/PNG/PDF, original delivery preservation and invalid selection rejection. This does not expand support to arbitrary geometry or editor round trips. [Acceptance](docs/VectorCraft-Boolean-Geometry-Acceptance.md).

Historical fixed dev.8 first-use gap, resolved by dev.9: an unrelated artboard SVG retains off-board brand paths and changes after a brand-token revision, although its PNG/PDF remain unchanged. A maintained native runtime is published; the repaired immutable skill/plugin snapshot is pending. [Reproduction and design boundary](docs/VectorCraft-Artboard-Export-Gap.md).

A local maintained CLI candidate `0.2.0-craft.1` now passes 954 engine tests, 12 CLI integration tests and the three-artboard isolated archive-install task, including byte-identical unrelated SVG/PNG/PDF after a brand-color edit. Twelve source skill installers support its maintained version identity and provenance. This paragraph records the earlier local candidate stage; the maintained runtime is now published, with fixed skill/plugin acceptance pending. [Candidate evidence](docs/evidence/native-artboard-svg-candidate-20261006.json).

The published maintained native runtime passed working-tree single-skill HTTPS cold first use (4.970 seconds). Immutable skill/plugin release and ArtCraft integration remain pending. [Evidence](docs/evidence/public-artboard-svg-runtime-20261006.json).

Skill source dev.8 pins maintained runtime `0.2.0-craft.1` and single-artboard SVG isolation. The complete current native suite passes 46 tests without skips (86.570 seconds). Fixed plugin dev.9 host acceptance and ArtCraft bundle update remain pending. [Full native regression](docs/evidence/maintained-full-native-suite-20261006.json).

Fixed public plugin dev.9 / skill source dev.8 now passes actual Codex discovery of 58 skills and installed single-export-skill public cold native acceptance (4.985 seconds). All 58 installed skill hashes remain unchanged. OpenSpec 4.22 is verified at this domain scope; the ArtCraft bundle update and complete V1 acceptance remain pending. [Fixed installed evidence](docs/evidence/codex-vectorcraft9-artboard-first-use-20261006.json).

Skill source dev.9 pins maintained CLI craft.2 and records stable PDF dates, including hash-bound fallback dates for legacy projects. The complete native source suite passes 49 tests with no skips (91.950 seconds). Fixed plugin dev.10 and ArtCraft bundle acceptance remain pending. [Date architecture](docs/VectorCraft-PDF-Date-Architecture.md), [native regression](docs/evidence/craft2-full-native-suite-20261006.json).

Fixed ArtCraft dev.50 / VectorCraft dev.10 first use passes in isolated Codex 0.153.4: five plugins, 58 skills and zero loading errors; one cold native export test with cross-second revision passes (8.108s), two mixed brand tests pass (51.409s), and all installed skill hashes remain unchanged. [Release-bound evidence](docs/evidence/codex-release50-vector10-stable-export-first-use-20261006.json). Generic Skills CLI installation, model/GUI, complete domain and creative acceptance remain open.

All 22 updated skills pass individual public cold first use (159.811s): each is copied alone to .agents/skills and installs into an independent empty runtime, checks exact version and command contracts, and preserves its files and all host-installed hashes. This does not establish generic Skills CLI installation or every creative scenario.

Registered-asset source candidate: linked PNG, embedded SVG, JPEG/SVG replacement, native dependency collection and relocation are implemented in the independent skill workflow. [Architecture](docs/VectorCraft-Asset-Handoff-Architecture.md). The existing fixed plugin snapshot is unchanged; new release and installed-host acceptance remain pending.

Registered assets are included in skill source dev.10: linked/embedded PNG, self-contained SVG and JPEG/SVG replacements, dependency collection and relocation. This release retains maintained CLI `0.2.0-craft.2`. Fixed plugin installation and ArtCraft integration are verified separately; the source candidate evidence is not a host receipt.

Fixed plugin dev.11 / skill source dev.10 has passed actual Codex 0.153.4 public-tag installation and discovery: 58 skills, zero loading errors. Installed single asset/export skills passed two native cold-start tests without skips (4.855s and 6.743s); 12 VectorCraft skills separately cold-installed in 56.275s. Linked/embedded PNG, SVG, JPEG/SVG replacement, direct relocated native reopening and unrelated artboard preservation were checked. All 58 installed hashes stayed unchanged. [Fixed evidence](docs/evidence/codex-vectorcraft11-assets-first-use-20261006.json). ArtCraft still consumes the older Vector bundle; its distribution upgrade and mixed first use remain open.

Public-workflow reply validation is synchronized in the domain source candidates and has bounded native/Art protocol evidence. Fixed updated domain and Art distributions are still pending. [Candidate architecture](docs/VectorCraft-Complete-Commands-Architecture.md) · [Evidence](docs/evidence/public-workflow-session-candidate-20261007.json).

Failed-stage candidate: public workflows retain original native staging paths, dependency hashes, last submitted requests and completed receipts; replay is prohibited. Fixed releases and installed-host acceptance remain open. [Architecture](docs/VectorCraft-Failed-Stage-Architecture.md).
