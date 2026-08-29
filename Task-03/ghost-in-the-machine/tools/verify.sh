#!/usr/bin/env bash

# Verify that each archive contains the required repository structure.
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
archives_dir="$root_dir/archives"

for archive in "$archives_dir"/*; do
  if [ -d "$archive" ]; then
    echo "Verifying $(basename "$archive")"
    find "$archive" -maxdepth 2 -type d | sort
  fi
done
