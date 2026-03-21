# Migration Guides

This page shows how to migrate to ECUtils from other Python ECC libraries,
or how to use them together. Every example is a complete, runnable workflow.

## Migrating from `ecdsa`

The [`ecdsa`](https://pypi.org/project/ecdsa/) library is one of the most
popular pure-Python ECC packages. Below are side-by-side comparisons
showing how each task is done in `ecdsa` vs. ECUtils.

### Key Generation

=== "Before (ecdsa)"

    ```python
    from ecdsa import SECP256k1, SigningKey

    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    print(vk.to_string("compressed").hex())
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import get_curve, get_generator

    curve = get_curve("secp256k1")
    G = get_generator("secp256k1")

    private_key = secrets.randbelow(curve.n - 1) + 1
    public_key = private_key * G

    print(public_key.compress_sec1().hex())
    ```

### Signing a Message

=== "Before (ecdsa)"

    ```python
    import hashlib
    from ecdsa import SECP256k1, SigningKey

    sk = SigningKey.generate(curve=SECP256k1)
    message = b"Hello, world!"

    # ecdsa hashes internally by default (sha1), or you pass hashfunc
    signature = sk.sign(message, hashfunc=hashlib.sha256)
    print(signature.hex())
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import DigitalSignature, get_curve

    curve = get_curve("secp256k1")
    private_key = secrets.randbelow(curve.n - 1) + 1

    ds = DigitalSignature(private_key, curve_name="secp256k1")
    r, s = ds.sign_message(b"Hello, world!")  # SHA-256 applied internally

    print(f"r = {r}")
    print(f"s = {s}")
    ```

### Verifying a Signature

=== "Before (ecdsa)"

    ```python
    import hashlib
    from ecdsa import SECP256k1, SigningKey, BadSignatureError

    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    message = b"Hello, world!"

    signature = sk.sign(message, hashfunc=hashlib.sha256)

    try:
        vk.verify(signature, message, hashfunc=hashlib.sha256)
        print("Valid")
    except BadSignatureError:
        print("Invalid")
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import DigitalSignature, get_curve

    curve = get_curve("secp256k1")
    private_key = secrets.randbelow(curve.n - 1) + 1

    ds = DigitalSignature(private_key, curve_name="secp256k1")
    message = b"Hello, world!"

    r, s = ds.sign_message(message)
    is_valid = ds.verify_message(ds.public_key, message, r, s)

    print("Valid" if is_valid else "Invalid")  # Valid
    ```

### Importing an `ecdsa` Public Key into ECUtils

If you have an existing system using `ecdsa` and want to verify or
operate on its keys in ECUtils:

```python
from ecdsa import SECP256k1, SigningKey
from ecutils import Point, get_curve

# --- Generate key in ecdsa ---
sk = SigningKey.generate(curve=SECP256k1)
vk = sk.get_verifying_key()

# Export as SEC 1 compressed bytes
ecdsa_pub_bytes = vk.to_string("compressed")

# --- Import into ecutils ---
curve = get_curve("secp256k1")
pub = Point.from_sec1(ecdsa_pub_bytes, curve)

print(pub)                  # Point(x=..., y=...)
print(pub.is_on_curve())    # True

# Now you can do EC arithmetic
doubled = pub + pub
scalar_mul = 42 * pub
print(doubled)              # Point(x=..., y=...)
print(scalar_mul)           # Point(x=..., y=...)
```

### Exporting an ECUtils Public Key to `ecdsa`

If you generated a key in ECUtils and need to use it with `ecdsa`:

```python
import secrets
from ecutils import get_curve, get_generator
from ecdsa import SECP256k1, VerifyingKey

# --- Generate key in ecutils ---
curve = get_curve("secp256k1")
G = get_generator("secp256k1")
private_key = secrets.randbelow(curve.n - 1) + 1
pub = private_key * G

# Export as SEC 1 compressed bytes
sec1_bytes = pub.compress_sec1()

# --- Import into ecdsa ---
vk = VerifyingKey.from_string(sec1_bytes, curve=SECP256k1)

print(vk.to_string("compressed").hex())
```

### Curve Name Mapping

| ecdsa | ecutils |
|-------|---------|
| `SECP256k1` | `"secp256k1"` |
| `NIST192p` | `"secp192r1"` |
| `NIST224p` | `"secp224r1"` |
| `NIST256p` | `"secp256r1"` |
| `NIST384p` | `"secp384r1"` |
| `NIST521p` | `"secp521r1"` |

---

## Migrating from `cryptography`

The [`cryptography`](https://pypi.org/project/cryptography/) library is the
most widely used Python crypto package, backed by OpenSSL. It uses a very
different API style (builder pattern, serialization formats).

### Key Generation

=== "Before (cryptography)"

    ```python
    from cryptography.hazmat.primitives.asymmetric import ec

    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    print(public_key.key_size)  # 256
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import get_curve, get_generator

    curve = get_curve("secp256k1")
    G = get_generator("secp256k1")

    private_key = secrets.randbelow(curve.n - 1) + 1
    public_key = private_key * G

    print(public_key)                # Point(x=..., y=...)
    print(public_key.is_on_curve())  # True
    ```

### Signing a Message

=== "Before (cryptography)"

    ```python
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, utils

    private_key = ec.generate_private_key(ec.SECP256K1())
    message = b"Hello, world!"

    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    # signature is DER-encoded (r, s)
    r, s = utils.decode_dss_signature(signature)

    print(f"r = {r}")
    print(f"s = {s}")
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import DigitalSignature, get_curve

    curve = get_curve("secp256k1")
    private_key = secrets.randbelow(curve.n - 1) + 1

    ds = DigitalSignature(private_key, curve_name="secp256k1")
    r, s = ds.sign_message(b"Hello, world!")
    # r, s are plain integers — no DER encoding

    print(f"r = {r}")
    print(f"s = {s}")
    ```

### Verifying a Signature

=== "Before (cryptography)"

    ```python
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from cryptography.exceptions import InvalidSignature

    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    message = b"Hello, world!"

    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(signature)

    der_sig = utils.encode_dss_signature(r, s)
    try:
        public_key.verify(der_sig, message, ec.ECDSA(hashes.SHA256()))
        print("Valid")
    except InvalidSignature:
        print("Invalid")
    ```

=== "After (ecutils)"

    ```python
    import secrets
    from ecutils import DigitalSignature, get_curve

    curve = get_curve("secp256k1")
    private_key = secrets.randbelow(curve.n - 1) + 1

    ds = DigitalSignature(private_key, curve_name="secp256k1")
    message = b"Hello, world!"

    r, s = ds.sign_message(message)
    is_valid = ds.verify_message(ds.public_key, message, r, s)

    print("Valid" if is_valid else "Invalid")  # Valid
    ```

### Importing a `cryptography` Public Key into ECUtils

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat,
)
from ecutils import Point, get_curve

# --- Generate key in cryptography ---
private_key = ec.generate_private_key(ec.SECP256K1())
pub_bytes = private_key.public_key().public_bytes(
    Encoding.X962, PublicFormat.CompressedPoint
)

# --- Import into ecutils ---
curve = get_curve("secp256k1")
pub = Point.from_sec1(pub_bytes, curve)

print(pub)                  # Point(x=..., y=...)
print(pub.is_on_curve())    # True

# EC arithmetic works immediately
doubled = pub + pub
scalar_mul = 42 * pub
print(doubled)              # Point(x=..., y=...)
print(scalar_mul)           # Point(x=..., y=...)
```

### Exporting an ECUtils Public Key to `cryptography`

```python
import secrets
from ecutils import get_curve, get_generator
from cryptography.hazmat.primitives.asymmetric import ec

# --- Generate key in ecutils ---
curve = get_curve("secp256k1")
G = get_generator("secp256k1")
private_key = secrets.randbelow(curve.n - 1) + 1
pub = private_key * G

# Export as SEC 1 compressed bytes
sec1_bytes = pub.compress_sec1()

# --- Import into cryptography ---
crypto_pub = ec.EllipticCurvePublicKey.from_encoded_point(
    ec.SECP256K1(), sec1_bytes
)

print(crypto_pub.key_size)  # 256
```

### Diffie-Hellman: cryptography ↔ ecutils

A complete ECDH key exchange where one party uses `cryptography` and the
other uses ECUtils:

```python
import secrets
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat,
)
from ecutils import DiffieHellman, Point, get_curve

