# Massey-Omura

The Massey-Omura encryption protocol utilizes elliptic curve cryptography for the secure exchange of messages. This protocol ensures that two parties can communicate confidentially without disclosing their private keys. For those interested in implementing the Massey-Omura protocol in Python, the `MasseyOmura` class provides convenient functions to perform the necessary encryption and decryption steps.

### Prerequisites

Before using the `MasseyOmura` class, you should have a foundational understanding of elliptic curve cryptography (ECC) and the role of public and private keys in securing communications.

### Getting Started

To begin, you must create an instance of the `MasseyOmura` class with your private key:

```python
from ecutils.protocols import MasseyOmura

private_key = 123456  # Use your chosen private key
mo = MasseyOmura(private_key)
```

### Properties and Methods

- The `curve` property returns the elliptic curve used for cryptographic operations.

#### `first_encryption_step`

Encrypt a message point on the elliptic curve using the sender's private key:

```python
from ecutils.protocols import Point

message = Point(...)  # Ensure the message is a Point on the elliptic curve
encrypted_message = mo.first_encryption_step(message)
```

#### `second_encryption_step`

Incoming encrypted messages are further encrypted with the receiver's private key:

```python
received_encrypted_message = Point(...)  # This Point must be the encrypted message from the sender
encrypted_message = mo.second_encryption_step(received_encrypted_message)
```

#### `partial_decryption_step`

Apply partial decryption with either your private key or its inverse:

```python
encrypted_message = Point(...)  # This Point is either doubly encrypted or has undergone one step of decryption
decrypted_message = mo.partial_decryption_step(encrypted_message)
```

### Protocol Flow

Following is the sequence of steps in the Massey-Omura protocol:

1. Sender encrypts the message using `first_encryption_step`.
2. The encrypted message is sent to the receiver.
3. The receiver uses `second_encryption_step` to encrypt the message with their private key.
4. The receiver sends this doubly encrypted message to the sender.
5. Sender performs `partial_decryption_step` to decrypt the message partially.
6. Sender returns the partially decrypted message to the receiver.
7. Receiver finally uses `partial_decryption_step` to obtain the original message.

### Example Scenario

Here is a practical example of how you might use `MasseyOmura` to secure message exchange with elliptic curve cryptography:

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

Following these steps, `original_message` will match the initial `message` that the sender encrypted, completing a secure message exchange.