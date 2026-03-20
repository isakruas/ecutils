# Configuration

ECUtils provides configuration options to customize its behavior for different use cases.

## LRU Cache

ECUtils uses an LRU (Least Recently Used) cache to improve performance by caching the results of elliptic curve arithmetic operations. The cache size is defined as a constant in `ecutils.utils.settings`:

```python
from ecutils.utils.settings import LRU_CACHE_MAXSIZE
print(LRU_CACHE_MAXSIZE)  # 256
```

The cached functions are:

- `affine_add` / `affine_double` — affine coordinate arithmetic
- `jac_add` / `jac_double` — Jacobian coordinate arithmetic

### Cache Size Guidelines

| Use Case | Recommended Size | Notes |
|----------|------------------|-------|
| Default | 256 | Good balance for most applications |
| High-throughput | 1024+ | More memory, better cache hits |
| Memory-constrained | 64 | Reduced memory footprint |

## Coordinate System

ECUtils supports two coordinate systems for internal arithmetic:

1. **Jacobian Coordinates** (default) — Faster for most operations, avoids modular inversions during intermediate calculations.
2. **Affine Coordinates** — Traditional representation, easier to debug.

### Selecting a Coordinate System

The coordinate system is set via the `coord` field on `CurveParams`:

```python
from ecutils import CurveParams, CoordinateSystem

# Jacobian (default)
curve = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Affine (explicit)
curve = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)
```

For pre-defined curves, `get_curve()` returns `CurveParams` with Jacobian coordinates by default. To use affine coordinates, create a copy with `dataclasses.replace`:

```python
from dataclasses import replace
from ecutils import CoordinateSystem, get_curve

curve_jac = get_curve("secp256k1")  # Jacobian (default)
curve_aff = replace(curve_jac, coord=CoordinateSystem.AFFINE)
```

### When to Use Each Coordinate System

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| General use | Jacobian | Faster scalar multiplication |
| Debugging | Affine | Easier to verify calculations |
| Interoperability | Affine | Standard representation for export |

## Curve Validation

`CurveParams` automatically checks the discriminant condition at construction
time:

$$
4a^3 + 27b^2 \neq 0 \pmod{p}
$$

This prevents accidental use of singular curves, which are cryptographically
broken. All pre-defined curves in the registry pass this validation.

```python
from ecutils import CurveParams

# Valid — non-zero discriminant
curve = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Invalid — raises ValueError
CurveParams(p=23, a=0, b=0, n=1)
```

### Algorithm and Protocol Configuration

Algorithms and protocols accept a `curve_name` parameter and use Jacobian coordinates internally:

```python
from ecutils import DigitalSignature, DiffieHellman

ds = DigitalSignature(private_key=123456, curve_name="secp256k1")
dh = DiffieHellman(private_key=12345, curve_name="secp256k1")
```