curve = get_curve("secp256k1")

# --- Alice (cryptography) ---
alice_sk = ec.generate_private_key(ec.SECP256K1())
alice_pub_bytes = alice_sk.public_key().public_bytes(
    Encoding.X962, PublicFormat.CompressedPoint
)

# --- Bob (ecutils) ---
bob = DiffieHellman(
    private_key=secrets.randbelow(curve.n - 1) + 1,
    curve_name="secp256k1",
)
bob_pub_bytes = bob.public_key.compress_sec1()

# --- Bob computes shared secret (ecutils) ---
alice_pub = Point.from_sec1(alice_pub_bytes, curve)
bob_shared = bob.compute_shared_secret(alice_pub)

# --- Alice computes shared secret (cryptography) ---
bob_crypto_pub = ec.EllipticCurvePublicKey.from_encoded_point(
    ec.SECP256K1(), bob_pub_bytes
)
alice_shared = alice_sk.exchange(ec.ECDH(), bob_crypto_pub)

# Both arrive at the same x-coordinate
bob_shared_bytes = bob_shared.x.to_bytes(32, "big")
assert alice_shared == bob_shared_bytes

print("Shared secrets match!")
```

### Curve Name Mapping

| cryptography | ecutils |
|--------------|---------|
| `ec.SECP256K1()` | `"secp256k1"` |
| `ec.SECP192R1()` | `"secp192r1"` |
| `ec.SECP224R1()` | `"secp224r1"` |
| `ec.SECP256R1()` | `"secp256r1"` |
| `ec.SECP384R1()` | `"secp384r1"` |
| `ec.SECP521R1()` | `"secp521r1"` |

---

## Why Migrate?

| Aspect | `ecdsa` | `cryptography` | **ecutils** |
|--------|---------|----------------|-------------|
| **Dependencies** | Pure Python | OpenSSL (C) | Pure Python, **zero deps** |
| **API style** | Object-oriented | Builder pattern | Operator overloading (`+`, `*`) |
| **EC arithmetic** | Not exposed | Not exposed | Full access (`P + Q`, `k * P`) |
| **Educational use** | Limited | Not designed for | Built for it |
| **Point compression** | Yes (SEC 1) | Yes (SEC 1) | Yes (SEC 1 + tuple) |
| **Koblitz encoding** | No | No | Yes |
| **Massey-Omura** | No | No | Yes |
| **Coordinate systems** | Affine only | Hidden (OpenSSL) | Affine + Jacobian (selectable) |
| **Production ready** | Yes | Yes | Educational / prototyping |

ECUtils is not a replacement for `cryptography` in production — it is
designed for learning, prototyping, and research where transparent access
to the math is more important than hardened security.
