# Firefox / Gecko development setup

**Stage:** first build spike. These instructions follow upstream Mozilla documentation and are **not yet validated on CachyOS**.

## System requirements

Use a native Linux filesystem, Python 3.10+, Git and at least 30 GB of free disk space. Mozilla recommends 8 GB+ RAM. See [Mozilla's Linux build guide](https://firefox-source-docs.mozilla.org/setup/linux_build.html).

## Upstream checkout and artifact build

Run in a **separate directory**, not inside this small Geekser repository:

```bash
sudo pacman -S --needed git python python-pip base-devel curl
mkdir -p ~/dev && cd ~/dev
curl -LO https://raw.githubusercontent.com/mozilla-firefox/firefox/refs/heads/main/python/mozboot/bin/bootstrap.py
python bootstrap.py
```

Follow the interactive prompts. Choose **Firefox for Desktop — Artifact Mode** when offered. Bootstrap is responsible for obtaining source/dependencies; check the resulting checkout location.

```bash
cd ~/dev/firefox
./mach build
./mach run
```

If bootstrap placed the source elsewhere, adjust the `cd` path. For front-end-only edits after a successful build:

```bash
./mach build faster
./mach run
```

Artifact builds allow JS, HTML, CSS and localization edits, **not** native C++/Rust changes. See [Mozilla artifact build documentation](https://firefox-source-docs.mozilla.org/contributing/build/artifact_builds.html).

## First practical Geekser UI

Load `prototype/manifest.json` as a temporary add-on using Firefox's `about:debugging` page. This exercises the home experience independently of the Firefox source checkout.

## Next integration task

Make a minimal, documented change to Firefox browser-chrome UI in the upstream checkout, confirm that it builds and launches, and record the exact Firefox revision, files, commands and upstream update procedure before moving UI code into a maintained patch set. Do **not** copy the full Firefox tree into this repository without a deliberate source-management, licensing and update strategy.
