# Curves

The `curves` module provides a registry of pre-defined elliptic curve parameters commonly used in Elliptic Curve Cryptography (ECC). These curves are standardized by SECG/NIST and have undergone extensive review.

## Available Curves

| Curve | Key Size | Standard | Common Use |
|-------|----------|----------|------------|
| `secp192k1` | 192-bit | SECG | Koblitz curve |
| `secp192r1` | 192-bit | NIST P-192 | Random curve |
| `secp224k1` | 224-bit | SECG | Koblitz curve |
| `secp224r1` | 224-bit | NIST P-224 | Random curve |
| `secp256k1` | 256-bit | SECG | Bitcoin, Ethereum |
| `secp256r1` | 256-bit | NIST P-256 | TLS, widely deployed |
| `secp384r1` | 384-bit | NIST P-384 | High security |
| `secp521r1` | 521-bit | NIST P-521 | Highest security |

## CurveParams Properties

Each curve is represented as a `CurveParams` dataclass with the following fields:

| Property | Description |
|----------|-------------|
| `p` | Prime defining the finite field |
| `a` | Coefficient 'a' in y² = x³ + ax + b |
| `b` | Coefficient 'b' in y² = x³ + ax + b |
| `n` | Order of the generator point |
| `h` | Cofactor |
| `coord` | Coordinate system (`CoordinateSystem.JACOBIAN` by default) |

## Functions

### `get_curve(name: str) -> CurveParams`

Retrieve curve parameters by standard name (case-insensitive).

```python
from ecutils.curves import get_curve

curve = get_curve("secp256k1")
print(curve.p)   # Prime field
print(curve.n)   # Order
print(curve.a)   # Coefficient a
print(curve.b)   # Coefficient b
```

**Raises** `KeyError` if the curve name is not found.

### `get_generator(name: str) -> Point`

Retrieve the generator point G for a named curve. The returned `Point` includes the curve parameters, so it is ready for arithmetic.

```python
from ecutils.curves import get_curve, get_generator

G = get_generator("secp256k1")
print(G)                # Point(x=..., y=...)
print(G.is_on_curve())  # True

# Scalar multiplication
public_key = 12345 * G
```

**Raises** `KeyError` if the curve name is not found.

## Exception Handling

```python
from ecutils.curves import get_curve

try:
    curve = get_curve("invalidCurveName")
except KeyError as e:
    print(e)  # "Unknown curve 'invalidCurveName'. Available: ..."
```

## Notes

- For secure applications, use standardized and vetted curves.
- All curves conform to SEC 2 / NIST standards.
- `get_curve()` returns `CurveParams` with Jacobian coordinates by default. Use `dataclasses.replace(curve, coord=CoordinateSystem.AFFINE)` for affine coordinates.
- `CurveParams` automatically validates the discriminant condition (4a³ + 27b² ≠ 0 mod p) at construction time, rejecting singular curves with `ValueError`.
