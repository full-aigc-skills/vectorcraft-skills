# VectorCraft independent skill optimization

dev.34 is the current source candidate; the fixed plugin still consumes dev.33. Source changes do not automatically reach installed copies. This increment adds consistent strict JSON, field-level brand invariants and requested-value checks, thirteen standalone operation contracts, host invocation policies and source CI.

## Maintenance and validation

```bash
python3 -I -B scripts/build_skill_contracts.py --check
python3 -I -B scripts/build_command_coverage.py --check
python3 -I -B scripts/build_scenario_catalog.py --check
python3 -I -B scripts/sync_skill_suite.py --check
python3 -I -B -m unittest discover -s tests -v
```

Shared scripts are maintained in vectorcraft-use and synchronized deterministically. Each operation-contract.json is generated for its own skill and excluded from shared reference synchronization. Hosts supporting agents/openai.yaml allow implicit use routing and explicit specialized skills. Other hosts report actual capability.

Plans, protocol envelopes and contracted JSON text reject duplicate keys, non-finite numbers and overflow. Plain-text/image tools retain their existing contract. Native error-only envelopes differ from legitimate business error fields. Unknown results do not bind successful references, continue edits or replay; original failed native files and dependencies remain in place.

Brand edits allow only color fields bound to the requested token. Consumer text, closed contours, geometry, opacity and non-target appearance remain protected. Verify the target swatch and every bound field, distinguishing ineffective updates, absent consumers and verified_noop. RGB/CMYK/Gray/Lab authoring and native tint semantics remain distinct. Non-RGB unit tests do not establish all native or interchange acceptance. Export inheritance, explicit empty exports, source-plan digests, PDF dates and unrelated bytes retain their contracts.

The source owns execution; the plugin consumes immutable releases and owns coordination, review and evidence. ArtCraft retains public protocol ownership; research remains read-only. This work maps to plugin OpenSpec section9. Source, native candidate, fixed installation, host and fullV1 evidence are recorded separately; skipped tests are not passes.


## Managed execution increment (2026-10-08)

The source candidate checks cancellation, deadline, epoch, original project digest and accumulated output budget before each native request, and fsyncs its intent first. Native children have a file-size limit. Managed local revisions check actual object and field authorization, including every global-swatch consumer; unclassified edits fail closed. Native save timestamps are checked separately from protected document properties.

The plugin records owned PID/PGID/start-time/task identity before releasing its launch gate. Parent exit is followed by process-group observation; TERM-ignoring owned descendants may receive KILL. Cancellation retains writer occupation. Reconciliation requires actual native stop, original directory identity and file digests, plus read-only native reopen and dependency checks. It produces cancelled or interrupted_verified, never successful delivery from partial files, and quarantines receipts from an older epoch.

Use `node src/cli.ts cancel STATE.sqlite TASK.json` or `node src/cli.ts reconcile STATE.sqlite TASK.json`; TASK contains taskId and epoch. Native opt-in driver: `node scripts/acceptance/managed_cancel.ts CONFIG.json`, using the explicit single-round brand fixture configuration. The fixed dev.33 skills lack execution_control, so managed execution rejects them until the new source is published and fixed separately.

Current source regression:162 tests,132 passed,30 conditionally skipped; plugin Node regression:15 passed. Native candidate proof covers authorized revision, real saved-checkpoint cancellation, registry restart, original-file/dependency inspection and epoch fencing. Tasks3.1/3.2/3.4/3.5/3.7/3.8 are checked; complete acceptance3.3/3.6/3.9 remains open. Full task table:81 completed,46 open. This is not fixed-install, full sections3/6 or V1 acceptance.
