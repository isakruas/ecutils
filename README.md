# Elliptic Curve Utils (ecutils)
[![Documentation Status](https://readthedocs.org/projects/ecutils/badge/?version=latest)](https://ecutils.readthedocs.io/en/latest/?badge=latest)
[![Latest Version](https://img.shields.io/pypi/v/ecutils.svg?style=flat)](https://pypi.python.org/pypi/ecutils/)
[![Downloads](https://static.pepy.tech/badge/ecutils)](https://pepy.tech/project/ecutils)
[![Downloads](https://static.pepy.tech/badge/ecutils/month)](https://pepy.tech/project/ecutils)
[![Downloads](https://static.pepy.tech/badge/ecutils/week)](https://pepy.tech/project/ecutils)
[![codecov](https://codecov.io/gh/isakruas/ecutils/branch/master/graph/badge.svg)](https://codecov.io/gh/isakruas/ecutils)

Elliptic Curve Utils, or `ecutils`, is a Python package that provides utilities for working with elliptic curves, particularly in the context of cryptography. It includes functionality for operations like point addition and scalar multiplication on curves, as well as higher-level protocols like key exchange and digital signatures.

## Features

- Implements common elliptic curve operations such as point addition and multiplication.
- Provides classes for encoding/decoding textual messages to and from elliptic curve points (e.g., Koblitz encoding).
- Supports several standardized elliptic curves including secp192k1, secp256r1, and secp521r1.
- Includes an implementation of the Elliptic Curve Digital Signature Algorithm (ECDSA) for signing messages and verifying signatures.
- Features key exchange protocols like Diffie-Hellman and Massey-Omura over elliptic curves.

## Installation

You can install the `ecutils` package using `pip`:

```bash
pip install ecutils
```

## Usage

### Encoding and Decoding Messages with Koblitz

```python
from ecutils.algorithms import Koblitz

# Initialize Koblitz with a specific curve
koblitz = Koblitz(curve_name="secp256k1")

# Encode a message to a curve point
point, j = koblitz.encode("Hello, World!")

# Decode the curve point back to a message
decoded_message = Koblitz.decode(point, j)
```

### Digital Signatures with ECDSA

```python
from ecutils.algorithms import DigitalSignature

# Create a DigitalSignature instance with your private key
ds = DigitalSignature(private_key=123456)

# Hash of your message
message_hash = hash('your message')

# Generate signature
r, s = ds.generate_signature(message_hash)

# Verify signature (typically on the receiver's side)
is_valid = ds.verify_signature(ds.public_key, message_hash, r, s)
```

### Diffie-Hellman Key Exchange

```python
from ecutils.protocols import DiffieHellman

# Alice's side
alice = DiffieHellman(private_key=12345)

# Bob's side
bob = DiffieHellman(private_key=67890)

# Alice computes her shared secret with Bob's public key
alice_shared_secret = alice.compute_shared_secret(bob.public_key)

# Bob computes his shared secret with Alice's public key
bob_shared_secret = bob.compute_shared_secret(alice.public_key)

# alice_shared_secret should be equal to bob_shared_secret
```

## Documentation

For more in-depth use and examples, check out the [official documentation](https://ecutils.readthedocs.io/en/latest/).

## Support

For issues, questions, or contributions, please refer to the project's [GitHub repository](https://github.com/isakruas/ecutils).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Don't forget to give this project a star if you find it useful! 🌟

## Cross-Platform Compiled Library

In addition to this Python module, there exists a cross-platform compiled library that offers similar functionalities. This library is available under the [Apache Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) license and can be found on the official website:

[ecutils - software distribution](https://d3llw48k0uhrwl.cloudfront.net/)

If you need an implementation outside of the Python environment or seek integration with other programming languages, this library might be an excellent alternative.

