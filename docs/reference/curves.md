# Curves

The `curves` module offers predefined elliptic curve parameters used in cryptographic systems.

## Available Curves

- secp192k1
- secp192r1
- secp224k1
- secp224r1
- secp256k1
- secp256r1
- secp384r1
- secp521r1

## Usage

```python
from ecutils.curves import get

curve = get('secp192k1')
# Now you have the parameters of the secp192k1 curve.
```