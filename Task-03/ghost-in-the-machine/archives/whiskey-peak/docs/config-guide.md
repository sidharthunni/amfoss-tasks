# Configuration Guide

`config/application.toml` is the authoritative runtime configuration.
`runtime.toml` is preserved solely for historical context.

The `validate_assets` flag controls whether startup performs strict asset path validation.
This was introduced during the Whiskey Peak stabilization phase.
