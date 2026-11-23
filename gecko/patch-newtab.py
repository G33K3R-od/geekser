#!/usr/bin/env python3
"""Integrate Geekser new-tab routing into Firefox browser chrome source.

Source-level integration: browser.js sets AboutNewTab.newTabURL at window startup.
A pref supplies the URL so a development profile can point to a local dashboard.
"""
from pathlib import Path
import argparse
import sys

START = "// GEEKSER NEW TAB ROUTING — BEGIN"
END = "// GEEKSER NEW TAB ROUTING — END"
BLOCK = """
// GEEKSER NEW TAB ROUTING — BEGIN
// Run once per browser window; this is browser chrome, not an extension.
// Do not intercept URLs, security prompts, or private browsing content.
window.addEventListener("load", () => {
  try {
    const { AboutNewTab } = ChromeUtils.importESModule(
      "resource:///modules/AboutNewTab.sys.mjs"
    );
    const dashboardURL = Services.prefs.getStringPref("geekser.newtab.url", "");
    if (dashboardURL.startsWith("file://")) {
      AboutNewTab.newTabURL = dashboardURL;
    }
  } catch (error) {
    console.error("Geekser new-tab integration failed", error);
  }
}, { once: true });
// GEEKSER NEW TAB ROUTING — END
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("firefox_source", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--revert", action="store_true")
    args = parser.parse_args()
    source = args.firefox_source.expanduser().resolve()
    target = source / "browser/base/content/browser.js"
    if not (source / "mach").is_file() or not target.is_file():
        parser.error("Expected Firefox checkout with browser/base/content/browser.js")
    data = target.read_text(encoding="utf-8")
    a, b = START in data, END in data
    if a != b or data.count(START) > 1 or data.count(END) > 1:
        print("Invalid Geekser marker state; refusing to edit.", file=sys.stderr)
        return 2
    if args.check:
        print("Geekser new-tab patch:", "installed" if a else "missing")
        return 0 if a else 1
    if a:
        first = data.index(START)
        last = data.index(END, first) + len(END)
        data = data[:first].rstrip("\n") + data[last:]
    if not args.revert:
        data = data.rstrip("\n") + "\n" + BLOCK
    target.write_text(data, encoding="utf-8")
    print(("Reverted" if args.revert else "Applied") + " Geekser new-tab patch:", target)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
