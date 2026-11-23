#!/usr/bin/env python3
"""Patch Firefox browser.js with Geekser's keyboard-first chrome command palette.

The palette is native browser chrome, not page content or an extension.
Ctrl+T opens the palette; Ctrl+Shift+T retains Firefox's restore-tab behavior.
"""
from pathlib import Path
import argparse
import sys

START = "// GEEKSER COMMAND PALETTE — BEGIN"
END = "// GEEKSER COMMAND PALETTE — END"
BLOCK = r"""
// GEEKSER COMMAND PALETTE — BEGIN
(() => {
  const ns = "http://www.w3.org/1999/xhtml";
  let panel;
  let input;
  let results;
  let selectedIndex = 0;
  let candidates = [];
  const create = (tag, className = "") => {
    const node = document.createElementNS(ns, tag);
    node.className = className;
    return node;
  };
  function close() {
    if (panel) panel.hidden = true;
    if (input) input.value = "";
  }
  function open() {
    if (!panel) {
      panel = create("div", "geekser-palette-backdrop");
      panel.id = "geekser-palette";
      panel.hidden = true;
      const dialog = create("div", "geekser-palette-dialog");
      dialog.setAttribute("role", "dialog");
      dialog.setAttribute("aria-label", "Geekser command launcher");
      input = create("input", "geekser-palette-input");
      input.type = "text";
      input.placeholder = "Search, enter URL, or switch tab…";
      input.setAttribute("aria-label", "Search or enter an address");
      input.setAttribute("autocomplete", "off");
      results = create("div", "geekser-palette-results");
      results.setAttribute("role", "listbox");
      dialog.append(input, results);
      panel.append(dialog);
      document.documentElement.append(panel);
      panel.addEventListener("mousedown", e => {
        if (e.target === panel) close();
      });
      input.addEventListener("input", render);
      input.addEventListener("keydown", e => {
        if (e.key === "Escape") {
          e.preventDefault();
          e.stopPropagation();
          close();
        } else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
          e.preventDefault();
          e.stopPropagation();
          if (candidates.length) {
            selectedIndex = (selectedIndex + (e.key === "ArrowDown" ? 1 : -1) + candidates.length) % candidates.length;
            draw();
          }
        } else if (e.key === "Enter") {
          e.preventDefault();
          e.stopPropagation();
          candidates[selectedIndex]?.run();
          close();
        }
      });
    }
    panel.hidden = false;
    selectedIndex = 0;
    input.value = "";
    render();
    input.focus();
  }
  function targetURL(value) {
    const q = value.trim();
    if (!q) return null;
    // Never navigate to privileged or executable URL schemes from the palette.
    if (/^[a-z][a-z\d+.-]*:/i.test(q) && !/^https?:\/\//i.test(q)) return null;
    if (/^https?:\/\//i.test(q)) {
      try { return new URL(q).href; } catch { return null; }
    }
    if (/^(localhost|[^\s/]+\.[^\s/]+)(:\d+)?(\/.*)?$/i.test(q)) {
      try { return new URL("https://" + q).href; } catch { return null; }
    }
    return "https://www.google.com/search?q=" + encodeURIComponent(q);
  }
  function render() {
    const q = input.value.trim();
    const matchingTabs = Array.from(gBrowser.tabs)
      .filter(tab => !tab.closing)
      .filter(tab => !q || (tab.label || "").toLowerCase().includes(q.toLowerCase()))
      .slice(0, 7);
    candidates = matchingTabs.map(tab => ({
      label: "Switch to: " + (tab.label || "Tab"),
      run: () => { gBrowser.selectedTab = tab; }
    }));
    if (q) {
      const url = targetURL(q);
      if (url) candidates.unshift({
        label: "Open: " + q,
        run: () => { gBrowser.selectedTab = gBrowser.addTrustedTab(url); }
      });
    } else {
      candidates.unshift({
        label: "New Geekser tab",
        run: () => { gBrowser.selectedTab = gBrowser.addTrustedTab("about:newtab"); }
      });
    }
    selectedIndex = 0;
    draw();
  }
  function draw() {
    results.replaceChildren();
    candidates.forEach((candidate, i) => {
      const item = create("button", "geekser-palette-item");
      item.type = "button";
      item.textContent = candidate.label;
      item.setAttribute("role", "option");
      item.setAttribute("aria-selected", String(i === selectedIndex));
      item.addEventListener("click", () => {
        candidate.run();
        close();
      });
      results.append(item);
    });
  }
  window.addEventListener("keydown", event => {
    if (event.key === "Escape" && panel && !panel.hidden) {
      event.preventDefault();
      event.stopImmediatePropagation();
      close();
      return;
    }
    if (event.key.toLowerCase() === "t" && (event.ctrlKey || event.metaKey) &&
        !event.altKey && !event.shiftKey && !event.repeat) {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (panel && !panel.hidden) close();
      else open();
    }
  }, true);
})();
// GEEKSER COMMAND PALETTE — END
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("firefox_source", type=Path)
    action = p.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true")
    action.add_argument("--revert", action="store_true")
    a = p.parse_args()
    root = a.firefox_source.expanduser().resolve()
    target = root / "browser/base/content/browser.js"
    if not (root / "mach").is_file() or not target.is_file():
        p.error("Not a Firefox checkout")
    original = target.read_text(encoding="utf-8")
    has_start, has_end = START in original, END in original
    if has_start != has_end or original.count(START) > 1 or original.count(END) > 1:
        print("Invalid patch markers", file=sys.stderr)
        return 2
    if a.check:
        return 0 if has_start else 1
    result = original
    if has_start:
        i = result.index(START)
        j = result.index(END, i) + len(END)
        result = result[:i].rstrip("\n") + result[j:]
    if not a.revert:
        result = result.rstrip("\n") + "\n" + BLOCK
    if result != original:
        target.write_text(result, encoding="utf-8")
    print("Geekser command palette:", "reverted" if a.revert else "applied")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
