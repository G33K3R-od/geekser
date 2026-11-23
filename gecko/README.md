# M1 — Firefox/Gecko source build

This is the **first actual browser-chrome integration spike**, not a new-tab add-on or a Firefox launcher. It adds a small visible purple focus outline to Firefox's address bar **in the Firefox source checkout**, then builds that checkout using Mozilla's Artifact Build workflow.

**Status:** scripts are committed, but **no successful build on CachyOS has been verified yet**. The Firefox source revision is printed by the build script; record it in an M1 verification issue after the first successful build.

## Important: filesystem placement

Your Geekser repository may live on `/run/media/.../HDD`. **Do not put the Firefox source/build tree on NTFS/exFAT or another non-native filesystem.** Mozilla warns this can cause unexpected build failures. Prefer `~/dev/firefox` on a Linux filesystem with **at least 30 GB free**. Geekser's lightweight repository may stay on the HDD.

## One-time Firefox bootstrap

Run these from a Linux-native home directory:

```bash
sudo pacman -S --needed git python python-pip base-devel curl
mkdir -p ~/dev
cd ~/dev
curl -LO https://raw.githubusercontent.com/mozilla-firefox/firefox/refs/heads/main/python/mozboot/bin/bootstrap.py
python3 bootstrap.py
```

Choose **Firefox for Desktop — Artifact Mode**. The bootstrapper downloads the upstream source and toolchain dependencies; note where it places the checkout. On Arch-derived distributions, bootstrap may need additional manual steps.

## Build Geekser's first browser-chrome change

From your existing Geekser checkout:

```bash
git pull --ff-only
bash gecko/build.sh ~/dev/firefox
```

If Firefox was cloned elsewhere, replace `~/dev/firefox` with its actual path. The build script:

1. Validates the Firefox checkout.
2. Applies a small, marked CSS change in the Firefox browser chrome.
3. Prints the exact upstream Firefox revision.
4. Runs `./mach build` with Geekser's artifact mozconfig.

When the build succeeds, run:

```bash
bash gecko/run.sh ~/dev/firefox
```

Focus the URL bar: it should have a purple Geekser outline. Firefox will otherwise look like upstream Firefox at this milestone. **The launcher in `app/` is not involved.**

## Fast rebuild after UI changes

```bash
cd ~/dev/firefox
MOZCONFIG=/absolute/path/to/geekser/gecko/mozconfig.artifact ./mach build faster
```

Use an absolute mozconfig path. The scripts above calculate it automatically.

## Check or revert the patch

```bash
python3 gecko/apply-ui.py ~/dev/firefox --check
python3 gecko/apply-ui.py ~/dev/firefox --revert
```

The script refuses to modify a checkout without a `mach` file, refuses ambiguous marker blocks, and only removes its own CSS block. Use `git diff` inside the Firefox checkout to inspect the actual change.

## Validation checklist (one test at the milestone gate)

- [ ] `./mach build` completes successfully.
- [ ] `./mach run` opens a working Gecko browser window.
- [ ] Purple address-bar focus indicator is visible.
- [ ] HTTPS navigation, site identity, downloads and permissions still work.
- [ ] Firefox source revision, OS, build log and any fixes are recorded.
- [ ] Patch is reproducible and reversible.

## Limitations and next steps

- This is a **proof of source-level UI modification**, not custom Geekser branding or a release package.
- Artifact mode supports browser JS/CSS but not native Gecko C++/Rust changes.
- No release signing, automatic security-update mechanism or stable upstream version pin exists yet.
- Before M2, decide how to track an upstream revision and distribute/maintain the patchset.

Sources: [Mozilla Linux build guide](https://firefox-source-docs.mozilla.org/setup/linux_build.html), [Artifact builds](https://firefox-source-docs.mozilla.org/contributing/build/artifact_builds.html), [mozconfig](https://firefox-source-docs.mozilla.org/setup/configuring_build_options.html).
