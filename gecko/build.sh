#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
FIREFOX_SOURCE="${1:-${GEEKSER_FIREFOX_SOURCE:-$HOME/dev/firefox}}"
if [[ ! -f "$FIREFOX_SOURCE/mach" ]]; then
  echo "Firefox source checkout not found: $FIREFOX_SOURCE" >&2
  echo "Follow gecko/README.md to bootstrap Firefox first." >&2
  exit 2
fi
FIREFOX_SOURCE="$(cd "$FIREFOX_SOURCE" && pwd)"
export MOZCONFIG="$ROOT/gecko/mozconfig.artifact"
python3 "$ROOT/gecko/apply-ui.py" "$FIREFOX_SOURCE"
python3 "$ROOT/gecko/patch-newtab.py" "$FIREFOX_SOURCE"
cd "$FIREFOX_SOURCE"
printf 'Firefox revision: '; git rev-parse HEAD
printf 'Mozconfig: %s\n' "$MOZCONFIG"
./mach build
echo "Build complete. Run: bash $ROOT/gecko/run.sh $FIREFOX_SOURCE"
