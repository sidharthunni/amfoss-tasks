#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f "logs/run.log" ]; then
  tail -n 5 logs/run.log
else
  echo "no runtime log available"
  exit 1
fi
