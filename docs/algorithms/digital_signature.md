# Digital Signature

The `DigitalSignature` module, provided by `ecutils.algorithms`, offers a secure way to generate and verify digital signatures using the Elliptic Curve Digital Signature Algorithm (ECDSA). This document provides a detailed explanation on how to use the `DigitalSignature` class and its methods.

## Digital Signature Class

The `DigitalSignature` class encapsulates the functionality of ECDSA signing and verification with a user's private and public keys. To perform these operations, the class interacts with an elliptic curve over a finite field defined by the class's `curve` property, providing essential parameters and operations for ECDSA.

### Initializing the Class

```python
from ecutils.algorithms import DigitalSignature

# The private key is a secret, large random integer.
private_key = 123456789
ds = DigitalSignature(private_key)
```

When you create an instance of the `DigitalSignature` class, you must pass a valid ECDSA private key, which is a large, secret integer that should be securely generated and stored. This private key is used to generate digital signatures.

### Generate a Signature

To create a digital signature for a given message, use the `generate_signature` method. The message must first be hashed using a reliable cryptographic hash function suitable for the security level desired.

```python
message_hash = hash('Your message here')

# r and s are the two components of an ECDSA signature.
r, s = ds.generate_signature(message_hash)
```

The `generate_signature` method computes an ECDSA signature based on the message's hash and returns a tuple `(r, s)`, which together represent the signature. These values should be securely transmitted or stored alongside the message for later verification.

### Verify a Signature

To confirm that a message hasn't been tampered with, you can check the validity of a signature received from a sender using the `verify_signature` static method. You'll need the public key associated with the private key used to sign the message, the hash of the message, and the signature's `(r, s)` tuple.

```python
public_key = ds.public_key
is_valid = DigitalSignature.verify_signature(public_key, message_hash, r, s)
```

The `verify_signature` method is a static method and does not require an instance of the `DigitalSignature` class to be called. It will return `True` if the signature is valid, and `False` otherwise.

## Public and Private Keys

The public-private key pair forms the foundation of the ECDSA digital signature scheme. The private key must remain secret, while the public key can be openly distributed without compromising the security of the signature.

- **Private Key**: An integer that is used to generate a digital signature.
- **Public Key**: A point on the elliptic curve that results from the multiplication of the private key and the curve's base point. The public key is used to verify signatures.

## Security Considerations

- **Key Generation**: Private keys should be generated using a cryptographically secure random number generator.
- **Key Storage**: Private keys are extremely sensitive and should be stored securely, such as in a hardware security module or a secure key store.
- **Message Hashing**: The message should be hashed using a secure and collision-resistant cryptographic hash function.
- **Signature Transmission**: The signature components `(r, s)` should be securely transmitted or stored. Any alteration in these values can invalidate the signature.

## Error Handling and Validation

Special care must be taken to ensure that the signature components `(r, s)` are valid. The `DigitalSignature` class may raise exceptions such as `ValueError` if an invalid signature is provided for verification. Always validate signatures through the `verify_signature` method.

By adhering to the provided documentation and best practices for generating and verifying digital signatures, you can ensure the integrity and authenticity of messages in your application.