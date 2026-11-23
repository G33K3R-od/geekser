# Architecture — initial direction

**Status:** draft / decision pending. This is not a description of existing code.

## Constraints

- Browser engine: Firefox / Gecko.
- First supported development platform: Linux.
- Primary work: browser chrome/UI and user workflows, not a new rendering engine.
- Preserve upstream security features and enable timely Firefox security updates.
- Avoid coupling UI prototypes to a build strategy until verified.

## First technical spike

1. Document prerequisites and obtain an upstream Firefox source tree.
2. Reproduce an upstream-supported Linux artifact/development build.
3. Make and run a minimal browser-chrome change.
4. Evaluate the cost of maintaining a fork versus available upstream extension points.
5. Record a decision (with build commands, source revision, trade-offs and update strategy) before implementing core features.

## Planned functional boundaries

- **Browser shell:** navigation, address bar, window controls.
- **Tab experience:** vertical list, active state, optional cached previews.
- **Launcher:** keyboard-driven URL/search/commands and suggestions.
- **Home dashboard:** user tiles, optional widgets, settings persistence.
- **Downloads:** status and compact popover over existing browser download capabilities.
- **Workspaces / split view:** later-phase window and tab management.

These are conceptual boundaries, **not existing modules or directory names**.

## Security and privacy questions to resolve

- Thumbnail capture timing, private-window behavior, retention, encryption and deletion.
- Widget network access, permissions, caching and location privacy.
- URL suggestions and search provider disclosure.
- Profile compatibility, extensions, updates and release signing.
- Mozilla licensing, notices and trademark/branding obligations.

## Architecture decision record template

For every consequential decision record: **Context**, **Options**, **Decision**, **Consequences**, **Rollback plan**, **Date/owner**. Store accepted ADRs under `docs/adr/` when needed.
