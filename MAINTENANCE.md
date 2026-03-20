# Maintenance Policy

This document describes the maintenance goals and update policy for ECUtils.

ECUtils is an open-source project maintained primarily by a single developer. The timelines below are **goals, not guarantees**. Community contributions are essential to keep the project healthy.

## Supported Versions

Only the latest major version receives updates. See [SECURITY.md](SECURITY.md) for the full support matrix.

| Version | Status |
|---------|--------|
| 2.0.x   | Active |
| 1.x.x   | End of life |
| 0.x.x   | End of life |

## Update Types

### Critical (security fixes)

- **Scope:** Vulnerabilities that could compromise cryptographic correctness or expose private keys.
- **Target response:** Patch within **72 hours** of confirmation.
- **Version bump:** Patch (e.g., 2.0.0 → 2.0.1).
- **Communication:** Security advisory on [GitHub](https://github.com/isakruas/ecutils/security/advisories).

### Bug fixes

- **Scope:** Incorrect results, crashes, or regressions in existing functionality.
- **Target response:** Patch within **14 days** of confirmation.
- **Version bump:** Patch (e.g., 2.0.0 → 2.0.1).

### Minor improvements

- **Scope:** New features, performance improvements, documentation updates, dependency bumps.
- **Target response:** Bundled into the next planned minor release.
- **Version bump:** Minor (e.g., 2.0.0 → 2.1.0).

### Breaking changes

- **Scope:** API changes that are not backward-compatible.
- **Target response:** Planned and announced in advance.
- **Version bump:** Major (e.g., 2.0.0 → 3.0.0).

> **Note:** These timelines are best-effort goals. Due to the nature of a solo-maintained open-source project, unforeseen circumstances may cause delays. Pull requests from the community are always welcome and can significantly accelerate fixes and improvements.

## Release Schedule

ECUtils follows a **release-when-ready** model rather than a fixed calendar:

| Type | Target frequency |
|------|------------------|
| Security patches | As soon as possible (target: 72h) |
| Bug fix releases | As needed (target: 14 days) |
| Minor releases | When sufficient improvements accumulate |
| Major releases | Only when breaking changes are justified |

## Deprecation Policy

- Deprecated features are marked with documentation warnings at least **one minor version** before removal.
- Deprecated features are listed in the [CHANGELOG.md](CHANGELOG.md).
- Migration guides are provided when breaking changes are introduced.

## Dependency Policy

ECUtils has **zero external dependencies** by design. This minimizes supply chain risk and simplifies maintenance.

Python version support follows this policy:

| Python Version | Policy |
|----------------|--------|
| Latest stable  | Always supported |
| Previous two   | Supported |
| Older          | Dropped in the next major release |

Currently supported: **Python 3.9+**

## Contributing

This project relies on community support. There are many ways to help:

- **Report bugs** — Open an issue on [GitHub](https://github.com/isakruas/ecutils/issues).
- **Submit fixes** — Pull requests for bugs or improvements are very welcome.
- **Improve documentation** — Typos, clarifications, new examples.
- **Review pull requests** — Help review and test contributions from others.
- **Security vulnerabilities** — Follow the process in [SECURITY.md](SECURITY.md).

See [CONTRIBUTING.md](https://github.com/isakruas/ecutils/blob/master/CONTRIBUTING.md) for guidelines.

## Quality Assurance

Every release must meet these criteria before publication:

- All tests pass (`pytest tests/`)
- Code coverage ≥ 99%
- Linting passes (`ruff check`)
- Documentation builds without errors (`mkdocs build`)
