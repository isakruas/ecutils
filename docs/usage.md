# Usage

This section provides basic guidance and example snippets for utilizing the `ecutils` library, which assists with Elliptic Curve Cryptography (ECC) related operations. Following these examples will help you integrate EC components such as Koblitz encoding, digital signatures, and Diffie-Hellman key exchanges into your applications.

For more detailed information on specific modules and their functionalities, refer to the corresponding sections in this documentation.

## Encoding Messages with Koblitz

The Koblitz module allows you to encode plaintext messages into points on an elliptic curve, providing a layer of cryptographic security for textual data.

Example:

```python
from ecutils.algorithms import Koblitz

# Initialize the Koblitz encoder with a named ECC curve.
koblitz = Koblitz(curve_name='secp192k1')

# Encode a message into an elliptic curve point.
message = 'Hello, world!'
encoded_point, j = koblitz.encode(message)

# `encoded_point` is now a tuple (x, y) representing a point on the curve.
# `j` is an integer used for accurately decoding the message later.
```

## Generating Digital Signatures

Using the Digital Signature module, you can generate secure and verifiable signatures for messages to ensure their authenticity and integrity.

Example:

```python
from ecutils.algorithms import DigitalSignature

# Define an ECDSA private key (should be generated securely).
private_key = 123456789

# Use a cryptographic hash function on the message first.
message = 'Secure communication'
message_hash = hash(message)

# Create an instance of DigitalSignature with your private key.
ds = DigitalSignature(private_key)

# Generate the signature for the message hash.
r, s = ds.generate_signature(message_hash)

# `r` and `s` constitute the digital signature for the given message hash.
```

## Performing the Diffie-Hellman Key Exchange

The Diffie-Hellman module enables two parties to establish a shared secret key over an insecure channel without exchanging their private keys, an essential process for secure two-way communication.

Example:

```python
from ecutils.protocols import DiffieHellman

# Initialize Diffie-Hellman instances with private keys for Alice and Bob.
alice_private = 12345
bob_private = 67890

alice_dh = DiffieHellman(alice_private)
bob_dh = DiffieHellman(bob_private)

# Alice computes the shared secret using Bob's public key.
alice_shared_secret = alice_dh.compute_shared_secret(bob_dh.public_key)

# Bob computes the shared secret using Alice's public key.
bob_shared_secret = bob_dh.compute_shared_secret(alice_dh.public_key)

# The shared secrets obtained by Alice and Bob (`alice_shared_secret` and
# `bob_shared_secret`) should now be the same, enabling secure communication.
```

Utilize these examples as a starting guide for incorporating ECC operations in your applications, whether it's for encoding textual data onto elliptic curves, securing messages with digital signatures, or safely exchanging cryptographic keys using the Diffie-Hellman protocol.