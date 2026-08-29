# Alabasta Architecture

The Alabasta service is the final integration point for Navigation Network runtime configuration and deployment orchestration.

It consolidates configuration from `application.toml` and applies runtime compatibility behavior inherited from prior archives.

The service uses a coordinator to initialize directories and a lightweight service wrapper for startup instrumentation.
