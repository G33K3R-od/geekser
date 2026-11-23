#!/usr/bin/env python3
"""Apply or check a minimal, reversible Geekser browser-chrome CSS proof of concept.

Run from the Geekser repository: python3 gecko/apply-ui.py /path/to/firefox
This edits a Firefox source checkout, NOT a system Firefox installation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys

START = "/* GEEKSER M1 PROOF OF CONCEPT — BEGIN */"
END = "/* GEEKSER M1 PROOF OF CONCEPT — END */"
CSS = f"""\n{START}
/* Deliberately tiny, visible and reversible. Keep security indicators intact. */
#navigator-toolbox {{
  --geekser-accent: #b38cf2;
}}
#urlbar[focused] #urlbar-background {{
  outline: 2px solid var(--geekser-accent) !important;
  outline-offset: -2px;
}}
{END}
"""
CANDIDATES = [
    "browser/themes/shared/browser-shared.css",
    "browser/themes/shared/browser.css",
]

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("firefox_source", type=Path)
    p.add_argument("--check", action="store_true", help="report whether patch is present")
    p.add_argument("--revert", action="store_true", help="remove only our marked CSS")
    args = p.parse_args()
    root = args.firefox_source.expanduser().resolve()
    if not (root / "mach").is_file() or not (root / "browser").is_dir():
        p.error(f"not a Firefox source checkout: {root}")
    target = next((root / path for path in CANDIDATES if (root / path).is_file()), None)
    if target is None:
        print("Firefox CSS location changed; inspect upstream and update CANDIDATES.", file=sys.stderr)
        return 2
    original = target.read_text(encoding="utf-8")
    has_start = START in original
    has_end = END in original
    if has_start != has_end:
        print("Incomplete Geekser marker block; refusing to edit.", file=sys.stderr)
        return 2
    if args.check:
        print(f"{target}: {'patched' if has_start else 'not patched'}")
        return 0 if has_start else 1
    if args.revert:
        if not has_start:
            print("No Geekser patch to revert.")
            return 0
        start = original.index(START)
        end = original.index(END, start) + len(END)
        updated = original[:start].rstrip("\n") + original[end:]
    else:
        if has_start:
            print(f"Already patched: {target}")
            return 0
        updated = original.rstrip("\n") + "\n" + CSS
    target.write_text(updated, encoding="utf-8")
    print(f"{'Reverted' if args.revert else 'Applied'} Geekser browser-chrome patch: {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
