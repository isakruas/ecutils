# Usage

This section provides basic examples of how to use ECUtils. For detailed usage on specific modules, see the dedicated sections in this documentation.

Example of encoding a message using Koblitz:

```python
from ecutils.algorithms import Koblitz

koblitz = Koblitz(curve_name='secp192k1')
point, j = koblitz.encode('Hello, world!')
```

Example of creating a digital signature:

```python
from ecutils.algorithms import DigitalSignature

private_key = 123456789
message_hash = hash('message')

ds = DigitalSignature(private_key)
r, s = ds.generate_signature(message_hash)
```

Example of Diffie-Hellman key exchange protocol:

```python
from ecutils.protocols import DiffieHellman

# Alice's side
alice_private = 12345
alice_dh = DiffieHellman(alice_private)

# Bob's side
bob_private = 67890
bob_dh = DiffieHellman(bob_private)

# Both parties compute their shared secret
alice_shared_secret = alice_dh.compute_shared_secret(bob_dh.public_key)
bob_shared_secret = bob_dh.compute_shared_secret(alice_dh.public_key)
```