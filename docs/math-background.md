# Mathematical Background

This page provides the mathematical foundations behind ECUtils, including the
formulas used in point arithmetic, the group structure, and worked examples
on small curves for educational purposes.

## Elliptic Curves over Finite Fields

An elliptic curve in **short Weierstrass form** over a prime field F_p is defined by:

$$
E: y^2 = x^3 + ax + b \pmod{p}
$$

where the **discriminant** must be non-zero to ensure the curve is non-singular:

$$
\Delta = -16(4a^3 + 27b^2) \neq 0 \pmod{p}
$$

ECUtils enforces this automatically when constructing `CurveParams`.

## Group Structure

The set of points on an elliptic curve, together with a special "point at infinity" O,
forms an **abelian group** under point addition:

| Property | Description |
|----------|-------------|
| **Closure** | P + Q is also on the curve |
| **Associativity** | (P + Q) + R = P + (Q + R) |
| **Identity** | P + O = P for all P |
| **Inverse** | For P = (x, y), the inverse is -P = (x, -y mod p), and P + (-P) = O |
| **Commutativity** | P + Q = Q + P |

## Point Addition Formulas

### Addition (P ≠ Q)

Given P = (x₁, y₁) and Q = (x₂, y₂) with P ≠ ±Q:

$$
\lambda = (y_2 - y_1) \cdot (x_2 - x_1)^{-1} \pmod{p}
$$

$$
x_3 = \lambda^2 - x_1 - x_2 \pmod{p}
$$

$$
y_3 = \lambda(x_1 - x_3) - y_1 \pmod{p}
$$

### Doubling (P = Q)

Given P = (x₁, y₁):

$$
\lambda = (3x_1^2 + a) \cdot (2y_1)^{-1} \pmod{p}
$$

$$
x_3 = \lambda^2 - 2x_1 \pmod{p}
$$

$$
y_3 = \lambda(x_1 - x_3) - y_1 \pmod{p}
$$

### Scalar Multiplication

k · P is computed using the **double-and-add** algorithm in O(log k) steps.

## Worked Example: E: y² = x³ + x + 1 over F₂₃

This curve has order n = 28 and is used throughout the ECUtils test suite.

### Points on the Curve

```python
from ecutils import Point, CurveParams, CoordinateSystem

curve = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)
P = Point(x=0, y=1, curve=curve)
Q = Point(x=6, y=19, curve=curve)
```

### Addition: P(0, 1) + Q(6, 19)

$$
\lambda = (19 - 1) \cdot (6 - 0)^{-1} = 18 \cdot 4 = 72 \equiv 3 \pmod{23}
$$

$$
x_3 = 3^2 - 0 - 6 = 3 \pmod{23}
$$

$$
y_3 = 3(0 - 3) - 1 = -10 \equiv 13 \pmod{23}
$$

Result: **(3, 13)**

```python
R = P + Q
assert R.x == 3 and R.y == 13
```

### Doubling: 2 · P(0, 1)

$$
\lambda = (3 \cdot 0^2 + 1) \cdot (2 \cdot 1)^{-1} = 1 \cdot 12 = 12 \pmod{23}
$$

$$
x_3 = 12^2 - 0 = 144 \equiv 6 \pmod{23}
$$

$$
y_3 = 12(0 - 6) - 1 = -73 \equiv 19 \pmod{23}
$$

Result: **(6, 19)** — which is Q! So 2P = Q on this curve.

```python
assert (2 * P).x == 6 and (2 * P).y == 19
```

### Negation: -P(0, 1)

$$
-P = (0, -1 \mod 23) = (0, 22)
$$

```python
neg_P = -P
assert neg_P.x == 0 and neg_P.y == 22
```

### Identity: n · P = O

```python
identity = 28 * P  # n = 28
assert identity.is_identity
```

## Jacobian Coordinates

In Jacobian coordinates, a point is represented as (X, Y, Z) where:

$$
x = X / Z^2, \quad y = Y / Z^3
$$

### Doubling Formulas

