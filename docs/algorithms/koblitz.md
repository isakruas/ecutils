# Koblitz

The `Koblitz` class offers a convenient way to perform encoding and decoding of textual messages using the mathematical properties of elliptic curves. This method is based on converting text to points on an elliptic curve and vice versa, which is useful in the context of cryptography.

## Usage

### Setup

To begin using the `Koblitz` class, you first need to instantiate it with a specific elliptic curve. The elliptic curve is chosen by name. For instance, you can use the `secp192k1` curve by specifying it in the constructor:

```python
from ecutils.algorithms import Koblitz

koblitz = Koblitz(curve_name='secp192k1')
```

### Encoding a message

The `encode` method of the `Koblitz` class takes a string message as input and converts it into a point on the specified elliptic curve. The message encoding process includes an integer `j` that might be needed during decoding.

Here's an example of how to encode a textual message:

```python
message = "Hello, world!"
point, j = koblitz.encode(message)
```

The `point` is an (x, y) tuple representing the coordinates of a point on the elliptic curve, while `j` is an integer modifier that will be required to accurately decode the message.

### Decoding a message

To decode a message, the `decode` method is used. It takes the encoded point and the `j` integer obtained during encoding. The method converts the point back into the original textual message.

Decoding is demonstrated in the following example:

```python
decoded_message = koblitz.decode(point, j)
```

After decoding, `decoded_message` should contain the same text that was originally encoded.

## Full example

Here is a complete example that demonstrates encoding and then decoding a message, which verifies that the original message and the decoded message are the same.

```python
from ecutils.algorithms import Koblitz

# Instantiate the Koblitz class with the desired elliptic curve
koblitz = Koblitz(curve_name="secp521r1")

# Original message to encode
original_message = "Koblitz encoding with elliptic curves!"

# Encoding the message to a point on the elliptic curve
encoded_point, j = koblitz.encode(original_message)

# Decoding the encoded point back into the original message
decoded_message = koblitz.decode(encoded_point, j)

# Confirm that the decoded message matches the original message
assert decoded_message == original_message, "The decoded message should match the original message."
```

## Notes and considerations

- The choice of elliptic curve can affect the security and efficiency of the encoding/decoding process. Make sure to choose an appropriate curve for your context.
- It is crucial to keep track of the modifier `j` obtained during the encoding process, as incorrect or missing `j` values will lead to inaccurate decoding.
- The implementation of the `Koblitz` class relies on mathematical properties of elliptic curves, and as such, it is crucial to ensure that the curve parameters and encoding/decoding methods are trustworthy and secure.

By following the examples and explanations provided above, you should be able to successfully encode and decode messages using the `Koblitz` class and elliptic curve cryptography methods.