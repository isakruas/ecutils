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

print(P)    # Point(x=0, y=1)
print(Q)    # Point(x=6, y=19)
print(inf)  # Point(∞)
```

!!! note "Curve Validation"
    `CurveParams` automatically validates that the curve is non-singular
    (4a³ + 27b² ≠ 0 mod p). Attempting to create a singular curve raises `ValueError`:

```python
from ecutils import CurveParams

# This raises ValueError: singular curve
try:
    CurveParams(p=23, a=0, b=0, n=1)
except ValueError as e:
    print(e)  # Singular curve: 4a³ + 27b² ≡ 0 ...
```

### Arithmetic with Operators

```python
from ecutils import Point, CurveParams

curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
P = Point(0, 1, curve)
Q = Point(6, 19, curve)

# Point addition
R = P + Q
print(R)  # Point(x=3, y=13)

# Point subtraction
S = P - Q
print(S)  # Point(x=0, y=22)

# Negation (additive inverse)
neg_P = -P
print(neg_P)  # Point(x=0, y=22)

# Scalar multiplication
T = 5 * P
print(T)  # Point(x=18, y=3)

# Commutative scalar multiplication
U = P * 5
print(U)  # Point(x=18, y=3)

# Equality
print(T == U)  # True
print(P == Q)  # False
```

### Using Pre-defined Curves

```python
from ecutils import get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

# Private key → public key
private_key = 0xDEADBEEFCAFE
public_key = private_key * G

print(public_key)                # Point(x=..., y=...)
print(public_key.is_on_curve())  # True
```

### Coordinate Systems

```python
from ecutils import Point, CurveParams, CoordinateSystem

# Jacobian coordinates (default — faster)
curve_jac = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Affine coordinates (explicit)
curve_aff = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)

# Both produce the same results
P_jac = Point(0, 1, curve_jac)
P_aff = Point(0, 1, curve_aff)

R_jac = 5 * P_jac
R_aff = 5 * P_aff

print(R_jac.x == R_aff.x and R_jac.y == R_aff.y)  # True
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
print(x, parity)  # 0 1

# Decompress: recover the full point
recovered = Point.decompress(x, parity, curve)
print(recovered)       # Point(x=0, y=1)
print(recovered == P)  # True
```

This also works with standard curves:

```python
from ecutils import Point, get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

x, parity = G.compress()
recovered = Point.decompress(x, parity, curve)

print(recovered.x == G.x and recovered.y == G.y)  # True
```

!!! warning
    Compressing the identity point (point at infinity) raises `ValueError`.
    Decompressing an x-coordinate that does not correspond to a valid curve
    point also raises `ValueError`.

### SEC 1 Format (Interoperable)

For interoperability with other libraries, ECUtils supports the SEC 1 / X9.62
standard format used by OpenSSL, Python `ecdsa`, `cryptography`, and others:

```python
from ecutils import Point, get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

# Compressed: 0x02|0x03 + x (33 bytes for secp256k1)
compressed = G.compress_sec1()
print(len(compressed))        # 33
print(hex(compressed[0]))     # 0x2 (even y) or 0x3 (odd y)

# Uncompressed: 0x04 + x + y (65 bytes for secp256k1)
uncompressed = G.to_uncompressed_sec1()
print(len(uncompressed))      # 65
print(hex(uncompressed[0]))   # 0x4

# Deserialize either format back to a Point
P1 = Point.from_sec1(compressed, curve)
P2 = Point.from_sec1(uncompressed, curve)

print(P1 == P2)  # True
print(P1 == G)   # True
```

See [Migration Guides](migration-guides.md) for complete examples of
interoperability with `ecdsa` and `cryptography`.

## Encoding Messages with Koblitz

Convert text into elliptic curve points and back:

```python
from ecutils import Koblitz

kob = Koblitz(curve_name="secp521r1")

# Encode a message
message = "Hello, world!"
point, j = kob.encode(message)
print(point)  # Point(x=..., y=...)

# Decode back
decoded = kob.decode(point, j)
print(decoded)            # Hello, world!
print(decoded == message)  # True
```

For Unicode support, specify a larger alphabet size:

```python
from ecutils import Koblitz

kob = Koblitz(curve_name="secp521r1", alphabet_size=2**16)

