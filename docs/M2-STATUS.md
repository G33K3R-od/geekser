# M2 implementation status — browser shell (in progress)

The M1 Gecko build is confirmed working by the maintainer. M2 now applies **source-level Firefox browser chrome CSS and default preferences**, plus a dedicated Gecko development profile.

## Included in this batch

- Dark graphite/purple native browser chrome, compact address bar and focus state.
- Native Firefox vertical tabs enabled by default; active/hover tab cards styled.
- Bookmarks toolbar hidden to reduce chrome clutter.
- Geekser dashboard opens at startup in the built Gecko browser.
- Sponsored Firefox new-tab tiles and top stories disabled in the Geekser development profile.
- Reversible, idempotent source patcher with offline marker tests.

## Run one batch test

```bash
cd /run/media/g33k/HDD/work/geekser
git config core.fileMode false  # only if your HDD produces permission-only changes
git pull --ff-only
python3 -m unittest discover -s gecko -p 'test_*.py'
bash gecko/build.sh ~/dev/firefox
bash gecko/run.sh ~/dev/firefox
```

**Important:** close the previous Gecko development instance before running the new build. The build must be rerun for source CSS/default pref changes.

## Known limitations

- The dashboard is loaded as a **startup page**, not a real Ctrl+T/new-tab integration.
- Native Firefox vertical tabs are functional, but custom thumbnail cards are **not** implemented.
- The toolbar is styled Firefox chrome, not a full replacement layout.
- The browser binary still carries upstream Firefox Nightly identity.
- The M2 UI has **not** yet been verified on the maintainer's machine.
- Existing profile choices are overridden by the development profile's `user.js` on launch. This profile is disposable; do not use it for important personal browsing.

## Next implementation batch

1. Browser-integrated new-tab route and keyboard command launcher.
2. Custom tab card component with controlled thumbnail capture and privacy rules.
3. Native toolbar layout and download popover.
4. Distinct Geekser icon and branding after Mozilla trademark/license review.
