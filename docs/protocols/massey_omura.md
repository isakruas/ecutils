# Massey-Omura

The `MasseyOmura` class supports the Massey-Omura encryption scheme using elliptic curves.

## Methods

### first_encryption_step

Encrypts the message with the sender's private key.

```python
from ecutils.protocols import MasseyOmura, Point

private_key = ...
mo = MasseyOmura(private_key)

message = Point(...)
encrypted_message = mo.first_encryption_step(message)
```

### second_encryption_step

Encrypts the message with the receiver's private key.

```python
from ecutils.protocols import MasseyOmura, Point

private_key = ...
mo = MasseyOmura(private_key)

received_encrypted_message = Point(...)
encrypted_message = mo.second_encryption_step(received_encrypted_message)
``` 

### partial_decryption_step

Applies partial decryption using the inverse of the sender's private key.

```python
from ecutils.protocols import MasseyOmura, Point

private_key = ...
mo = MasseyOmura(private_key)

encrypted_message = Point(...)
decrypted_message = mo.partial_decryption_step(encrypted_message)
```