$$
S = 4 \cdot X \cdot Y^2
$$

$$
M = 3X^2 + aZ^4
$$

$$
X' = M^2 - 2S
$$

$$
Y' = M(S - X') - 8Y^4
$$

$$
Z' = 2YZ
$$

### Advantage

Point addition and doubling in Jacobian coordinates require **no modular
inversions** (only multiplications and squarings), making scalar multiplication
roughly 3x faster. A single inversion is needed only at the end to convert
back to affine form.

See [RFC 6090, Section 4](https://www.rfc-editor.org/rfc/rfc6090#section-4)
for a detailed treatment.

## Quadratic Residues and Modular Square Roots

A value *a* is a **quadratic residue** mod *p* if there exists an *r* such
that r² ≡ a (mod p). ECUtils provides:

- `is_quadratic_residue(a, p)` — Euler's criterion: a^((p-1)/2) ≡ 1 (mod p)
- `modular_sqrt(a, p)` — computes r, using direct formula when p ≡ 3 (mod 4)
  or Tonelli-Shanks for the general case

```python
from ecutils import is_quadratic_residue, modular_sqrt

# Quadratic residues mod 23: {1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18}
assert is_quadratic_residue(4, 23) is True
assert is_quadratic_residue(5, 23) is False

r = modular_sqrt(4, 23)
assert r * r % 23 == 4
```

These utilities are used internally by `Point.decompress()` for point
decompression.

## Point Compression

A point P = (x, y) can be **compressed** to just (x, parity_of_y) since
for any x on the curve there are at most two valid y-values, which are
negatives of each other. The parity bit (y mod 2) distinguishes them.

```python
from ecutils import Point, CurveParams

curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
P = Point(x=0, y=1, curve=curve)

# Compress
x, parity = P.compress()  # (0, 1)

# Decompress
recovered = Point.decompress(x, parity, curve)
assert recovered == P
```

## ECDSA Signatures

### Signing

Given private key *d*, message hash *m*, and generator *G* of order *n*:

1. Choose random k ∈ [1, n-1]
2. R = k · G, r = R.x mod n
3. s = (m + r · d) · k⁻¹ mod n
4. Signature is (r, s)

### Verification

Given public key Q = d · G, message hash *m*, and signature (r, s):

1. w = s⁻¹ mod n
2. u₁ = m · w mod n, u₂ = r · w mod n
3. R' = u₁ · G + u₂ · Q
4. Accept iff R'.x mod n = r

## Koblitz Encoding

To encode a message as a curve point:

1. Convert the message to an integer *m* (base-α positional encoding)
2. For j = 1, 2, ..., try x = d · m + j (mod p)
3. Compute s = x³ + ax + b (mod p)
4. If *s* is a quadratic residue, compute y = √s and return (Point(x, y), j)

With d = 100, the probability of failure per attempt is ≈ 1/2, making
overall failure after 99 attempts astronomically unlikely (≈ 2⁻⁹⁹).

## Diffie-Hellman Key Exchange (ECDH)

1. Alice: H_A = d_A · G (public key)
2. Bob: H_B = d_B · G (public key)
3. Shared secret: S = d_A · H_B = d_B · H_A = d_A · d_B · G

Security is based on the **ECDLP**: given G and Q = d · G, recovering *d* is infeasible.

## Massey-Omura Three-Pass Protocol

Allows exchanging a secret point M without shared keys:

1. C₁ = e_A · M (Alice encrypts)
2. C₂ = e_B · C₁ (Bob encrypts)
3. C₃ = e_A⁻¹ · C₂ (Alice removes her layer)
4. M = e_B⁻¹ · C₃ (Bob recovers M)

Works because scalar multiplication is commutative: e_A · (e_B · M) = e_B · (e_A · M).

**Requirement:** gcd(private_key, n) = 1, so the modular inverse exists.

## References

- [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)
- [RFC 6090: Fundamental Elliptic Curve Cryptography Algorithms](https://www.rfc-editor.org/rfc/rfc6090)
- [NIST SP 800-57: Recommendation for Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
