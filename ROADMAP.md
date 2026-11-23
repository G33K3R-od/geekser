# Geekser — master development roadmap

**Product:** Geekser — Built by G33K. Made for geeks.
**Engine:** Firefox / Gecko. **First platform:** Linux.
**Status (2026-11-23):** Firefox-backed development launcher and local home prototype run on the maintainer's machine. A standalone Firefox/Gecko source build **does not yet exist**.

This document is the source of truth for the development sequence. Features below are **planned**, not shipped, unless explicitly checked off. We will deliver cohesive milestone-sized increments rather than request a manual check after each small change.

## Definition of done (every milestone)

- Implemented functionality is real, not a static mockup.
- Basic tests or reproducible manual verification are documented; never fabricate results.
- Existing navigation, privacy, security and keyboard accessibility are preserved.
- Changes are reviewed for Firefox upstream compatibility and maintenance burden.
- User-facing limitations and known bugs are documented.
- The milestone ends with one concise demo/test checklist and a summary of changes.

## M0 — Project foundation [PARTIAL]

- [x] Public repository and contributor/AI policies.
- [x] Firefox-backed launcher and dedicated profile for Linux development.
- [x] Local home page prototype; remove placeholder date and confusing helper copy.
- [ ] Decide license, Mozilla trademark/branding and third-party attribution.
- [ ] Establish issues, CI, code ownership, security reporting contact.
- [ ] Decide how to maintain Firefox patchset and upstream version tracking.

**Gate:** architecture and contribution rules documented; legal/security blockers for distributing derived binaries identified.

## M1 — Real Firefox/Gecko development build [NEXT]

- [ ] Pin a known Firefox source revision and supported Linux toolchain.
- [ ] Reproduce upstream Firefox Artifact Build on CachyOS/Arch.
- [ ] Demonstrate an actual browser-chrome modification in a running build.
- [ ] Create a minimal Geekser patchset and documented apply/build/run commands.
- [ ] Document upstream rebase/update and rollback.
- [ ] Preserve Firefox browser security controls and extension compatibility.

**Gate:** a contributor can reproduce the patched Firefox build from documented commands on Linux. The existing launcher is **not** sufficient.

## M2 — Geekser browser shell

- [ ] Design tokens: colors, typography, spacing, radius, animation and contrast.
- [ ] Replace/customize browser chrome: navigation, address bar, window controls and menus.
- [ ] Implement responsive sizing, collapsed sidebar and keyboard/focus states.
- [ ] Preserve identity indicators, permission prompts, certificate warnings and security UI.
- [ ] Support multiple windows and Firefox profile/session semantics.

**Gate:** browser chrome is recognizably Geekser while browsing real websites.

## M3 — Vertical tabs and previews

- [ ] Vertical tab cards: title, URL/domain, favicon and active state.
- [ ] Close, pin, reorder, mute, multi-select and keyboard navigation.
- [ ] Capture cached thumbnails on tab switch/idle with strict resource limits.
- [ ] Define thumbnail privacy rules: no private windows, sensitive surfaces or uncontrolled storage.
- [ ] Handle large tab counts, crashed tabs, restored sessions and multiple windows.

**Gate:** full browsing workflow without relying on standard horizontal tabs.

## M4 — Command launcher

- [ ] Ctrl+T and sidebar + open a floating command palette.
- [ ] URL navigation and user-selectable search engine.
- [ ] Search open tabs, bookmarks, history and browser actions.
- [ ] Arrow keys/Enter/Escape, focus restoration, accessibility labels.
- [ ] Correct handling of pasted URLs, dangerous schemes and private windows.

**Gate:** fast keyboard-first navigation with no duplicate tabs by accident.

## M5 — Home dashboard

- [ ] Proper new-tab integration in browser chrome.
- [ ] Drag/drop and resizeable site tiles.
- [ ] User-defined sections (Work/Personal) and optional widgets.
- [ ] Widget permissions, network/privacy disclosure, offline behavior.
- [ ] Theme and persistence migration; remove prototype-only copy.

**Gate:** fully configurable dashboard works in normal new tabs and across restarts.

## M6 — Everyday browsing features

- [ ] Compact downloads popover with progress, open file/folder and keyboard access.
- [ ] Bookmarks/history UI integration and search.
- [ ] Search settings, tab restore, common context menus and shortcuts.
- [ ] Firefox extensions, password management and sync compatibility assessment.

**Gate:** daily browsing tasks can be performed without falling back to hidden Firefox UI.

## M7 — Workspaces and Split View

- [ ] Named workspaces, tab movement and persistence.
- [ ] Split View from the top toolbar, resize and close behavior.
- [ ] Sessions, windows, crashes and restore tests.

**Gate:** workspaces and split browsing survive restart safely.

## M8 — Personalization

- [ ] Themes and accent colors.
- [ ] Sidebar width, density, card preview visibility and animations.
- [ ] Configurable keyboard shortcuts and import/export where safe.
- [ ] Accessibility audit and reduced-motion settings.

**Gate:** customizations persist and do not degrade usability.

## M9 — Hardening and release infrastructure

- [ ] Automated smoke/UI tests, performance baselines and profiling.
- [ ] Firefox security update intake and release cadence.
- [ ] License compliance, Mozilla branding review, signed artifacts and update mechanism.
- [ ] Crash reporting design (opt-in only if added), privacy review and release checklist.

**Gate:** no known critical security, privacy, data-loss or build blockers.

## M10 — Public Linux Alpha

- [ ] Original Geekser logo/icon, app identity and release assets.
- [ ] Installable Linux packages and uninstall/update documentation.
- [ ] Public changelog, issue templates, known limitations and feedback process.
- [ ] Reproducible release and tested clean-install/upgrade path.

**Gate:** public alpha can be installed and updated with clearly documented support limits.

## Execution cadence and review policy

- Work in **milestone-sized batches** with small, reviewable commits.
- Do not ask the maintainer to verify every visual tweak. Run available automated/static checks first.
- Request human validation only for a meaningful demo, environment-only build step, security-sensitive decision or irreversible operation.
- If a milestone is blocked, document the blocker and continue independent, in-scope work where possible.
- Do not claim local runtime testing without access to the maintainer's machine.
- No unattended background work is implied: each coding session makes concrete commits and reports its result.

## Scope and priorities

**P0:** security, data loss, build blockers.
**P1:** browsing and navigation.
**P2:** user experience and customization.
**P3:** visual polish.

**Not in initial scope:** new rendering engine, mandatory accounts, unapproved telemetry, AI features that send browsing data to remote services, or promised Windows/macOS releases.

## Immediate next batch: M1

1. Establish Firefox checkout/revision and build configuration.
2. Add a minimal, reviewable browser-chrome patch.
3. Document commands for build/run/test and the upstream update procedure.
4. Test on the maintainer's CachyOS environment once, at the milestone gate.
