# Geekser new-tab prototype

This is a **working Firefox WebExtension prototype**, not a standalone Geekser browser build. It replaces Firefox's new-tab page with a dark dashboard, a URL/search field and editable local shortcuts.

## Run it on Firefox (Linux)

1. Install Firefox and open `about:debugging#/runtime/this-firefox`.
2. Click **Load Temporary Add-on…**.
3. Select `prototype/manifest.json` from this repository.
4. Open a new tab.

The temporary extension will be removed when Firefox restarts. Your existing Firefox installation is not modified.

## Implemented

- Responsive dark new-tab page.
- Search or navigate using the search field.
- Add/remove shortcut tiles; saved using `browser.storage.local`.
- Date display, keyboard-focus styling, and reduced-motion support.

## Not implemented

- Browser chrome, vertical tabs, tab thumbnails, split view, downloads popover, and workspaces.
- Intercepting Firefox's built-in `Ctrl+T` shortcut: this requires browser-chrome integration and cannot be achieved by this extension.
- Drag-and-drop tiles, weather widgets, sync, themes or release packaging.

## Safety

No analytics or external APIs are called by the dashboard itself. The search field sends searches to Google when you submit a query; site tiles navigate to the chosen websites. The extension requests only the `storage` permission. Only HTTP(S) shortcuts are accepted. This is a prototype; do not treat it as a hardened browser distribution.
