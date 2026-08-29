# navnet-core

Internal compatibility crate used by Navigation Network services for station metadata, protocol versioning, and migration support.

## Purpose

`navnet-core` consolidates legacy station registry behavior and compatibility rules inherited from the Navigation Stations fleet. It is used by both runtime services and migration tooling during cross-release upgrades.

## Overview

- `registry` manages station metadata and registry snapshots.
- `compat` encodes compatibility policy for protocol negotiation and enforcement.
- `migration` houses migration helpers for legacy manifest formats and schema evolution.

## Operational Notes

This repository is maintained by the Compatibility Layer team. The crate has historically been consumed by multiple downstream services, so backward compatibility and semantics preservation are critical.

## Build

```sh
cargo test
```
