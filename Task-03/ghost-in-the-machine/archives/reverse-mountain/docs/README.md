# Reverse Mountain Operational Notes

The Reverse Mountain archive contains the first service version recovered after the East Blue engineering group restored the build.

The runtime starts cleanly, but configuration values still reflect historical defaults from the earlier restoration effort.
The legacy `assets_dir` path is resolved relative to the config directory, while the cache directory is resolved relative to the process working directory.

This mismatch is consistent with a transition in progress and matches the type of issue that would later be revisited by the Whiskey Peak Engineering Office.
