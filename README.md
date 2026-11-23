# geekser.

**Built by G33K. Made for geeks.**

Geekser is an early-stage, community-oriented browser project built around **Firefox / Gecko**. Our goal is a comfortable, customizable daily browser: fewer unnecessary controls, faster navigation, and a home page that feels like your own workspace.

> **Status: planning / foundation.** No usable browser build exists yet. Features below are goals, not shipped functionality.

## Product vision

- **Vertical tabs** with optional cached page thumbnails, clear titles, and compact controls.
- **Command launcher** on `Ctrl+T`: search the web, navigate to URLs, find open tabs/history/bookmarks, and run browser actions without leaving the current page.
- **Customizable home dashboard** with rearrangeable site tiles and optional widgets (weather, calendar, recently visited).
- **Compact downloads** button with a hover/focus popover showing recent downloads and progress.
- **Workspaces** for different contexts and an optional **Split View**.
- A cohesive, dark-first UI that stays usable with keyboard, mouse, and assistive technologies.

## Technical direction

We are targeting **Firefox / Gecko**, not building a new rendering engine. The integration approach (upstream fork, browser-chrome modifications, build tooling) is **not yet finalized**. Our first technical milestone is a reproducible Firefox artifact/development build and a small UI integration proof of concept. We will document the selected approach in `docs/ARCHITECTURE.md` before major implementation.

**Initial target:** Linux. Other platforms are future possibilities, not promises.

## Getting involved

Read [the roadmap](ROADMAP.md), [contribution guide](CONTRIBUTING.md), and [AI agent instructions](AGENTS.md). Open an issue before undertaking large changes. Human and AI-assisted contributions are welcome under the same review standards.

## Project principles

1. Daily usability over feature count.
2. Performance, accessibility, privacy and security by design.
3. No deceptive UI: prototypes must be labeled as prototypes.
4. Prefer small, reviewable changes and upstream-friendly maintenance.
5. Browser engine security updates take priority over cosmetic work.

## License and upstream attribution

**Licensing is not yet finalized.** Do not assume this repository is licensed for redistribution just because it is public. Before adding or distributing Firefox-derived code, review Mozilla's applicable MPL-2.0 obligations, third-party notices, branding/trademark requirements, and the licenses of all bundled dependencies. Contributors should only submit code they have the right to contribute.

Maintainer: [G33K3R-od](https://github.com/G33K3R-od). This is an independent project and is not affiliated with Mozilla.
