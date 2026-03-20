# Usage Guide

Practical examples for common use cases with ECUtils.

## Core Operations

### Creating Points and Curves

```python
from ecutils import Point, CurveParams, CoordinateSystem

# Define a curve: y² = x³ + x + 1 (mod 23)
curve = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Create points on the curve
P = Point(0, 1, curve)
Q = Point(6, 19, curve)

# Point at infinity (identity element)
inf = Point(curve=curve)
```

!!! note "Curve Validation"
    `CurveParams` automatically validates that the curve is non-singular
    (4a³ + 27b² ≠ 0 mod p). Attempting to create a singular curve raises `ValueError`:

```python
# This raises ValueError: singular curve
CurveParams(p=23, a=0, b=0, n=1)
```

### Arithmetic with Operators

```python
P + Q       # point addition
P - Q       # point subtraction
-P          # negation (additive inverse)
5 * P       # scalar multiplication
P * 5       # scalar multiplication (commutative)
P == Q      # equality
```

### Using Pre-defined Curves

```python
from ecutils import get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

# Private key → public key
private_key = 0xDEADBEEFCAFE
public_key = private_key * G
print(public_key.is_on_curve())  # True
```

### Coordinate Systems

```python
from ecutils import CurveParams, CoordinateSystem

# Jacobian coordinates (default — faster)
curve_jac = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Affine coordinates (explicit)
curve_aff = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)
```

## Point Compression

Compress a point to its x-coordinate and a single parity bit, reducing
storage from two field elements to one:

```python
from ecutils import Point, CurveParams

curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
P = Point(0, 1, curve)

# Compress: store only x and parity of y
x, parity = P.compress()
print(x, parity)  # 0  1

# Decompress: recover the full point
recovered = Point.decompress(x, parity, curve)
assert recovered == P
```

This also works with standard curves:

```python
from ecutils import get_curve, get_generator, Point

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

x, parity = G.compress()
recovered = Point.decompress(x, parity, curve)
assert recovered.x == G.x and recovered.y == G.y
```

!!! warning
    Compressing the identity point (point at infinity) raises `ValueError`.
    Decompressing an x-coordinate that does not correspond to a valid curve
    point also raises `ValueError`.

## Encoding Messages with Koblitz

Convert text into elliptic curve points and back:

```python
from ecutils import Koblitz

kob = Koblitz(curve_name="secp521r1")

# Encode a message
message = "Hello, world!"
point, j = kob.encode(message)

# Decode back
decoded = kob.decode(point, j)
assert decoded == message
```

For Unicode support, specify a larger alphabet size:

```python
kob = Koblitz(curve_name="secp521r1", alphabet_size=2**16)
point, j = kob.encode("Hello!")
```

## Digital Signatures (ECDSA)

### Simple: Sign and Verify Bytes

The easiest way — SHA-256 hashing is handled automatically:

```python
from ecutils import DigitalSignature

private_key = 123456789
ds = DigitalSignature(private_key, curve_name="secp256k1")

# Sign a message (SHA-256 applied internally)
r, s = ds.sign_message(b"Secure communication")

# Verify
is_valid = ds.verify_message(ds.public_key, b"Secure communication", r, s)
assert is_valid
```

### Advanced: Bring Your Own Hash

For full control over the hash function:

```python
import hashlib
from ecutils import DigitalSignature

private_key = 123456789
ds = DigitalSignature(private_key, curve_name="secp256k1")

# Hash the message yourself
message_hash = int(hashlib.sha256(b"Secure communication").hexdigest(), 16)

# Sign
r, s = ds.sign(message_hash)

# Verify
is_valid = ds.verify(ds.public_key, message_hash, r, s)
assert is_valid
```

## Diffie-Hellman Key Exchange

Establish a shared secret between two parties:

```python
from ecutils import DiffieHellman

alice = DiffieHellman(private_key=12345, curve_name="secp256k1")
bob = DiffieHellman(private_key=67890, curve_name="secp256k1")

# Exchange public keys and compute shared secret
secret_alice = alice.compute_shared_secret(bob.public_key)
secret_bob = bob.compute_shared_secret(alice.public_key)

assert secret_alice == secret_bob
```

## Massey-Omura Three-Pass Protocol

Exchange a secret message without prior key exchange:

```python
from ecutils import MasseyOmura, Koblitz

# Encode message as a curve point
kob = Koblitz(curve_name="secp521r1")
M, j = kob.encode("secret message")

alice = MasseyOmura(private_key=0xA1, curve_name="secp521r1")
bob = MasseyOmura(private_key=0xB2, curve_name="secp521r1")

# Three passes
c1 = alice.encrypt(M)        # Alice → Bob
c2 = bob.encrypt(c1)         # Bob → Alice
c3 = alice.decrypt(c2)       # Alice → Bob
plaintext = bob.decrypt(c3)  # Bob recovers M

assert kob.decode(plaintext, j) == "secret message"
```

## Math Utilities

ECUtils exposes low-level modular arithmetic utilities that are useful for
educational purposes and custom ECC implementations:

### Quadratic Residue Test

```python
from ecutils import is_quadratic_residue

# Is 4 a quadratic residue mod 23?
print(is_quadratic_residue(4, 23))  # True  (2² ≡ 4 mod 23)
print(is_quadratic_residue(5, 23))  # False
```

### Modular Square Root

```python
from ecutils import modular_sqrt

# Compute √4 mod 23
r = modular_sqrt(4, 23)
print(r)           # 2 (or 21, since both are valid)
print(r * r % 23)  # 4

# Returns None for non-residues
print(modular_sqrt(5, 23))  # None
```

These functions are used internally by `Point.decompress()` and can be
useful when implementing custom point-recovery or encoding schemes.
