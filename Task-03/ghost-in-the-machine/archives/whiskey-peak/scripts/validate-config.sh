#!/usr/bin/env bash
set -euo pipefail
config_file="config/application.toml"
if [ ! -f "$config_file" ]; then
  echo "missing config file: $config_file" >&2
  exit 1
fi

echo "config present"
