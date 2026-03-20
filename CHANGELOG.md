# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - 2026-03-20

### Breaking Changes

This is a full API redesign. Code written for v1.x **will not work** without migration.

#### Core

| v1.x | v2.0 |
|------|------|
| `EllipticCurve(p, a, b, G, n, h)` | `CurveParams(p, a, b, n, h)` — immutable dataclass, no methods |
| `Point(x, y)` | `Point(x, y, curve)` — carries curve params, validates on construction |
| `curve.add_points(p1, p2)` | `p1 + p2` |
| `curve.multiply_point(k, p)` | `k * p` or `p * k` |
| `curve.double_point(p)` | `p + p` |
| `curve.is_point_on_curve(p)` | `p.is_on_curve()` |
| `JacobianPoint` (public) | `_JacobianPoint` (internal) |
| `EllipticCurveOperations` class | Standalone functions: `affine_add`, `jac_add`, etc. |
| `curve.use_projective_coordinates = True/False` | `CurveParams(coord=CoordinateSystem.JACOBIAN)` or `.AFFINE` |

#### Curves

| v1.x | v2.0 |
|------|------|
| `from ecutils.curves import get, secp256k1` | `from ecutils.curves import get_curve, get_generator` |
| `get("secp256k1", use_projective_coordinates=False)` | `get_curve("secp256k1")` + `dataclasses.replace(curve, coord=CoordinateSystem.AFFINE)` |
| `secp256k1` (pre-instantiated object) | `get_curve("secp256k1")` returns `CurveParams` |
| `curve.G` (generator as attribute) | `get_generator("secp256k1")` returns `Point` |

#### Algorithms

| v1.x | v2.0 |
|------|------|
| `ds.generate_signature(hash)` | `ds.sign(hash)` |
| `ds.verify_signature(pub, hash, r, s)` | `ds.verify(pub, hash, r, s)` |
| `ds.curve.n` | `ds._curve.n` |
| `Koblitz.encode(msg, alphabet_size=256, chunked=True)` | `Koblitz(alphabet_size=256).encode(msg)` — no more `chunked` mode |
| `Koblitz.decode(point, j, alphabet_size=256, chunked=True)` | `Koblitz(alphabet_size=256).decode(point, j)` |

#### Protocols

| v1.x | v2.0 |
|------|------|
| `MasseyOmura.first_encryption_step(msg)` | `MasseyOmura.encrypt(msg)` |
| `MasseyOmura.second_encryption_step(msg)` | `MasseyOmura.encrypt(msg)` |
| `MasseyOmura.partial_decryption_step(msg)` | `MasseyOmura.decrypt(msg)` |
| `mo.public_key` | Removed — Massey-Omura does not expose public keys |
| `mo.curve` (EllipticCurve instance) | `mo.curve_name` (string) + `get_curve()` / `get_generator()` |

#### Utils / Settings

| v1.x | v2.0 |
|------|------|
| `settings.LRU_CACHE_MAXSIZE = 0` (mutable at runtime) | `LRU_CACHE_MAXSIZE = 256` (compile-time constant) |
| `LRU_CACHE_MAXSIZE` via environment variable | Removed — constant defined in `ecutils.utils.settings` |
| `calculate_file_hash()` | Removed |

### Added
- Operator overloading on `Point`: `+`, `-`, `*`, `==`, unary `-`
- `Point.is_identity` property for checking point at infinity
- `Point.is_on_curve()` method
- Automatic point validation on construction (raises `ValueError` for invalid points)
- `CoordinateSystem` enum (`AFFINE`, `JACOBIAN`)
- `CurveParams` frozen dataclass with `coord` field
- `get_generator(name)` function to retrieve generator points
- `_trusted` flag on `Point` to skip validation for internal arithmetic results
- `py.typed` marker for PEP 561 type checker support
- Module structure diagram (`docs/assets/module_structure.svg`)
- `tests/test_group_properties.py` — group law tests (associativity, commutativity, distributivity, identity, inverse, Jacobian/Affine consistency)
- `.github/workflows/tests.yml` — test-only CI workflow for all PR branches
- Curve validation: `CurveParams.__post_init__` checks discriminant 4a³ + 27b² ≠ 0 (mod p); singular curves raise `ValueError`
- Point compression: `Point.compress()` returns (x, parity); `Point.decompress(x, parity, curve)` reconstructs the point
- Math utilities: `is_quadratic_residue(a, p)` (Euler criterion) and `modular_sqrt(a, p)` (Tonelli-Shanks) in `ecutils.utils.math`
- Sign/verify with hashing: `DigitalSignature.sign_message(bytes)` and `verify_message(pub, bytes, r, s)` with integrated SHA-256
- Comprehensive docstrings with formulas (addition, doubling, Jacobian), worked examples (E/F₂₃), security notes (nonce reuse, RFC 6090), algorithm descriptions (ECDSA, Koblitz, ECDH, Massey-Omura)
- Mathematical background documentation page (`docs/math-background.md`)
- New test suites: `test_curve_validation.py`, `test_math_utils.py`, `test_point_compression.py`, `test_educational_examples.py`

