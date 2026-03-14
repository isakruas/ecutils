# ecutils

A pure Python library for Elliptic Curve Cryptography (ECC). Designed for educational purposes and for building secure systems.

[![CI](https://github.com/isakruas/ecutils/actions/workflows/ci.yml/badge.svg)](https://github.com/isakruas/ecutils/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/ecutils/badge/?version=latest)](https://ecutils.readthedocs.io/en/stable/?badge=latest)
[![PyPI Version](https://img.shields.io/pypi/v/ecutils.svg)](https://pypi.python.org/pypi/ecutils/)
[![PyPI Downloads](https://static.pepy.tech/badge/ecutils/month)](https://pepy.tech/project/ecutils)
[![codecov](https://codecov.io/gh/isakruas/ecutils/branch/master/graph/badge.svg)](https://codecov.io/gh/isakruas/ecutils)

## Installation

```bash
pip install ecutils
```

## Quick start

```python
from ecutils import Point, get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")

# Private key → public key
private_key = 0xDEADBEEFCAFE
public_key = private_key * G

print(public_key)                # Point(x=..., y=...)
print(public_key.is_on_curve())  # True
```

## Features

### Core

Arithmetic operations on elliptic curves `y² = x³ + ax + b (mod p)` with two internal coordinate systems.

```python
from ecutils import Point, CurveParams, CoordinateSystem

# Jacobian (default — faster)
curve = CurveParams(p=23, a=1, b=1, n=28, h=1)

# Affine (explicit)
curve = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)

P = Point(0, 1, curve)
Q = Point(6, 19, curve)

P + Q       # addition
P - Q       # subtraction
-P          # negation (additive inverse)
5 * P       # scalar multiplication
P * 5       # scalar multiplication (commutative)
P == Q      # equality
```

Points are automatically validated on construction:

```python
Point(0, 1, curve)   # ✅ valid
Point(0, 5, curve)   # ❌ ValueError: not on the curve
Point(curve=curve)   # ✅ point at infinity (identity)
```

### Pre-defined curves

```python
from ecutils import get_curve, get_generator

curve = get_curve("secp256k1")
G = get_generator("secp256k1")
```

Available curves: `secp192k1`, `secp192r1`, `secp224k1`, `secp224r1`, `secp256k1`, `secp256r1`, `secp384r1`, `secp521r1`.

### Protocols

#### Diffie-Hellman (ECDH)

Key exchange between two parties.

```python
from ecutils import DiffieHellman

alice = DiffieHellman(private_key=0xA1, curve_name="secp256k1")
bob   = DiffieHellman(private_key=0xB2, curve_name="secp256k1")

# Each party shares their public key
shared_alice = alice.compute_shared_secret(bob.public_key)
shared_bob   = bob.compute_shared_secret(alice.public_key)

assert shared_alice == shared_bob  # same shared secret
```

#### Massey-Omura

Three-pass protocol — no prior public key exchange required.

```python
from ecutils import MasseyOmura, Koblitz

# Encode message as a curve point
kob = Koblitz(curve_name="secp521r1")
M, j = kob.encode("secret message")

alice = MasseyOmura(private_key=0xA1, curve_name="secp521r1")
bob   = MasseyOmura(private_key=0xB2, curve_name="secp521r1")

# Three passes
c1 = alice.encrypt(M)        # Alice → Bob
c2 = bob.encrypt(c1)         # Bob → Alice
c3 = alice.decrypt(c2)       # Alice → Bob
plaintext = bob.decrypt(c3)  # Bob recovers M

assert kob.decode(plaintext, j) == "secret message"
```

### Algorithms

#### Digital Signature (ECDSA)

```python
import hashlib
from ecutils import DigitalSignature

signer = DigitalSignature(private_key=123456789, curve_name="secp256k1")

msg_hash = int(hashlib.sha256(b"hello").hexdigest(), 16)

# Sign
r, s = signer.sign(msg_hash)

# Verify
assert signer.verify(signer.public_key, msg_hash, r, s)
```

#### Koblitz (message encoding)

Encode text as curve points and decode back.

```python
from ecutils import Koblitz

kob = Koblitz(curve_name="secp521r1")

point, j = kob.encode("Hello, world!")
text = kob.decode(point, j)

assert text == "Hello, world!"
```

## Project structure

![ECUtils Module Structure](docs/assets/module_structure.svg)

```
ecutils/
├── __init__.py                  # Public API
├── py.typed                     # PEP 561 — type checker support
├── core/
│   ├── curve.py                 # CurveParams, CoordinateSystem
│   ├── point.py                 # Point
│   └── arithmetic/
│       ├── affine.py            # affine coordinate arithmetic
│       └── jacobian.py          # Jacobian coordinate arithmetic
├── curves/
│   └── registry.py              # pre-defined curves, get_curve(), get_generator()
├── protocols/
│   ├── diffie_hellman.py        # DiffieHellman
│   └── massey_omura.py          # MasseyOmura
├── algorithms/
│   ├── digital_signature.py     # DigitalSignature (ECDSA)
│   └── koblitz.py               # Koblitz
└── utils/
    └── settings.py              # global settings
```

## Contributing

Contributions are welcome! Please read our [contributing guidelines](https://github.com/isakruas/ecutils/blob/master/CONTRIBUTING.md) to get started.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).