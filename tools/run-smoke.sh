#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
maestro test .maestro --include-tags smoke
