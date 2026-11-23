# Geekser roadmap

This is a **proposed sequence**, not a release schedule. Milestones move only when acceptance criteria are met. Track individual tasks through GitHub Issues.

## M0 — Foundation (current)

- [x] Create public repository.
- [x] Add initial README, roadmap, contribution policy and AI agent instructions.
- [ ] Decide and document Firefox source/build strategy; test supported Linux toolchain.
- [ ] Establish license, Mozilla attribution/branding approach, and security contact.
- [ ] Set up issue/PR templates and basic CI once code exists.
- [ ] Create architecture decision records (ADRs) for major decisions.

**Done when:** new contributors can understand the goal, reproduce the development environment, and identify the first code task.

## M1 — Gecko integration proof of concept

- [ ] Reproduce a working upstream Firefox development/artifact build on Linux.
- [ ] Prove that a small browser-chrome UI change can be built and launched.
- [ ] Document startup, debugging, upstream sync and rollback procedures.
- [ ] Verify normal navigation, profiles, permissions and basic browsing security are preserved.

**Done when:** a fresh contributor can build and run the prototype using documented steps.

## M2 — Geekser browser shell

- [ ] Establish design tokens and component conventions.
- [ ] Implement compact navigation/URL bar and vertical tab list.
- [ ] Add active-tab styling, close/new-tab behavior and keyboard navigation.
- [ ] Prototype cached thumbnails with bounded storage, privacy rules and no background page capture.
- [ ] Test multiple windows, long titles, many tabs and screen readers.

## M3 — Home and command launcher

- [ ] Build customizable home dashboard and reorderable site tiles.
- [ ] Add optional widgets with explicit permissions and data sources.
- [ ] Implement `Ctrl+T` command launcher, URL/search, suggestions and Escape handling.
- [ ] Support keyboard-only navigation and user-configurable search providers.
- [ ] Persist settings safely and test migration/defaults.

## M4 — Everyday features

- [ ] Compact downloads popover (mouse hover, keyboard focus, touch/click fallback).
- [ ] History, bookmarks and existing-tab search integration.
- [ ] Workspaces, optional Split View and restored sessions.
- [ ] Review privacy and permission boundaries for each feature.

## M5 — Personalization and alpha readiness

- [ ] Theme options, layout preferences and dashboard customization.
- [ ] Automated checks, performance baselines and accessibility review.
- [ ] Security update process, dependency inventory and release checklist.
- [ ] Linux alpha packaging, changelog, issue triage and user feedback.

## Explicit non-goals for the first prototype

- A new web rendering engine.
- A cloud account, proprietary sync backend or mandatory telemetry.
- Shipping an unmaintained Firefox fork without a security update plan.
- Promising cross-platform releases before Linux is stable.

## Prioritization

Use `P0` for security/build blockers, `P1` for core browsing, `P2` for everyday usability, `P3` for polish. Label beginner-friendly, well-scoped tasks `good first issue`.