point, j = kob.encode("Hello!")
print(point)  # Point(x=..., y=...)

decoded = kob.decode(point, j)
print(decoded)  # Hello!
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
print(f"r = {r}")
print(f"s = {s}")

# Verify with the correct message
is_valid = ds.verify_message(ds.public_key, b"Secure communication", r, s)
print(f"Valid: {is_valid}")  # Valid: True

# Verify with a wrong message
is_wrong = ds.verify_message(ds.public_key, b"Tampered message", r, s)
print(f"Valid: {is_wrong}")  # Valid: False
```

### Advanced: Bring Your Own Hash

For full control over the hash function:

```python
import hashlib
from ecutils import DigitalSignature

private_key = 123456789
ds = DigitalSignature(private_key, curve_name="secp256k1")

# Hash the message yourself
message = b"Secure communication"
message_hash = int(hashlib.sha256(message).hexdigest(), 16)

# Sign the hash
r, s = ds.sign(message_hash)
print(f"r = {r}")
print(f"s = {s}")

# Verify with the same hash
is_valid = ds.verify(ds.public_key, message_hash, r, s)
print(f"Valid: {is_valid}")  # Valid: True

# Verify with a different hash
wrong_hash = int(hashlib.sha256(b"Wrong message").hexdigest(), 16)
is_wrong = ds.verify(ds.public_key, wrong_hash, r, s)
print(f"Valid: {is_wrong}")  # Valid: False
```

## Diffie-Hellman Key Exchange

Establish a shared secret between two parties:

```python
from ecutils import DiffieHellman

# Alice and Bob each have their own private key
alice = DiffieHellman(private_key=12345, curve_name="secp256k1")
bob = DiffieHellman(private_key=67890, curve_name="secp256k1")

# Each party can see the other's public key
print(f"Alice public key: {alice.public_key}")
print(f"Bob public key:   {bob.public_key}")

# Exchange public keys and compute shared secret
secret_alice = alice.compute_shared_secret(bob.public_key)
secret_bob = bob.compute_shared_secret(alice.public_key)

# Both arrive at the same shared point
print(f"Alice shared secret: {secret_alice}")
print(f"Bob shared secret:   {secret_bob}")
print(f"Secrets match: {secret_alice == secret_bob}")  # True
```

## Massey-Omura Three-Pass Protocol

Exchange a secret message without prior key exchange:

```python
from ecutils import MasseyOmura, Koblitz

# Encode message as a curve point
kob = Koblitz(curve_name="secp521r1")
M, j = kob.encode("secret message")
print(f"Original point: {M}")

# Alice and Bob each have their own private key
alice = MasseyOmura(private_key=0xA1, curve_name="secp521r1")
bob = MasseyOmura(private_key=0xB2, curve_name="secp521r1")

# Three passes
c1 = alice.encrypt(M)        # Alice encrypts and sends to Bob
c2 = bob.encrypt(c1)         # Bob encrypts and sends back to Alice
c3 = alice.decrypt(c2)       # Alice removes her encryption, sends to Bob
plaintext = bob.decrypt(c3)  # Bob removes his encryption, recovers M

# Verify the message was recovered correctly
decoded = kob.decode(plaintext, j)
print(f"Decoded: {decoded}")                    # Decoded: secret message
print(f"Match: {decoded == 'secret message'}")  # Match: True
```

## Math Utilities

ECUtils exposes low-level modular arithmetic utilities that are useful for
educational purposes and custom ECC implementations:

### Quadratic Residue Test

```python
from ecutils import is_quadratic_residue

# Is 4 a quadratic residue mod 23?  (Yes, because 2² ≡ 4 mod 23)
print(is_quadratic_residue(4, 23))  # True

# Is 5 a quadratic residue mod 23?
print(is_quadratic_residue(5, 23))  # False
```

### Modular Square Root

```python
from ecutils import modular_sqrt

# Compute √4 mod 23
r = modular_sqrt(4, 23)
print(r)           # 2 (or 21, since both are valid roots)
print(r * r % 23)  # 4 — confirms it's a valid root

# Returns None for non-residues
result = modular_sqrt(5, 23)
print(result)  # None
```

These functions are used internally by `Point.decompress()` and can be
useful when implementing custom point-recovery or encoding schemes.
