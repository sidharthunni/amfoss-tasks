## East Blue Archive Findings

1. env_logger requires RUST_LOG env var set - otherwise info! logs are
   silently suppressed, making the program look broken when it isn't.
2. config/*.toml describes a networked service (host/port/max_clients)
   that the actual code never reads or implements - configuration
   drift from an earlier/different intended architecture.
3. main.rs originally hardcoded one station instead of using the
   clearly-built migration::upgrade_legacy_snapshot() + 
   legacy-stations.yml pipeline - fixed by wiring this up properly
   (now loads real legacy data).
4. Bug found in CompatibilityLayer::enforce(): only rejects mismatches
   when target == V2; doesn't correctly reject a V2 station when
   target is V1 (asymmetric with is_compatible, which handles this
   correctly). Documented rather than fixed, to preserve original
   behavior for historical analysis.

## Reverse Mountain Archive Findings

1. Same env_logger/RUST_LOG behavior as East Blue - needed RUST_LOG=info
   to see actual runtime logs.
2. Runtime warned "asset directory does not exist: config/assets" on
   startup. Traced this in runtime.rs - assets_dir is correctly resolved
   relative to the config file's own directory (config_dir.join(...)),
   so this wasn't a code bug. The config/assets folder was simply never
   recovered/created. Fixed by creating the missing directory
   (mkdir -p config/assets), which resolved the warning.
3. Confirmed via cargo test that a test named
   runtime_initializes_with_missing_asset_dir exists and passes -
   meaning the original warning-based handling (not crashing on a
   missing asset dir) was intentional, tested behavior.
4. Found scripts/validate-config.sh had no execute permission
   (-rw-rw-r--), causing "Permission denied" when run directly with
   ./scripts/validate-config.sh even though it has a valid shebang line.
   This is a classic Linux file-permission issue from archival recovery.
   Fixed with chmod +x scripts/validate-config.sh.
## Whiskey Peak Archive Findings

1. Two config files exist: application.toml (legacy_mode=false) and
   runtime.toml (legacy_mode=true) - only application.toml is actually
   loaded (confirmed via grep in main.rs). runtime.toml is a stale,
   unused historical artifact from Reverse Mountain migration.
2. Old bootstrap.log shows legacy_mode enabled at runtime - contradicts
   current application.toml (legacy_mode=false). Confirms behavior
   changed after this log was captured; log preserved as historical
   evidence, not current state.
3. Same missing config/assets directory issue as reverse-mountain -
   created it for consistency.
4. Scripts already had correct execute permissions this time.
5. All tests pass (application_config_loads, 
   legacy_mode_is_preserved_for_backward_compatibility,
   runtime_initializes_with_cache_creation, effective_max_clients_defaults_to_100).
## Alabasta Archive Findings

1. config/override.toml silently overrides application.toml at runtime
   (port, cache_dir, logging level) via apply_overrides() in config.rs -
   confirmed port 9011 in logs comes from the override file, not the
   base config. This is the "subtle, end-to-end" issue the README
   warned about - invisible unless you trace config.rs's load logic.
2. config/deprecated-settings.toml is explicitly marked as
   non-authoritative/archival in its own comments - no action needed.
3. All tests pass; no code bugs found in this archive, just the
   override mechanism to document.
