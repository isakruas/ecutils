# Point

The `Point` class is a crucial component of the ECUtils module, representing a point on an elliptic curve which is the foundational element in elliptic curve-based cryptographic algorithms. The points on elliptic curves are used for various operations, such as point addition and scalar multiplication, which underpin the security of Elliptic Curve Cryptography (ECC).

## Description

In ECC, a `Point` typically consists of two coordinates `(x, y)` that satisfy the elliptic curve equation `y^2 = x^3 + ax + b`. These points can be added together or multiplied by a scalar to create new points on the curve. The `Point` class encapsulates this pair of coordinates along with other functionality necessary for ECC operations.

## Attributes

- **x** (Optional[int]): The x-coordinate of the point. This attribute represents the horizontal position of the point on the elliptic curve. If not provided, it defaults to `None`, which can represent the point at infinity for certain operations.
- **y** (Optional[int]): The y-coordinate of the point. This attribute represents the vertical position of the point on the elliptic curve. Similar to `x`, if not provided, it may signify the point at infinity.

## Initialization

To initialize a `Point`, you can provide the x and y coordinates as integer values. If either coordinate is not provided, the `Point` instance will represent a special point at infinity.

## Example Usage

The following example demonstrates how to create an instance of the `Point` class with specific x and y coordinates, thus defining a point on the elliptic curve.

```python
from ecutils.core import Point

# Instantiate a new Point
p = Point(x=10, y=20)

# Accessing the coordinates
print(f"The point has x-coordinate {p.x} and y-coordinate {p.y}.")
```

After creating a `Point`, it can be used in various operations specific to elliptic curves, such as adding it to another point or multiplying it by a scalar.

## Additional Considerations

When working with `Point` objects:

- Always ensure that the provided coordinates `(x, y)` actually lie on the intended elliptic curve, as not all pairs of coordinates correspond to valid points on the curve.
- Be aware that the arithmetic of `Point` instances must adhere to the rules specific to elliptic curves, which differ from typical Cartesian coordinate arithmetic.
- If dealing with cryptographic applications, be careful with operations that involve points at infinity as they can affect the security properties of the ECC algorithms.

## Points at Infinity

In elliptic curve groups, the point at infinity acts as the identity element, which is akin to the number zero in regular arithmetic. When a `Point` instance doesn't have specific `(x, y)` coordinates provided, it can be used to represent this identity element in ECC computations.

Incorporating the `Point` class into elliptic curve cryptographic schemes allows for a robust and secure implementation of ECC methods, forming the basis for encryption, digital signatures, and key exchange protocols.