# Diffie-Hellman

The `DiffieHellman` class in the `ecutils.protocols` module provides an implementation of the Diffie-Hellman key exchange protocol using elliptic curve cryptography. This cryptographic protocol enables two parties to generate a shared secret over an insecure channel. The generated shared secret can subsequently be used to encrypt subsequent communications using a symmetric-key algorithm.

## Overview

The Diffie-Hellman key exchange is a method that allows two parties, each having an elliptic curve private key, to derive a shared secret over an unsecured channel without exchanging the private keys. This shared secret can then be used for secure communication. The strength of the Diffie-Hellman exchange lies in the difficulty of the discrete logarithm problem in elliptic curve groups.

## Class: `DiffieHellman`

The `DiffieHellman` class is designed to handle the creation of private/public key pairs and the computation of the shared secret key.

### Initialization

To create a new instance of the `DiffieHellman` class, you need to provide a private key.

```python
from ecutils.protocols import DiffieHellman

private_key = ...  # Your private key (an integer)
dh_instance = DiffieHellman(private_key)
```

The aforementioned private key should be a large randomly generated number that remains secret to the owner. The corresponding public key is computed and made publicly available.

### Attributes
- `public_key`: Once the `DiffieHellman` instance is initialized, this attribute holds the public key computed from the provided private key. The public key is what you will share with the other party for computing the shared secret.

### Methods

#### `compute_shared_secret(other_public_key)`
This method computes the shared secret using your private key and the other party's public key.

**Parameter:**
- `other_public_key`: The public key of the other party involved in the key exchange.

**Returns:**
- The method returns the shared secret, which is a number derived from the inputs, and remains the same for both parties if the process is followed correctly. This mutual secret is then often used to derive the encryption key for subsequent secure communications.

**Example usage:**
```python
# Assume you have the private key for Alice and Bob's instances of DiffieHellman
private_key_alice = 12345
private_key_bob = 67890

# Initialize DiffieHellman instances for Alice and Bob
dh_alice = DiffieHellman(private_key_alice)
dh_bob = DiffieHellman(private_key_bob)

# Alice gets Bob's public key and computes the shared secret
shared_secret_alice = dh_alice.compute_shared_secret(dh_bob.public_key)

# Bob gets Alice's public key and computes the shared secret
shared_secret_bob = dh_bob.compute_shared_secret(dh_alice.public_key)

# shared_secret_alice and shared_secret_bob should be identical at this point
```

In a real-world scenario, you would use secure methods to generate private keys and ensure that public keys are exchanged over a trusted channel or are verified by some form of authentication to prevent Man-in-the-Middle (MITM) attacks. After the shared secret is computed, it is usually further processed (e.g., hashed) to produce the final symmetric encryption key.

Note:

- The security of the Diffie-Hellman key exchange relies on selecting a secure elliptic curve and using appropriate-sized keys.
- It's crucial not to reuse the same private key for multiple key exchanges to maintain forward secrecy. Forward secrecy ensures that the compromise of one shared secret does not compromise past or future shared secrets.