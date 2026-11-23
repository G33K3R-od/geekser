#!/usr/bin/env python3
"""Apply Geekser M2 browser-chrome styling and defaults to a Firefox source tree.

Only modifies browser theme CSS and browser/app/profile/firefox.js.
Reversible, idempotent, and fails closed if expected source paths change.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

OLD_START = "/* GEEKSER M1 PROOF OF CONCEPT — BEGIN */"
OLD_END = "/* GEEKSER M1 PROOF OF CONCEPT — END */"
START = "/* GEEKSER M2 SHELL — BEGIN */"
END = "/* GEEKSER M2 SHELL — END */"
PREF_START = "// GEEKSER M2 DEFAULTS — BEGIN"
PREF_END = "// GEEKSER M2 DEFAULTS — END"

CSS = """
/* GEEKSER M2 SHELL — BEGIN */
/* These are browser chrome selectors, not content-page styling.
   Native Firefox sidebar/tabs remain functional. Security indicators remain visible. */
:root {
  --geekser-canvas: #15121d;
  --geekser-panel: #201a2b;
  --geekser-hover: #342941;
  --geekser-accent: #b38cf2;
  --geekser-text: #f2eafa;
  --geekser-muted: #a99bb9;
  --toolbarbutton-border-radius: 11px;
}
#navigator-toolbox {
  background: var(--geekser-canvas) !important;
  border-bottom: 1px solid #393044 !important;
  color: var(--geekser-text) !important;
}
#nav-bar {
  background: var(--geekser-canvas) !important;
  padding-block: 5px !important;
}
#urlbar-background {
  background: var(--geekser-panel) !important;
  border: 1px solid #4a3b58 !important;
  border-radius: 13px !important;
}
#urlbar[focused] #urlbar-background,
#urlbar[open] #urlbar-background {
  outline: 2px solid var(--geekser-accent) !important;
  outline-offset: -2px;
}
#urlbar-input {
  color: var(--geekser-text) !important;
}
#urlbar-input::placeholder {
  color: var(--geekser-muted) !important;
}
#nav-bar toolbarbutton:hover > .toolbarbutton-icon,
#nav-bar toolbarbutton:hover > .toolbarbutton-badge-stack {
  background-color: var(--geekser-hover) !important;
}
#sidebar-main,
#sidebar-box,
#vertical-tabs {
  background: var(--geekser-canvas) !important;
  color: var(--geekser-text) !important;
}
#sidebar-main .tab-background,
#vertical-tabs .tab-background {
  border-radius: 11px !important;
}
#sidebar-main .tabbrowser-tab[selected] .tab-background,
#vertical-tabs .tabbrowser-tab[selected] .tab-background {
  background: #463359 !important;
  outline: 1px solid #8662b4 !important;
}
#sidebar-main .tabbrowser-tab:hover .tab-background,
#vertical-tabs .tabbrowser-tab:hover .tab-background {
  background: var(--geekser-hover) !important;
}
#PersonalToolbar {
  background: var(--geekser-canvas) !important;
}
@media (prefers-reduced-motion: reduce) {
  #navigator-toolbox, #sidebar-main { transition: none !important; }
}
/* Geekser command palette */
#geekser-palette[hidden] { display: none !important; }
#geekser-palette {
  position: fixed !important;
  inset: 0 !important;
  z-index: 2147483647 !important;
  display: flex !important;
  align-items: flex-start !important;
  justify-content: center !important;
  padding-top: min(18vh, 150px) !important;
  background: rgba(8, 6, 13, .68) !important;
}
#geekser-palette .geekser-palette-dialog {
  width: min(660px, calc(100vw - 40px)) !important;
  max-height: 65vh !important;
  overflow: auto !important;
  border: 1px solid #6b5384 !important;
  border-radius: 18px !important;
  background: #201a2b !important;
  box-shadow: 0 24px 80px #0009 !important;
  padding: 12px !important;
}
#geekser-palette .geekser-palette-input {
  box-sizing: border-box !important;
  display: block !important;
  width: 100% !important;
  padding: 17px !important;
  border: 0 !important;
  border-bottom: 1px solid #493a57 !important;
  outline: none !important;
  background: transparent !important;
  color: #f5edff !important;
  font: 17px system-ui !important;
}
#geekser-palette .geekser-palette-item {
  box-sizing: border-box !important;
  display: block !important;
  width: 100% !important;
  text-align: left !important;
  padding: 12px 16px !important;
  margin: 3px 0 !important;
  border: 0 !important;
  border-radius: 10px !important;
  background: transparent !important;
  color: #e8dff3 !important;
  font: 14px system-ui !important;
  cursor: pointer !important;
}
#geekser-palette .geekser-palette-item:hover,
#geekser-palette .geekser-palette-item[aria-selected="true"] {
  background: #4b3562 !important;
}
/* GEEKSER M2 SHELL — END */
"""
PREFS = """
// GEEKSER M2 DEFAULTS — BEGIN
// Default preferences only; existing user choices take precedence.
pref("sidebar.revamp", true);
pref("sidebar.verticalTabs", true);
pref("sidebar.visibility", "always-show");
pref("browser.toolbars.bookmarks.visibility", "never");
// GEEKSER M2 DEFAULTS — END
"""
CSS_PATHS = [
    "browser/themes/shared/browser-shared.css",
    "browser/themes/shared/browser.css",
]
PREF_PATH = "browser/app/profile/firefox.js"


def remove_block(content: str, start: str, end: str) -> str:
    has_start, has_end = start in content, end in content
    if has_start != has_end:
        raise ValueError(f"incomplete block: {start}")
    if not has_start:
        return content
    if content.count(start) != 1 or content.count(end) != 1:
        raise ValueError(f"duplicate block: {start}")
    a = content.index(start)
    b = content.index(end, a) + len(end)
    return content[:a] + content[b:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("firefox_source", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true")
    action.add_argument("--revert", action="store_true")
    args = parser.parse_args()
    root = args.firefox_source.expanduser().resolve()
    if not (root / "mach").is_file() or not (root / "browser").is_dir():
        parser.error(f"not a Firefox checkout: {root}")
    css_path = next((root / p for p in CSS_PATHS if (root / p).is_file()), None)
    pref_path = root / PREF_PATH
    if css_path is None or not pref_path.is_file():
        print("Upstream Firefox paths changed; refusing to patch.", file=sys.stderr)
        return 2
    original_css = css_path.read_text(encoding="utf-8")
    original_prefs = pref_path.read_text(encoding="utf-8")
    if args.check:
        ok = START in original_css and END in original_css and PREF_START in original_prefs and PREF_END in original_prefs
        print("Geekser M2 patch: " + ("installed" if ok else "not installed"))
        return 0 if ok else 1
    try:
        new_css = remove_block(remove_block(original_css, OLD_START, OLD_END), START, END)
        new_prefs = remove_block(original_prefs, PREF_START, PREF_END)
    except ValueError as exc:
        print(f"Refusing unsafe patch: {exc}", file=sys.stderr)
        return 2
    if not args.revert:
        new_css = new_css.rstrip("\n") + "\n" + CSS
        new_prefs = new_prefs.rstrip("\n") + "\n" + PREFS
    # Validate both files before writing either.
    if new_css != original_css:
        css_path.write_text(new_css, encoding="utf-8")
    if new_prefs != original_prefs:
        pref_path.write_text(new_prefs, encoding="utf-8")
    print(("Reverted" if args.revert else "Applied") + " Geekser source changes:")
    print(" -", css_path)
    print(" -", pref_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
