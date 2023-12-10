# Elliptic Curve

This documentation provides an extensive overview of the Elliptic Curve Utils module, which facilitates elliptic curve operations such as point addition, scalar multiplication, and validation of points on a curve. These operations are fundamental in various cryptographic protocols, including key agreement, digital signatures, and encryption.

## Overview of ECC

Elliptic Curve Cryptography (ECC) is a form of public-key cryptography based on algebraic structures of elliptic curves over finite fields. Compared to other cryptosystems like RSA, ECC can achieve equivalent security with smaller key sizes, resulting in faster computations and reduced power consumption.

## Key Components

### Elliptic Curve

An elliptic curve is represented by the equation `y^2 = x^3 + ax + b` over a finite field defined by a prime number `p`. The curve parameters include:

- **a** (int): The coefficient 'a' in the curve equation.
- **b** (int): The coefficient 'b' in the curve equation.
- **p** (int): The prime order of the finite field.

### Point on an Elliptic Curve

A point `P` on an elliptic curve consists of two coordinates `(x, y)` that satisfy the curve's equation.

### Base Point (Generator)

The base point `G` is a specific point on the elliptic curve chosen to generate other points through scalar multiplication.

### Order of Point

The order of point `n` is the smallest positive integer such that `nG` (scalar multiplication of `G` by `n`) is the identity element (point at infinity) on the curve.

### Cofactor

The cofactor `h` relates the order of the base point `G` with the total number of points on the curve.

## Core Classes

### `EllipticCurve`

An instance of `EllipticCurve` represents a specific elliptic curve defined over a finite field.

#### Attributes:
- `p`: The prime order of the finite field.
- `a`: The coefficient 'a' in the curve equation.
- `b`: The coefficient 'b' in the curve equation.
- `G`: The base point (generator) of the curve.
- `n`: The order of the base point.
- `h`: The cofactor.

#### Operations:

##### `add_points(point1, point2)`
Adds two points on the elliptic curve.

##### `multiply_point(scalar, point)`
Multiplies a point on the curve by an integer scalar.

##### `is_point_on_curve(point)`
Checks if a point lies on the elliptic curve.

### `Point`

An instance of `Point` represents a point on an elliptic curve with `x` and `y` coordinates.

#### Attributes:
- `x`: The x-coordinate of the point.
- `y`: The y-coordinate of the point.

## Using the ECC Utility Module

### Example Usage:

To add two points on the curve:

```python
from ecutils.core import EllipticCurve, Point

curve = EllipticCurve(p=<prime_value>, a=<coef_a>, b=<coef_b>, G=<base_point>, ...)
point1 = Point(x=<x1_value>, y=<y1_value>)
point2 = Point(x=<x2_value>, y=<y2_value>)

sum_point = curve.add_points(point1, point2)
```

To multiply a point by a scalar:

```python
product_point = curve.multiply_point(<scalar_value>, point1)
```

To check if a point lies on the curve:

```python
is_valid = curve.is_point_on_curve(point1)
```

### Working with Predefined Curves:

For convenience, the module includes predefined curves, such as `secp192k1`.

```python
from ecutils.curves import secp192k1

# Use secp192k1 as the curve
curve = secp192k1
# Now you can perform operations with this predefined curve
```

## Important Notes

- Always verify that the points involved in operations reside on the intended curve.
- For cryptographic applications, ensure that the private keys (scalars) are kept confidential and securely generated.
- When adding points or multiplying by a scalar, if an operation yields the identity element or "point at infinity," it should be handled appropriately, as this represents the additive identity in elliptic curve groups.

## Conclusion

The ECC utility module provides the fundamental tools necessary for elliptic curve operations used in modern cryptography. With this documentation, users should have a clear understanding of how to utilize the module for various ECC-related tasks.