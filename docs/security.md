# Security Considerations

This document outlines important security considerations when using ECUtils for cryptographic applications.

## Intended Use

ECUtils is designed for:

- **Educational purposes:** Learning about elliptic curve cryptography
- **Prototyping:** Rapid development of cryptographic systems
- **Research:** Experimenting with ECC algorithms and protocols

For production systems with high-security requirements, consider using battle-tested libraries like `cryptography` or hardware security modules (HSMs).

## Curve Validation

ECUtils automatically validates curves at construction time by checking the discriminant condition:

$$
\Delta = -16(4a^3 + 27b^2) \neq 0 \pmod{p}
$$

A zero discriminant means the curve is **singular** (has a cusp or node), which is cryptographically broken. Attempting to create a singular curve raises `ValueError`:

```python
from ecutils import CurveParams

# This raises ValueError — singular curve
CurveParams(p=23, a=0, b=0, n=1)
```

All curves in the built-in registry pass this validation.

!!! note "Order Considerations"
    For cryptographic security the group order *n* should be at least 2^160
    (NIST SP 800-57). ECUtils does not enforce a minimum order so that
    small "toy" curves can be used for educational purposes.

## Key Generation

### Private Keys

Private keys must be generated using cryptographically secure random number generators:

```python
import secrets

# SECURE: Use secrets module for cryptographic randomness
private_key = secrets.randbits(256)

# INSECURE: Never use random module for cryptographic keys
# import random
# private_key = random.randint(1, n-1)  # DO NOT USE
```

### Key Size Recommendations

| Security Level | Recommended Curve | Key Size |
|----------------|-------------------|----------|
| 80-bit         | secp192k1/r1      | 192 bits |
| 112-bit        | secp224k1/r1      | 224 bits |
| 128-bit        | secp256k1/r1      | 256 bits |
| 192-bit        | secp384r1         | 384 bits |
| 256-bit        | secp521r1         | 521 bits |

For new applications, **secp256r1** or higher is recommended.

## Digital Signatures

### Message Hashing

Always hash messages before signing. The `sign_message()` and `verify_message()` convenience methods handle SHA-256 hashing automatically:

```python
from ecutils import DigitalSignature

ds = DigitalSignature(private_key=123456, curve_name="secp256k1")

# Automatic SHA-256 hashing
r, s = ds.sign_message(b"Your message here")
ds.verify_message(ds.public_key, b"Your message here", r, s)
```

For manual hashing, match the hash function to the curve's security level:

```python
import hashlib

# For secp256r1, use SHA-256
message_hash = int.from_bytes(hashlib.sha256(message).digest(), "big")

# For secp384r1, use SHA-384
message_hash = int.from_bytes(hashlib.sha384(message).digest(), "big")

# For secp521r1, use SHA-512
message_hash = int.from_bytes(hashlib.sha512(message).digest(), "big")
```

### Nonce Security (Critical)

ECUtils generates random nonces internally for signature generation. The security of ECDSA critically depends on:

1. **Unique nonces:** Each signature must use a different nonce
2. **Unpredictable nonces:** Nonces must be cryptographically random
3. **Secret nonces:** Nonces must never be disclosed

!!! danger "Nonce Reuse Vulnerability"
    Reusing a nonce *k* with the same private key allows an attacker to
    recover the private key algebraically. This was famously exploited in
    the **2010 Sony PS3 attack**, where a static nonce in the ECDSA
    implementation allowed extraction of the private signing key,
    compromising the entire platform's code-signing infrastructure.

### Signature Verification

Always verify signatures before trusting signed data:

```python
is_valid = ds.verify(public_key, message_hash, r, s)
if not is_valid:
    raise SecurityError("Invalid signature")
```

## Key Exchange Protocols

### Diffie-Hellman (ECDH)

The shared secret from ECDH should never be used directly as an encryption key. Always derive keys using a Key Derivation Function (KDF):

