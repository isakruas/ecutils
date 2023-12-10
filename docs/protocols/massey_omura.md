# Massey-Omura

The Massey-Omura encryption protocol is a cryptographic scheme for key exchange based on the properties of elliptic curves. The protocol involves a sender and a receiver, both of which have their private keys, and allows the secure exchange of information without disclosing the keys used for encryption and decryption.

The `MasseyOmura` class provided by the `ecutils.protocols` module offers functionality to perform this cryptographic protocol using elliptic curves.

## Prerequisites

To use the Massey-Omura class, you need to understand the basics of elliptic curve cryptography and how elliptic curves can be used for encryption and decryption. Additionally, users should have some familiarity with the concepts of public and private keys in cryptography.

## Initialization

To initiate a Massey-Omura encryption or decryption process, instantiate the `MasseyOmura` class with a private key:

```python
from ecutils.protocols import MasseyOmura

private_key = 123456  # Replace with a chosen private key value
mo = MasseyOmura(private_key)
```

## Properties

- `curve`: The elliptic curve over which the encryption and decryption processes are carried out. By default, the curve used by the class is defined internally.

## Methods

### `first_encryption_step`

This method encodes a message point on the elliptic curve using the sender's private key. This encrypted message can then be sent to the receiver.

```python
from ecutils.protocols import Point

message = Point(...)
encrypted_message = mo.first_encryption_step(message)
```
- `message`: The elliptic curve point to be encrypted (the original data).
- Returns: An encrypted elliptic curve point.

### `second_encryption_step`

This method further encrypts the already encrypted message with the receiver's private key. The receiver should use this method upon receipt of the encrypted message from the sender.

```python
received_encrypted_message = Point(...)
encrypted_message = mo.second_encryption_step(received_encrypted_message)
```
- `received_encrypted_message`: An encrypted elliptic curve point from the sender.
- Returns: A doubly encrypted elliptic curve point.

### `partial_decryption_step`

This method applies partial decryption. It should be used during the exchanging process both by the sender and receiver to apply their private keys inversely to decrypt the message partly.

```python
encrypted_message = Point(...)
decrypted_message = mo.partial_decryption_step(encrypted_message)
```
- `encrypted_message`: An encrypted elliptic curve point (either doubly encrypted or after one half of the decryption process).
- Returns: A partial decrypted message if it is the sender using it; the original message if it is the receiver.

## Protocol Steps

Using the Massey-Omura class, the protocol flow goes like this:

1. The sender encrypts the message with their private key using `first_encryption_step`.
2. The encrypted message is sent to the receiver.
3. The receiver further encrypts the message with their private key using `second_encryption_step`.
4. This doubly encrypted message is sent back to the sender.
5. The sender applies `partial_decryption_step` to decrypt the message partially.
6. The sender sends this partially decrypted message back to the receiver.
7. Finally, the receiver uses `partial_decryption_step` to undo their own encryption, receiving the original message sent by the sender.

## Example of Use

Below is an example scenario of using `MasseyOmura` to encrypt and decrypt a message using elliptic curve cryptography:

```python
# Sender side
private_key_sender = 123456  # Sender's private key
mo_sender = MasseyOmura(private_key_sender)
# We assume `message` is a valid elliptic curve point representable by `Point`
encrypted_msg_sender = mo_sender.first_encryption_step(message)

# Sends `encrypted_msg_sender` to the receiver...

# Receiver side
private_key_receiver = 654321  # Receiver's private key
mo_receiver = MasseyOmura(private_key_receiver)
# The receiver further encrypts the message
encrypted_msg_receiver = mo_receiver.second_encryption_step(encrypted_msg_sender)

# Sends `encrypted_msg_receiver` back to the sender...

# Sender side
# The sender partially decrypts the message
partial_decrypted_msg = mo_sender.partial_decryption_step(encrypted_msg_receiver)

# Sends `partial_decrypted_msg` back to the receiver...

# Receiver side
# Finally, the receiver fully decrypts the message
original_message = mo_receiver.partial_decryption_step(partial_decrypted_msg)
```

After completing these steps, `original_message` is the same as the initial `message` that was encrypted by the sender, thus completing a secure exchange of information.