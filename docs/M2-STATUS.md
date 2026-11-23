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

## Follow-up batch: native new-tab integration (pending runtime verification)

The Gecko source patch `gecko/patch-newtab.py` now modifies `browser/base/content/browser.js` and sets `AboutNewTab.newTabURL` from the development profile preference `geekser.newtab.url`. This routes Firefox's normal new-tab operation to the Geekser dashboard without relying on a WebExtension. The patch is idempotent, reversible and has a disposable-checkout unit test.

**Risk:** this uses an upstream browser-chrome API and must be checked on the current Firefox checkout; the browser may load an initial upstream new-tab page before the window load event. This has **not** been runtime verified yet. Do not mark M2 complete until the result is confirmed.

Run the single batch verification:

```bash
cd /run/media/g33k/HDD/work/geekser
git pull --ff-only
python3 -m unittest discover -s gecko -p 'test_*.py'
bash gecko/build.sh ~/dev/firefox
bash gecko/run.sh ~/dev/firefox
```

Check that the first page is Geekser, Ctrl+T opens Geekser rather than Nightly, and navigation and HTTPS security indicators still work. If the native new-tab API fails, capture the Browser Console error; the source patch can be reverted with `python3 gecko/patch-newtab.py ~/dev/firefox --revert` followed by rebuild.

Remaining work: floating command palette, native toolbar restructuring, custom tab previews, compact downloads, identity/branding.

## Batch: native Ctrl+T command launcher (pending runtime validation)

A source-level `gecko/patch-command.py` now adds a browser-chrome command palette to `browser/base/content/browser.js`. It intercepts Ctrl+T, searches open tabs by title, accepts HTTPS URLs and ordinary search queries, and supports arrow keys, Enter and Escape. Ctrl+Shift+T remains untouched. Styling lives in the M2 Gecko CSS patch; offline patch idempotence/rollback tests live in `gecko/test_command.py`.

**Not yet runtime verified.** The browser's own keyboard shortcut dispatch may differ between Firefox versions; verify Ctrl+T opens the overlay, search and tab switching work, Escape dismisses it, and Ctrl+Shift+T still restores a tab. If browser console reports an error, capture the message. Revert with `python3 gecko/patch-command.py ~/dev/firefox --revert` followed by a rebuild.

This is a **first functional launcher**: it does not yet include bookmarks/history/actions search, a configurable search provider, or accessibility focus restoration. Sidebar tab thumbnail cards, toolbar restructuring and downloads popover are still outstanding.

The current search implementation uses Google as a provisional default; provider settings are scheduled for M6. No arbitrary JavaScript/privileged schemes are accepted as direct input.
