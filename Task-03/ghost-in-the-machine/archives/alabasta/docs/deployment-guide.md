# Deployment Guide

The Alabasta archive should be deployed from the repository root.
The service reads configuration from `config/application.toml` and honors overrides in `config/override.toml`.

The `deployment/plan.yml` file records the final rollout strategy.
Legacy compatibility is preserved for older toolchains during the final integration pass.
