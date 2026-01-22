# Security Considerations

This document outlines important security considerations when using ECUtils for cryptographic applications. While ECUtils provides robust implementations of elliptic curve algorithms, proper usage is essential for maintaining security.

## Intended Use

ECUtils is designed for:

- **Educational purposes:** Learning about elliptic curve cryptography
- **Prototyping:** Rapid development of cryptographic systems
- **Research:** Experimenting with ECC algorithms and protocols

For production systems with high-security requirements, consider using battle-tested libraries like `cryptography` or hardware security modules (HSMs).

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

Always hash messages before signing. The hash function should match the security level of the curve:

```python
import hashlib

# For secp256r1, use SHA-256
message = b"Your message here"
message_hash = int.from_bytes(hashlib.sha256(message).digest(), "big")

# For secp384r1, use SHA-384
message_hash = int.from_bytes(hashlib.sha384(message).digest(), "big")

# For secp521r1, use SHA-512
message_hash = int.from_bytes(hashlib.sha512(message).digest(), "big")
```

### Nonce Generation

ECUtils generates random nonces internally for signature generation. The security of ECDSA critically depends on:

1. **Unique nonces:** Each signature must use a different nonce
2. **Unpredictable nonces:** Nonces must be cryptographically random
3. **Secret nonces:** Nonces must never be disclosed

Reusing a nonce with the same private key allows an attacker to recover the private key.

### Signature Verification

Always verify signatures before trusting signed data:

```python
is_valid = ds.verify_signature(public_key, message_hash, r, s)
if not is_valid:
    raise SecurityError("Invalid signature")
```

## Key Exchange Protocols

### Diffie-Hellman (ECDH)

The shared secret from ECDH should never be used directly as an encryption key. Always derive keys using a Key Derivation Function (KDF):

```python
import hashlib

# Compute shared secret
shared_point = dh.compute_shared_secret(other_public_key)

# Derive encryption key using HKDF or similar
shared_bytes = shared_point.x.to_bytes(32, 'big')
encryption_key = hashlib.sha256(shared_bytes).digest()
```

### Public Key Validation

Always validate received public keys to prevent invalid curve attacks:

```python
from ecutils.curves import get

curve = get("secp256r1")

# Validate that the point is on the curve
if not curve.is_point_on_curve(received_public_key):
    raise SecurityError("Invalid public key")
```

## Koblitz Encoding

Koblitz encoding is intended for message embedding, not encryption. For secure communication:

1. Use Koblitz to encode the message to a point
2. Encrypt the point using a secure protocol (e.g., ElGamal, ECIES)
3. Never transmit encoded points without encryption

## Side-Channel Considerations

### Timing Attacks

ECUtils uses Python's built-in `pow()` function for modular exponentiation, which provides some timing attack resistance. However, for high-security applications:

- Avoid exposing timing information to potential attackers
- Consider constant-time implementations for sensitive operations
- Use hardware security modules for critical operations

### Cache Timing

The LRU cache can potentially leak information through cache timing:

- Cache hits are faster than cache misses
- An attacker with timing access might infer information about operations

For highly sensitive applications, consider disabling the cache:

```python
from ecutils import settings
settings.LRU_CACHE_MAXSIZE = 0
```

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
2. **Hash messages** before signing with an appropriate hash function
3. **Validate public keys** received from untrusted sources
4. **Derive encryption keys** from ECDH shared secrets using a KDF
5. **Use appropriate curve sizes** for your security requirements
6. **Keep private keys secret** and store them securely
7. **Update regularly** to receive security fixes

## Reporting Security Issues

If you discover a security vulnerability in ECUtils, please report it responsibly by opening a private security advisory on the [GitHub repository](https://github.com/isakruas/ecutils/security/advisories).
