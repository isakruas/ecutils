# ECUtils Documentation

Welcome to the documentation for ECUtils, a pure Python library for elliptic curve cryptography (ECC). ECUtils provides a clean and straightforward interface for common ECC operations, algorithms, and protocols.

## Quick Start

```python
import hashlib
import secrets
from ecutils.algorithms import DigitalSignature

# Generate a private key and create a signature instance
private_key = secrets.randbits(256)
ds = DigitalSignature(private_key, curve_name="secp256r1")

# Sign a message
message = b"Hello, ECUtils!"
message_hash = int.from_bytes(hashlib.sha256(message).digest(), "big")
r, s = ds.generate_signature(message_hash)

# Verify the signature
is_valid = ds.verify_signature(ds.public_key, message_hash, r, s)
print(f"Valid: {is_valid}")  # Output: Valid: True
```

## Documentation Overview

### Getting Started

- **[Installation](installation.md):** How to install ECUtils via pip or from source.
- **[Usage Guide](usage.md):** Practical examples for common use cases.
- **[Configuration](configuration.md):** Customize cache size and coordinate systems.

### API Reference

- **[Core](reference/core.md):** `Point`, `JacobianPoint`, and `EllipticCurve` classes for fundamental operations.
- **[Algorithms](reference/algorithms.md):** `DigitalSignature` (ECDSA) and `Koblitz` encoding.
- **[Protocols](reference/protocols.md):** `DiffieHellman` (ECDH) and `MasseyOmura` key exchange.
- **[Curves](reference/curves.md):** Pre-configured curve parameters (secp192k1 through secp521r1).
- **[Utils](reference/utils.md):** Utility functions.

### Advanced Topics

- **[Benchmarks](benchmarks.md):** Performance data across configurations and curves.
- **[Security Considerations](security.md):** Best practices for secure implementations.

## Features

| Feature | Description |
|---------|-------------|
| **Core Operations** | Point addition, doubling, scalar multiplication |
| **Digital Signatures** | ECDSA sign and verify |
| **Key Exchange** | Diffie-Hellman (ECDH), Massey-Omura |
| **Message Encoding** | Koblitz method |
| **Supported Curves** | secp192k1/r1, secp224k1/r1, secp256k1/r1, secp384r1, secp521r1 |
| **Performance** | LRU caching, Jacobian coordinates |

## Supported Curves

| Curve | Key Size | Common Use |
|-------|----------|------------|
| secp192k1 | 192-bit | Legacy |
| secp192r1 | 192-bit | NIST P-192 |
| secp224k1 | 224-bit | Legacy |
| secp224r1 | 224-bit | NIST P-224 |
| secp256k1 | 256-bit | Bitcoin, Ethereum |
| secp256r1 | 256-bit | TLS, NIST P-256 |
| secp384r1 | 384-bit | NIST P-384 |
| secp521r1 | 521-bit | NIST P-521 |

## License

ECUtils is available under the [MIT License](https://opensource.org/licenses/MIT), providing flexibility for both personal and commercial use. The MIT License is one of the least restrictive licenses favored in the open-source community for its minimal limitations.

By using ECUtils, you agree to the license terms, which allow you to:

- **Use** the software for any purpose.
- **Modify** it to suit your needs.
- **Distribute** the original or modified software.
- **Include** the software in your proprietary applications.

However, please be aware that the software comes "as is," with no warranty of any kind, whether express or implied. Under no circumstances shall the authors or copyright holders be liable for any claim, damages or other liabilities arising from the use of the software.

Before incorporating ECUtils, it's advised to read the full license text, available in the `LICENSE.md` file in the [source code repository](https://github.com/isakruas/ecutils/blob/master/LICENSE.md) or on the official website.

## Language-Specific Libraries for Elliptic Curve Cryptography

In addition to the Python module, there are other language-specific libraries available for elliptic curve cryptography:

- **JavaScript Library for Elliptic Curve Cryptography**: The `js-ecutils` package provides elliptic curve functionalities tailored for JavaScript developers. You can find it on [GitHub](https://github.com/isakruas/js-ecutils).

- **Go Library for Elliptic Curve Cryptography**: The `go-ecutils` library offers similar elliptic curve utilities for Go developers. More information and documentation can be found on [GitHub](https://github.com/isakruas/go-ecutils).

These libraries enable developers to utilize elliptic curve cryptography in their preferred programming environments, ensuring flexibility and ease of integration.
