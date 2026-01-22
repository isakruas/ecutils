# ecutils

**A Pythonic Elliptic Curve Cryptography Library**

[![CI](https://github.com/isakruas/ecutils/actions/workflows/ci.yml/badge.svg)](https://github.com/isakruas/ecutils/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/ecutils/badge/?version=latest)](https://ecutils.readthedocs.io/en/stable/?badge=latest)
[![PyPI Version](https://img.shields.io/pypi/v/ecutils.svg)](https://pypi.python.org/pypi/ecutils/)
[![PyPI Downloads](https://static.pepy.tech/badge/ecutils/month)](https://pepy.tech/project/ecutils)
[![codecov](https://codecov.io/gh/isakruas/ecutils/branch/master/graph/badge.svg)](https://codecov.io/gh/isakruas/ecutils)

`ecutils` is a pure Python library that provides a clean and straightforward interface for elliptic curve cryptography (ECC). Designed for educational purposes and for building secure systems, it implements common ECC operations, algorithms, and protocols with a focus on readability and ease of use.

## Features

- **Core Operations:** Point addition, doubling, and scalar multiplication on various curves.
- **Standard Curves:** Pre-configured parameters for `secp192k1`, `secp192r1`, `secp224k1`, `secp224r1`, `secp256k1`, `secp256r1`, `secp384r1`, and `secp521r1`.
- **Digital Signatures:** Implementation of the Elliptic Curve Digital Signature Algorithm (ECDSA).
- **Key Exchange Protocols:** Secure key exchange using Diffie-Hellman (ECDH) and Massey-Omura.
- **Message Encoding:** Koblitz's method for encoding messages to and from curve points.
- **Performance:** Optimized with LRU cache and Jacobian (projective) coordinates for faster computations.
- **Pure Python:** No external dependencies required.

## Installation

Install `ecutils` directly from PyPI:

```bash
pip install ecutils
```

## Quickstart: Digital Signatures (ECDSA)

Here's a quick example of how to generate and verify a digital signature.

```python
import hashlib
import secrets
from ecutils.algorithms import DigitalSignature

# 1. Generate a secure private key
# In a real application, this should be a securely generated and stored key.
private_key = secrets.randbits(256)

# 2. Create a DigitalSignature instance
# This automatically derives the public key.
ds = DigitalSignature(private_key, curve_name="secp256r1")

# 3. Prepare the message
# Always hash the message before signing.
message = b"This is a message to be signed."
message_hash = int.from_bytes(hashlib.sha256(message).digest(), "big")

# 4. Generate the signature
r, s = ds.generate_signature(message_hash)
print(f"Signature: (r={r}, s={s})")

# 5. Verify the signature
# This step would typically be done by the receiver, using the sender's public key.
is_valid = ds.verify_signature(ds.public_key, message_hash, r, s)

print(f"Signature is valid: {is_valid}")
# Output: Signature is valid: True
```

For more examples, including key exchange and message encoding, please check out our full [**documentation**](https://ecutils.readthedocs.io/en/stable/).

## Performance

ECUtils is optimized for performance using LRU caching and Jacobian coordinates. Here's a sample of signature operations on secp256r1:

| Configuration | Signature Generation | Signature Verification |
|---------------|---------------------|------------------------|
| Jacobian + LRU Cache | 0.02 ms | 0.04 ms |
| Jacobian (no cache) | 17.35 ms | 53.48 ms |
| Affine + LRU Cache | 0.07 ms | 0.11 ms |
| Affine (no cache) | 17.24 ms | 51.21 ms |

For complete benchmarks across all curves and operations, see the [Benchmarks documentation](https://ecutils.readthedocs.io/en/stable/benchmarks/).

## Supported Curves

| Curve | Key Size | Use Case |
|-------|----------|----------|
| secp192k1 | 192-bit | Legacy systems |
| secp192r1 | 192-bit | Legacy systems |
| secp224k1 | 224-bit | Moderate security |
| secp224r1 | 224-bit | Moderate security |
| secp256k1 | 256-bit | Bitcoin, Ethereum |
| secp256r1 | 256-bit | TLS, general purpose |
| secp384r1 | 384-bit | High security |
| secp521r1 | 521-bit | Maximum security |

## Documentation

- [Installation Guide](https://ecutils.readthedocs.io/en/stable/installation/)
- [Usage Examples](https://ecutils.readthedocs.io/en/stable/usage/)
- [Configuration](https://ecutils.readthedocs.io/en/stable/configuration/)
- [API Reference](https://ecutils.readthedocs.io/en/stable/reference/core/)
- [Security Considerations](https://ecutils.readthedocs.io/en/stable/security/)
- [Benchmarks](https://ecutils.readthedocs.io/en/stable/benchmarks/)

## Contributing

Contributions are welcome! Please read our [contributing guidelines](https://github.com/isakruas/ecutils/blob/master/CONTRIBUTING.md) to get started.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).