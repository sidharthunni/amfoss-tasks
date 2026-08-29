#!/usr/bin/env bash

# Archive synchronization helper for the Grand Line Restoration Initiative.
# This script is intentionally simple and designed for archive maintenance.
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
archives_dir="$root_dir/archives"

for archive in "$archives_dir"/*; do
  if [ -d "$archive" ]; then
    echo "Checking archive: $(basename "$archive")"
    if [ -f "$archive/Cargo.toml" ]; then
      echo "  Cargo.toml found"
    else
      echo "  Warning: missing Cargo.toml"
    fi
  fi
 done
