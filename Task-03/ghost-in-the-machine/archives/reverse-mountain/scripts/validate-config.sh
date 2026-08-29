#!/usr/bin/env bash

set -euo pipefail

CONFIG_FILE="config/application.toml"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "missing config file: $CONFIG_FILE" >&2
  exit 1
fi

echo "config file found: $CONFIG_FILE"
