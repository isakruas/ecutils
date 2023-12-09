# Digital Signature

The `DigitalSignature` class provides methods for generating and verifying digital signatures using the ECDSA scheme.

## Methods

### generate_signature

Generates an ECDSA signature for a message hash.

```python
from ecutils.algorithms import DigitalSignature

private_key = ...
message_hash = hash('message')

ds = DigitalSignature(private_key)
r, s = ds.generate_signature(message_hash)
```

### verify_signature

Verifies the ECDSA signature against a message hash and public key.

```python
from ecutils.algorithms import DigitalSignature

public_key = ...
message_hash = ...
r = ...
s = ...

is_valid = DigitalSignature.verify_signature(public_key, message_hash, r, s)
```