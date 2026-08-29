# navnet-core Architecture

## Purpose

This crate exists as the compatibility backbone for the Navigation Network core stack. It is intentionally small but widely referenced.

## Modules

- `registry` - loads and validates station registry snapshots from JSON payloads.
- `compat` - provides compatibility enforcement for station protocol versions and deployment metadata.
- `migration` - upgrades legacy YAML station snapshots produced by older Log Pose releases.

## Compatibility Constraints

The Compatibility Layer team has maintained a strict policy that `v2` target services only accept `v2` stations. `v1` services continue to accept legacy protocol versions for a gradual migration.

## Historical Notes

- `StationMetadata.last_checked` is preserved for compatibility with older operational tooling, even though newer services do not rely on it directly.
- `upgrade_legacy_snapshot` preserves labels for older deployments. The `last_checked` timestamp is intentionally hardcoded to avoid introducing false audit data during migrations.
