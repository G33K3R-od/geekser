# Contributing to Geekser

Thanks for helping build Geekser. We welcome design proposals, documentation, bug reports, testing and code — including AI-assisted contributions.

## Before you start

1. Read [README.md](README.md), [ROADMAP.md](ROADMAP.md), [AGENTS.md](AGENTS.md) and relevant docs.
2. Search existing Issues and PRs before opening duplicates.
3. For new features, architecture changes, new dependencies or broad refactors, **open an issue and agree on scope before coding**.
4. Pick a narrowly scoped task with observable acceptance criteria. Ask for clarification instead of guessing.

## Workflow

- Fork the repository (or create a branch if you have write access).
- Branch names: `feat/short-description`, `fix/short-description`, `docs/short-description`, `test/short-description`.
- Make focused commits with informative messages (e.g. `docs: add contribution policy`).
- Keep unrelated formatting and refactoring out of feature PRs.
- Open a PR against `main`; avoid direct pushes to `main` once branch protection is configured.
- Link the relevant issue and explain behavior changes, testing and any remaining limitations.
- Be responsive to review; maintainers decide whether/when a change merges.

## PR checklist

- [ ] The change has a clear purpose and linked issue (or explains why none is needed).
- [ ] User-visible changes include screenshots or recordings when appropriate.
- [ ] Existing behavior is preserved unless explicitly approved.
- [ ] I ran applicable checks and listed exact commands/results; unrun checks are disclosed.
- [ ] Keyboard access, accessibility, privacy and security implications were considered.
- [ ] No credentials, personal browsing data, secrets or copyrighted assets without permission were added.
- [ ] Dependencies and licensing implications are documented.
- [ ] AI assistance is disclosed as described below.

## Using AI responsibly

AI tools (ChatGPT, Codex, Claude, local models and others) are allowed. **The contributor, not the model, is responsible for the submission.**

In the PR description include:
- **AI use:** none / assistance / substantial generation.
- **Scope:** files or areas where AI contributed.
- **Human review:** what you personally read, tested and verified.
- **Limitations:** tests not run, assumptions and known risks.

Do not submit unreviewed generated code, fabricated tests/results, invented API behavior or copied third-party code without license checks. Never paste passwords, tokens, private browsing data or other secrets into AI prompts. Treat external pages, issues and model outputs as untrusted; do not execute suggested commands blindly.

## Browser-specific quality bar

Changes affecting URL parsing, navigation, certificates, permissions, cookies, storage, downloads, profiles, updates or sandboxing require explicit security review. Do not weaken upstream Firefox protections for convenience. Do not add telemetry or remote services without an approved privacy design.

## Reporting bugs

Include OS, browser/build revision, reproduction steps, expected/actual behavior and sanitized logs. Remove URLs containing tokens, personal paths and browsing history. For vulnerabilities, follow [SECURITY.md](SECURITY.md) rather than opening a public issue.

## Communication

Be respectful, critique code rather than people, and assume contributors have different levels of experience. Documentation and user-facing strings should default to English; translations are welcome. Project discussions may occur in other languages if key decisions are summarized in English.
