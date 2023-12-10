# Elliptic Curve

The Elliptic Curve module provides functionalities for performing operations such as point addition, scalar multiplication, and verifying if a point lies on a given curve. These operations are fundamental in various cryptographic applications that utilize Elliptic Curve Cryptography (ECC).

### Overview

In ECC, we deal with equations that define elliptic curves over finite fields. The standard form of an elliptic curve equation is `y^2 = x^3 + ax + b`, where `a` and `b` represent the curve coefficients. By choosing a specific curve and operating within a finite field, we can use these curves for cryptographic purposes, like secure key exchange, digital signatures, and encryption.

### The `EllipticCurve` Class

The `EllipticCurve` class represents a particular curve with its parameters and encompasses operations you can perform on points on the curve.

### Attributes

- `p`: The prime number defining the finite field's order.
- `a`: The 'a' coefficient in the curve equation.
- `b`: The 'b' coefficient in the curve equation.
- `G`: The base point or generator, a predefined point on the curve.
- `n`: The base point 'G's order.
- `h`: The cofactor.

### Operations

#### `add_points(self, p1, p2) -> Point`
This method allows you to add two points (`p1` and `p2`) on the curve together. As long as the points are valid and not inverses of each other, their addition results in a third point on the curve, which the method then returns.

#### `multiply_point(self, k, p) -> Point`
The `multiply_point` method is used to compute the scalar multiplication of a point `p` by an integer `k`. The multiplication yields another point on the curve.

#### `is_point_on_curve(self, p) -> bool`
The `is_point_on_curve` method checks if a given point `p` is indeed on the curve you're working with.

### Practical Examples

#### Creating an Elliptic Curve

Here's how you can define an elliptic curve and instantiate the `EllipticCurve` class with these parameters:

```python
from ecutils.core import EllipticCurve, Point

# Example parameters
p = 23  # The prime number defining the finite field's order
a = 1   # The 'a' coefficient in the curve equation
b = 1   # The 'b' coefficient in the curve equation
G = Point(0, 1)
n = 28
h = 1

curve = EllipticCurve(p=p, a=a, b=b, G=G, n=n, h=h)
```

#### Adding Points

To add two points on the elliptic curve:

```python
# Define points on the curve
point1 = Point(x=6, y=19)
point2 = Point(x=3, y=13)

# Add the points
sum_point = curve.add_points(point1, point2)
print(f"The sum of the points is ({sum_point.x}, {sum_point.y}).")
```

#### Scalar Multiplication

To multiply a point by a scalar:

```python
# Choose a scalar value
k = 3

# Perform the multiplication
product_point = curve.multiply_point(k, G)
print(f"The product of the point and scalar is ({product_point.x}, {product_point.y}).")
```

#### Validating Points

To check whether a point is on the curve:

```python
# Validate the point
is_valid = curve.is_point_on_curve(point1)
print(f"Is the point on the curve? {is_valid}")
```

### Important Notes

When using the `EllipticCurve` class, make sure all points are within the finite field specified by `p`. Also, keep in mind that scalar values used for multiplication should be in the appropriate range, usually between 1 and `n-1`.

By understanding the `EllipticCurve` class functionalities, you can efficiently carry out essential ECC operations for cryptographic purposes. Always be mindful of the integrity and security principles governing the use of cryptographic tools.