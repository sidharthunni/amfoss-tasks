# Grand Line Restoration Initiative — Investigation Report

## Overview
Four recovered archives were investigated in order of increasing
restoration completeness: East Blue, Reverse Mountain, Whiskey Peak,
and Alabasta. Each was built, tested, and traced through its source,
config, logs, and (where present) git history to understand actual
vs. expected behavior.

## East Blue
- `env_logger` requires `RUST_LOG` to be set (e.g. `RUST_LOG=info`) or
  `info!` logs are silently suppressed — the program looked broken but
  wasn't.
- `config/*.toml` describes a networked service (host/port/max_clients)
  that the code never reads — configuration drift from an earlier
  intended architecture.
- `main.rs` hardcoded a single station instead of using the existing
  `migration::upgrade_legacy_snapshot()` + `legacy-stations.yml`
  pipeline. **Fixed**: `main.rs` now loads and migrates the real legacy
  snapshot on startup.
- **Bug identified (not fixed, documented)**: `CompatibilityLayer::enforce()`
  only rejects mismatches when `target == V2`; it does not correctly
  reject a `V2` station when `target == V1`, unlike `is_compatible()`
  which handles this correctly. Preserved as-is per the instruction to
  respect historical engineering decisions.

## Reverse Mountain
- Same `RUST_LOG` behavior as East Blue.
- Runtime warned `asset directory does not exist: config/assets`.
  Traced in `runtime.rs`: `assets_dir` is correctly resolved relative
  to the config file's own directory — not a code bug, just a missing
  recovered directory. **Fixed**: created `config/assets`.
- A test (`runtime_initializes_with_missing_asset_dir`) confirms the
  warn-not-crash behavior was intentional and already tested.
- `scripts/validate-config.sh` lacked execute permission, causing
  `Permission denied` despite a valid shebang. **Fixed**: `chmod +x`.

## Whiskey Peak
- Two config files exist: `application.toml` (`legacy_mode = false`)
  and `runtime.toml` (`legacy_mode = true`). Only `application.toml`
  is loaded (confirmed via `main.rs`); `runtime.toml` is a stale,
  unused artifact from the Reverse Mountain migration.
- An old `bootstrap.log` shows `legacy_mode enabled`, contradicting
  the current config — evidence that `legacy_mode` was flipped to
  `false` after that log was captured. Preserved as historical record.
- Same missing `config/assets` pattern — created for consistency.
- All tests passed; scripts already had correct permissions.

## Alabasta
- `config/override.toml` silently overrides `application.toml` at
  runtime (port, cache_dir, logging level) via `apply_overrides()` in
  `config.rs`. Confirmed the running service's port (9011) comes from
  the override file, not the base config — the "subtle, end-to-end"
  issue the archive's own README warned about.
- `config/deprecated-settings.toml` is explicitly self-documented as
  non-authoritative/archival — no action needed.
- `scripts/healthcheck.sh` and `scripts/start.sh` lacked execute
  permission. **Fixed**: `chmod +x` on both.
- All tests passed; no code bugs found.

## Rust concepts encountered
- Modules and workspace-style local path dependencies (`navnet-core`)
- Structs, enums (`ProtocolVersion`), and trait implementations
  (`CompatibilityPolicy`)
- Error handling with `anyhow::Context` and `thiserror`'s
  `#[error("...")]` derive macro
- Generic functions using `impl AsRef<Path>` for flexible path inputs
- `serde` for TOML/YAML/JSON (de)serialization with field renaming
  (`#[serde(rename = "id")]`)
- Ownership/borrowing shown clearly in functions like `enforce(&self, metadata: &StationMetadata)`

## Git concepts encountered
- Investigating commit history with `git log --oneline`
- Recognizing when a small commit count (e.g. Whiskey Peak's 2 commits)
  limits how much "evolution" can be traced through git alone, versus
  needing to cross-reference docs/logs instead

## Linux concepts encountered
- File permission bits (`-rw-r--r--` vs `-rwxr-xr-x`) and `chmod +x`
- Path resolution relative to a file's own directory vs. the current
  working directory
- Environment variables controlling program behavior (`RUST_LOG`)

## Assumptions made
- Where a discrepancy looked like a deliberate design choice with test
  coverage (e.g. Reverse Mountain's missing-asset warning), it was
  preserved rather than "fixed" beyond restoring the missing artifact.
- Where a discrepancy looked like a genuine logic bug with no test
  coverage protecting the current behavior (East Blue's `enforce()`
  asymmetry), it was documented rather than silently fixed, in order
  to preserve the original historical behavior for review.
