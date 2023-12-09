# Diffie-Hellman

The `DiffieHellman` class facilitates the Diffie-Hellman key exchange using elliptic curves.

## Methods

### compute_shared_secret

Computes a shared secret based on a private key and the other party's public key.

```python
from ecutils.protocols import DiffieHellman

private_key = ...
dh = DiffieHellman(private_key)

other_public_key = ...

shared_secret = dh.compute_shared_secret(other_public_key)
```