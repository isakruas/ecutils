# Diffie-Hellman

The `DiffieHellman` class provides an easy-to-use implementation of the Diffie-Hellman key exchange protocol with a focus on elliptic curve cryptography. This protocol is a secure way for two parties to create a shared secret over an insecure channel, which can then be used to encrypt further communications using a symmetric-key algorithm.

## A Quick Overview

Imagine you want to whisper a secret to a friend in a room full of eavesdroppers. The Diffie-Hellman key exchange is like creating a shared secret language between you and your friend without anyone else catching on. It's all about using elliptic curve math to baffle the eavesdroppers (who represent potential attackers in our digital world).

## Introducing `DiffieHellman`

Let's get to know the `DiffieHellman` class, your toolkit for crafting private/public key pairs and doing the magical math that leads to a shared secret key.

### Getting Started

You'll start by creating a shiny new `DiffieHellman` instance:

```python
from ecutils.protocols import DiffieHellman

your_private_key = ...  # A secret number you pick and keep to yourself
dh = DiffieHellman(your_private_key)
```

Remember, your private key should be a big, random number that's for your eyes only! The corresponding public key will be out there for the world to see—but no worries, it won't spill any of your secrets.

### Attributes At Your Disposal
- `public_key`: This is your public key, which the `DiffieHellman` instance works out from your private key. You'll be sharing this with the other person to cook up that shared secret.

### Handy Methods

#### `compute_shared_secret(their_public_key)`
Use this method when you're ready to conjure up the shared secret using your private key and the other person's public key.

**Ingredients:**
- `their_public_key`: The public key of your friend in this game of secret whispers.

**What You'll Get:**
- The method returns a number—the shared secret. If both you and your friend follow the steps correctly, you'll both end up with the same magical number. This is what you'll use to create a key for your secret conversations.

**Here's How You Might Use It:**
```python
# Alice and Bob both have their private keys
private_key_alice = 12345
private_key_bob = 67890

# They each set up their DiffieHellman instances
dh_alice = DiffieHellman(private_key_alice)
dh_bob = DiffieHellman(private_key_bob)

# Alice takes Bob's public key to find their shared secret
shared_secret_alice = dh_alice.compute_shared_secret(dh_bob.public_key)

# Bob does the same with Alice's public key
shared_secret_bob = dh_bob.compute_shared_secret(dh_alice.public_key)

# Now, both Alice and Bob should have matching shared secrets
```

In real life, you'd use super secure methods to make your private keys, and you'd make sure public keys are swapped safely to keep those pesky eavesdroppers from stepping in. Once you've got your shared secret, it's common to put it through some extra steps (like hashing) to come up with the final key for your encrypted chats.

A Few Parting Tips:

- The strength of your Diffie-Hellman secret handshake depends on picking a tough elliptic curve and going for keys that are big enough to make the math really hard.
- Don't fall into the trap of using the same private key over and over—it's like wearing the same disguise every day, and eventually, someone will catch on. Changing your private key helps make sure that if one secret gets out, it won't spoil all the rest (that's what cryptographers call "forward secrecy").

Enjoy your secret conversations!