### Changed
- Refactored from monolithic modules to subpackage architecture:
  - `core.py` → `core/point.py`, `core/curve.py`, `core/arithmetic/affine.py`, `core/arithmetic/jacobian.py`
  - `algorithms.py` → `algorithms/digital_signature.py`, `algorithms/koblitz.py`
  - `protocols.py` → `protocols/diffie_hellman.py`, `protocols/massey_omura.py`
  - `curves.py` → `curves/registry.py`
  - `settings.py` → `utils/settings.py`
- All documentation updated to reflect v2.0 API and new features (usage, security, configuration, reference, index)
- All tests rewritten for the new API
- Minimum Python version raised to 3.9
- `ecutils.utils.__init__` and `ecutils.__init__` now export `is_quadratic_residue` and `modular_sqrt`

### Removed
- `EllipticCurve` class (replaced by `CurveParams` + `Point` operators)
- `EllipticCurveOperations` class (replaced by standalone functions)
- `JacobianPoint` as public API (now `_JacobianPoint`, internal)
- `calculate_file_hash()` utility function
- `chunked` mode in Koblitz encoding
- Pre-instantiated curve objects (`secp256k1`, `secp192k1`, etc.)
- Runtime-mutable `LRU_CACHE_MAXSIZE` and environment variable support
- `benchmarks.py` and `benchmarks_helper.py` scripts

## [v1.1.5] - 2026-01-21

### Added
- Benchmarks documentation page with performance data for all curves and configurations
- Security considerations documentation page
- Configuration documentation page for LRU cache and coordinate systems
- Benchmark scripts for performance testing
- Ruff configuration for linting and formatting

### Changed
- Reorganized documentation structure using mkdocstrings for API reference
- Consolidated CI workflows into single ci.yml
- Updated README with performance data and supported curves table
- Improved test coverage to 100%

### Removed
- Deprecated separate documentation files (moved to reference/ structure)
- Old workflow files (codecov.yml, pypi.yml)

## [v1.1.4] - 2024-10-26

### Changed
- Updated project description

## [v1.1.3] - 2024-10-26

### Changed
- Expand README and API documentation with usage examples and multi-language support

## [v1.1.2] - 2024-10-03

### Changed
- Updated test and documentation dependencies, expanded test coverage for the code, and added the ability to configure LRU cache size via an environment variable.

## [v1.1.1] - 2024-09-30

### Security
- Security fixes suggested by Snyk: updated `zipp` to version 3.19.1 or higher to avoid a vulnerability. (`zipp>=3.19.1`)

## [v1.1.0] - 2024-05-27

### Added
- Added operations in Jacobian coordinates to improve calculation efficiency.

### Changed
- Updated version to v1.1.0, making it the official stable version.

## [v1.0.0] - 2024-04-22

### Added
- Updated code of conduct and security policy.

### Changed
- Updated version to v1.0.0, making it the official stable version.

## [v0.0.1] - 2024-04-05

### Added
- Added names of new authors to the project.

### Changed
- Updated version to v0.0.1, making it the official stable version.

## [0.0.1.a0] - 2023-12-09

### Added
- Comprehensive documentation for the updated project structure and usage.
- Unit tests for ensuring the correctness of the implemented features and algorithms.
- Enhanced code design and architecture for better maintainability and extensibility.

### Changed
- Complete redesign of the project structure to make it incompatible with the previous version (0.0.1.dev4).
- Improved naming conventions and code organization to adhere to best practices.

### Removed
- Features, classes, or methods from version 0.0.1.dev4 that were not applicable to the redesigned architecture.

### Fixed
- Issues and bugs that were present in the previous version have been addressed.

### Deprecated
- Support for version 0.0.1.dev4 has been discontinued due to the significant changes in the project.
