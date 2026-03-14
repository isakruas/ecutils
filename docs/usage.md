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

Sign and verify messages:

```python
import hashlib
from ecutils import DigitalSignature

private_key = 123456789
ds = DigitalSignature(private_key, curve_name="secp256k1")

# Hash the message
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
