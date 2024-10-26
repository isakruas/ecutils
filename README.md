# ecutils

**Python Library for Elliptic Curve Cryptography**

[![Documentation Status](https://readthedocs.org/projects/ecutils/badge/?version=latest)](https://ecutils.readthedocs.io/en/stable/?badge=latest)
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

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Examples](#examples)
  - [Encoding and Decoding Messages with Koblitz](#encoding-and-decoding-messages-with-koblitz)
  - [Digital Signatures with ECDSA](#digital-signatures-with-ecdsa)
  - [Diffie-Hellman Key Exchange](#diffie-hellman-key-exchange)
  - [Massey-Omura Key Exchange](#massey-omura-key-exchange)
- [Support](#support)
- [License](#license)
- [Language-Specific Libraries for Elliptic Curve Cryptography](#language-specific-libraries-for-elliptic-curve-cryptography)


## Installation

You can install the `ecutils` package using `pip`:

```bash
pip install ecutils
```

## Usage

After installing the `ecutils` library, you can import it into your Python project. Below are the steps for using the library:

```python
# Importing core classes and functions
from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve
from ecutils.settings import LRU_CACHE_MAXSIZE

# Importing protocols
from ecutils.protocols import DiffieHellman, MasseyOmura

# Importing algorithms
from ecutils.algorithms import Koblitz, DigitalSignature
```

## API Documentation

### Classes and Methods

#### Class: **`DigitalSignature`**

##### Constructor
- **`__init__(self, private_key, curve_name='secp192k1')`**
  - Creates a new instance of the `DigitalSignature` class for performing ECDSA (Elliptic Curve Digital Signature Algorithm) operations.
  - **Parameters**:
    - `private_key`: The private key used for generating a signature.
    - `curve_name`: (Optional) The name of the elliptic curve to use. Defaults to `'secp192k1'`.

##### Properties
- **`public_key`**
  - Retrieves the public key associated with the given private key, derived by multiplying the elliptic curve's generator point by the private key.
  - **Returns**: `Point` representing the public key of the signer.

##### Methods
- **`generate_signature(self, message_hash)`**
  - Generates an ECDSA signature for a given message hash using the private key.
  - **Parameters**:
    - `message_hash`: The hash of the message to be signed (string or bytes).
  - **Returns**: A tuple `(r: int, s: int)` representing the ECDSA signature components.

- **`verify_signature(self, public_key, message_hash, r, s)`**
  - Verifies the authenticity of an ECDSA signature `(r, s)` against a public key and a message hash.
  - **Parameters**:
    - `public_key`: The public key associated with the signature.
    - `message_hash`: The hash of the message that was signed (string or bytes).
    - `r`: The `r` component of the signature (int).
    - `s`: The `s` component of the signature (int).
  - **Returns**: `True` if the signature is valid; `False` otherwise.

---

#### Class: **`Koblitz`**

##### Constructor
- **`__init__(self, curve_name='secp521r1')`**
  - Creates a new instance of the `Koblitz` class for encoding and decoding messages on elliptic curves using the Koblitz method.
  - **Parameters**:
    - `curve_name`: (Optional) The name of the elliptic curve to use. Defaults to `'secp521r1'`.

##### Methods
- **`encode(self, message, alphabet_size=256, chunked=False)`**
  - Encodes a textual message into a point on the elliptic curve using the Koblitz method.
  - **Parameters**:
    - `message`: The string message to be encoded.
    - `alphabet_size`: (Optional) The size of the character set used in the message. Defaults to 256 (for ASCII).
    - `chunked`: (Optional) Set to `True` for encoding large messages in chunks. Defaults to `False`.
  - **Returns**: A tuple `(Point, int)` representing the encoded message as a point on the curve.

- **`decode(self, encoded, j=0, alphabet_size=256, chunked=False)`**
  - Decodes a point from the elliptic curve back into its corresponding textual message using the Koblitz method.
  - **Parameters**:
    - `encoded`: The point on the elliptic curve or tuple of points representing the encoded message.
    - `j`: (Optional) An auxiliary value used during encoding. Defaults to `0`.
    - `alphabet_size`: (Optional) The size of the character set used during encoding. Defaults to 256 (for ASCII).
    - `chunked`: (Optional) Set to `True` if the message was encoded in chunks. Defaults to `False`.
  - **Returns**: The decoded message as a string.

---

#### Class: **`DiffieHellman`**

##### Constructor
- **`__init__(self, private_key, curve_name='secp192k1')`**
  - Creates a new instance of the `DiffieHellman` class for performing Diffie-Hellman key exchange using elliptic curves.
  - **Parameters**:
    - `private_key`: The private key of the user.
    - `curve_name`: (Optional) The name of the elliptic curve to use. Defaults to `'secp192k1'`.

##### Properties
- **`public_key`**
  - Retrieves the public key associated with the given private key, derived by multiplying the elliptic curve's generator point by the private key.
  - **Returns**: `Point` representing the user's public key.

##### Methods
- **`compute_shared_secret(self, other_public_key)`**
  - Computes the shared secret using the private key and the other party’s public key.
  - **Parameters**:
    - `other_public_key`: The other party's public key.
  - **Returns**: The shared secret as a `Point`.

---

#### Class: **`MasseyOmura`**

##### Constructor
- **`__init__(self, private_key, curve_name='secp192k1')`**
  - Creates a new instance of the `MasseyOmura` class for performing the Massey-Omura key exchange using elliptic curves.
  - **Parameters**:
    - `private_key`: The private key of the user.
    - `curve_name`: (Optional) The name of the elliptic curve to use. Defaults to `'secp192k1'`.

##### Properties
- **`public_key`**
  - Retrieves the public key associated with the given private key, derived by multiplying the elliptic curve's generator point by the private key.
  - **Returns**: `Point` representing the user's public key.

##### Methods
- **`first_encryption_step(self, message)`**
  - Applies the first encryption step by encrypting the provided message using the user's private key.
  - **Parameters**:
    - `message`: The original message as a `Point`.
  - **Returns**: The encrypted message as a `Point`.

- **`second_encryption_step(self, received_encrypted_message)`**
  - Applies the second encryption step by encrypting the received later message using the user's private key.
  - **Parameters**:
    - `received_encrypted_message`: The encrypted message received from the other party.
  - **Returns**: The resulting encrypted message as a `Point`.

- **`partial_decryption_step(self, encrypted_message)`**
  - Applies a partial decryption using the inverse of the private key.
  - **Parameters**:
    - `encrypted_message`: The encrypted message as a `Point`.
  - **Returns**: A partially decrypted `Point`.

---

#### Class: **`EllipticCurve`**

##### Constructor
- **`__init__(self, p, a, b, G, n, h, use_projective_coordinates=True)`**
  - Creates a new instance of the `EllipticCurve` class to define the elliptic curve parameters and available mathematical operations.
  - **Parameters**:
    - `p`: The prime order of the finite field.
    - `a`: The coefficient `a` in the elliptic curve equation.
    - `b`: The coefficient `b` in the elliptic curve equation.
    - `G`: The base point/origin of the curve (point generator).
    - `n`: The order of the base point.
    - `h`: The cofactor of the elliptic curve.
    - `use_projective_coordinates`: (Optional) Whether to use Jacobian/projective coordinate systems for efficient point operations. Defaults to `True`.

##### Methods
- **`add_points(self, p1, p2)`**
  - Adds two points `p1` and `p2` on the elliptic curve.
  - **Parameters**:
    - `p1`: Point on the elliptic curve.
    - `p2`: Another point to be added.
  - **Returns**: `Point` representing the sum of the two points.

- **`double_point(self, p)`**
  - Doubles a point on the elliptic curve.
  - **Parameters**:
    - `p`: The point on the elliptic curve to be doubled.
  - **Returns**: The resulting `Point`.

- **`multiply_point(self, k, p)`**
  - Multiplies a point by an integer scalar `k` on the elliptic curve.
  - **Parameters**:
    - `k`: The integer scalar to multiply by.
    - `p`: The point to be multiplied.
  - **Returns**: The resulting `Point`.

- **`is_point_on_curve(self, p)`**
  - Checks whether a point lies on the elliptic curve.
  - **Parameters**:
    - `p`: The point to check.
  - **Returns**: `True` if the point is on the curve; `False` otherwise.

For more in-depth use and examples, check out the [official documentation](https://ecutils.readthedocs.io/en/stable/).

## Examples

In the following examples, you'll see how to use ecutils for essential elliptic curve operations and cryptographic protocols, including message encoding, digital signatures with ECDSA, and key exchange methods. These practical implementations will help you quickly integrate elliptic curve cryptography into your applications.

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

### Massey-Omura Key Exchange

```python
from ecutils.protocols import MasseyOmura
from ecutils.algorithms import Koblitz

# Initialize the Koblitz instance for the elliptic curve 'secp192k1'
koblitz = Koblitz(curve_name='secp192k1')

# Sender's side
# -------------
# Sender chooses their private key
private_key_sender = 123456789
# Initialize Massey-Omura protocol with the sender's private key
mo_sender = MasseyOmura(private_key_sender, curve_name='secp192k1')

# Encode the message using the Koblitz method
# `j` is used to handle the ambiguity in the decoding process
message, j = koblitz.encode("Hello, world!")

# Perform the first encryption step with Massey-Omura protocol
encrypted_msg_sender = mo_sender.first_encryption_step(message)

# The encoded message is now sent to the receiver...
# (transmission of encrypted_msg_sender)

# Receiver's side
# ---------------
# Receiver chooses their private key
private_key_receiver = 987654321
# Initialize Massey-Omura protocol with the receiver's private key
mo_receiver = MasseyOmura(private_key_receiver, curve_name='secp192k1')

# Perform the second encryption step with Massey-Omura protocol
encrypted_msg_receiver = mo_receiver.second_encryption_step(encrypted_msg_sender)

# The double-encrypted message is sent back to the sender...
# (transmission of encrypted_msg_receiver)

# Sender's side again
# -------------------
# Perform the partial decryption step with Massey-Omura protocol
partial_decrypted_msg = mo_sender.partial_decryption_step(encrypted_msg_receiver)

# The partially decrypted message is sent back to the receiver...
# (transmission of partial_decrypted_msg)

# Receiver's final decryption
# ---------------------------
# Finish decryption with Massey-Omura protocol to get the original message
original_message = mo_receiver.partial_decryption_step(partial_decrypted_msg)

# Decode the message using the Koblitz method
# `j` is used to resolve the mapping from the elliptic curve point back to the message
decoded_message = koblitz.decode(original_message, j)

# The decoded_message contains the original plaintext message
print(decoded_message)
```

## Support

For issues, questions, or contributions, please refer to the project's [GitHub repository](https://github.com/isakruas/ecutils).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Don't forget to give this project a star if you find it useful! 🌟

## Language-Specific Libraries for Elliptic Curve Cryptography

In addition to the Python module, there are other language-specific libraries available for elliptic curve cryptography:

- **JavaScript Library for Elliptic Curve Cryptography**: The `js-ecutils` package provides elliptic curve functionalities tailored for JavaScript developers. You can find it on [GitHub](https://github.com/isakruas/js-ecutils).

- **Go Library for Elliptic Curve Cryptography**: The `go-ecutils` library offers similar elliptic curve utilities for Go developers. More information and documentation can be found on [GitHub](https://github.com/isakruas/go-ecutils).

These libraries enable developers to utilize elliptic curve cryptography in their preferred programming environments, ensuring flexibility and ease of integration.
