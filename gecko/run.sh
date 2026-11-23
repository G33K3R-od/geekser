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

# Dedicated development profile: apply Geekser defaults to existing profiles too.
# Never disable certificate validation, safe browsing or sandboxing.
cat > "$PROFILE/user.js" <<'PREFS'
user_pref("sidebar.revamp", true);
user_pref("sidebar.verticalTabs", true);
user_pref("sidebar.visibility", "always-show");
user_pref("browser.toolbars.bookmarks.visibility", "never");
user_pref("browser.startup.page", 1);
user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.showSearch", false);
user_pref("ui.systemUsesDarkTheme", 1);
PREFS

# The dashboard is loaded on startup as a local file, NOT yet a new-tab override.
HOME_URL="file://$ROOT/app/home/index.html"
cd "$FIREFOX_SOURCE"
./mach run --no-remote --profile "$PROFILE" "$HOME_URL"
