# Koblitz

The `Koblitz` class implements the Koblitz method for encoding and decoding textual messages using elliptic curves.

## Methods

### encode

Encodes a textual message to a curve point.

```python
from ecutils.algorithms import Koblitz

koblitz = Koblitz(curve_name='secp192k1')
point, j = koblitz.encode('Hello, world!')
```

### decode

Decodes a point on an elliptic curve back to a textual message.

```python
from ecutils.algorithms import Koblitz

point = Point(...)
j = ...

message = Koblitz.decode(point, j)
```