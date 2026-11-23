# Geekser Linux development app

This is a **separately launchable Gecko browser development profile** backed by an installed Firefox executable. It is not yet a compiled Geekser fork or a fully independent binary. It uses Firefox's existing navigation, tabs, permissions, downloads, extensions and security features.

## Install on CachyOS / Arch

```bash
sudo pacman -S --needed firefox git
git clone https://github.com/G33K3R-od/geekser.git
cd geekser
bash app/install-linux.sh
~/.local/bin/geekser
```

If already cloned, run `git pull` instead of `git clone`.

The installer adds a **Geekser (Development)** application launcher. It does not replace your normal Firefox profile. Your Geekser profile lives at `~/.local/share/geekser/firefox-profile` (or under `$XDG_DATA_HOME`).

**Important:** the launcher runs Firefox with `--no-remote --profile` and a dedicated local home page. The app still uses Firefox branding, Firefox's own native chrome, and Firefox's native new-tab behavior. The `userChrome.css` stylesheet applies experimental colors and requests Firefox's native vertical tabs. Firefox may ignore or change these preferences depending on version.

## Current limitations

- This is a Firefox-backed application launcher, **not a new Gecko distribution**.
- `Ctrl+T` opens Firefox's native new-tab page, **not** our launcher. We will change this through Firefox browser-chrome source modifications.
- The home page is a local file; new tabs do not automatically display it.
- No custom app icon yet. The desktop launcher temporarily uses the Firefox icon.
- Existing profile preferences are intentionally not overwritten on subsequent launches. To try updated styles, copy `app/userChrome.css` into the profile's `chrome/userChrome.css` manually and restart.
- Home page shortcut data is saved in the dedicated profile's localStorage.

## Next engineering milestone

Produce an actual Firefox/Gecko source build with a custom Geekser identity and browser-chrome changes. Follow `docs/DEVELOPMENT.md` for the upstream artifact build spike. Do not ship a rebranded Firefox binary without auditing Mozilla trademarks, licensing, release/update processes and security maintenance.
