#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
FIREFOX_SOURCE="${1:-${GEEKSER_FIREFOX_SOURCE:-$HOME/dev/firefox}}"
if [[ ! -f "$FIREFOX_SOURCE/mach" ]]; then
  echo "Firefox source checkout not found: $FIREFOX_SOURCE" >&2
  exit 2
fi
FIREFOX_SOURCE="$(cd "$FIREFOX_SOURCE" && pwd)"
export MOZCONFIG="$ROOT/gecko/mozconfig.artifact"
PROFILE="${XDG_DATA_HOME:-$HOME/.local/share}/geekser/gecko-dev-profile"
mkdir -p "$PROFILE"
cd "$FIREFOX_SOURCE"
./mach run --no-remote --profile "$PROFILE"