```python
import hashlib
from ecutils import DiffieHellman

dh = DiffieHellman(private_key=0xA1, curve_name="secp256k1")

# Compute shared secret
shared_point = dh.compute_shared_secret(other_public_key)

# Derive encryption key using HKDF or similar
shared_bytes = shared_point.x.to_bytes(32, "big")
encryption_key = hashlib.sha256(shared_bytes).digest()
```

The security of ECDH is based on the **Elliptic Curve Discrete Logarithm Problem (ECDLP)**: given G and Q = d·G, it is computationally infeasible to recover the private scalar *d*.

### Public Key Validation

Points are automatically validated on construction when curve parameters are provided:

```python
from ecutils import Point, get_curve

curve = get_curve("secp256r1")

# This will raise ValueError if the point is not on the curve
try:
    p = Point(x=1, y=2, curve=curve)
except ValueError:
    print("Invalid point — not on the curve")
```

You can also check explicitly:

```python
point.is_on_curve()  # Returns True/False
```

## Point Compression Security

Point compression reduces storage from two coordinates to one (x + parity bit).
When decompressing, ECUtils computes the modular square root and validates the
result. An invalid x-coordinate (one that does not yield a quadratic residue)
is rejected with `ValueError`.

```python
from ecutils import Point, get_curve

curve = get_curve("secp256k1")

# Safe decompression with validation
try:
    P = Point.decompress(x=12345, parity=0, curve=curve)
except ValueError:
    print("Invalid compressed point")
```

## Koblitz Encoding

Koblitz encoding is intended for message embedding, not encryption. For secure communication:

1. Use Koblitz to encode the message to a point
2. Encrypt the point using a secure protocol (e.g., ElGamal, ECIES)
3. Never transmit encoded points without encryption

## Side-Channel Considerations

### Timing Attacks

ECUtils uses the double-and-add algorithm for scalar multiplication, which
is **not constant-time** — the number of additions depends on the Hamming
weight of the scalar. For background on secure implementations, see
[RFC 6090, Section 4](https://www.rfc-editor.org/rfc/rfc6090#section-4).

For high-security applications:

- Avoid exposing timing information to potential attackers
- Consider constant-time implementations for sensitive operations
- Use hardware security modules for critical operations

### Cache Timing

The LRU cache can potentially leak information through cache timing:

- Cache hits are faster than cache misses
- An attacker with timing access might infer information about operations

## Memory Security

Python does not provide guarantees about memory clearing. Sensitive data (private keys, nonces) may remain in memory after use. For high-security applications:

- Minimize the lifetime of sensitive data
- Consider using specialized secure memory handling
- Be aware that garbage collection timing is non-deterministic

## Supported Curves

All curves in ECUtils are standardized SECG curves that have been extensively analyzed:

| Curve | Standard | Notes |
|-------|----------|-------|
| secp192k1 | SECG | Koblitz curve |
| secp192r1 | NIST P-192 | Random curve |
| secp224k1 | SECG | Koblitz curve |
| secp224r1 | NIST P-224 | Random curve |
| secp256k1 | SECG | Used in Bitcoin |
| secp256r1 | NIST P-256 | Widely deployed |
| secp384r1 | NIST P-384 | High security |
| secp521r1 | NIST P-521 | Highest security |

## Best Practices Summary

1. **Use secure random number generation** for all keys and nonces
2. **Hash messages** before signing with an appropriate hash function (or use `sign_message()`)
3. **Validate public keys** received from untrusted sources
4. **Derive encryption keys** from ECDH shared secrets using a KDF
5. **Use appropriate curve sizes** for your security requirements
6. **Keep private keys secret** and store them securely
7. **Never reuse ECDSA nonces** — this leaks the private key
8. **Update regularly** to receive security fixes

## Reporting Security Issues

If you discover a security vulnerability in ECUtils, please report it responsibly by opening a private security advisory on the [GitHub repository](https://github.com/isakruas/ecutils/security/advisories).
