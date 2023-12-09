# Elliptic Curve

The `EllipticCurve` class represents the parameters and operations of an elliptic curve used in cryptographic algorithms.

## Attributes

- **p** (int): The prime order of the finite field.
- **a** (int): The coefficient 'a' in the curve equation y^2 = x^3 + ax + b.
- **b** (int): The coefficient 'b' in the curve equation.
- **G** (Point): The base point (generator) of the curve.
- **n** (int): The order of the base point.
- **h** (int): The cofactor.

## Operations

### add_points

Adds two points on an elliptic curve.

```python
from ecutils.core import EllipticCurve, Point

curve = EllipticCurve(...)
point1 = Point(...)
point2 = Point(...)

resulting_point = curve.add_points(point1, point2)
```

### multiply_point

Multiplies a point by an integer scalar.

```python
from ecutils.core import EllipticCurve, Point

curve = EllipticCurve(...)
point = Point(...)

resulting_point = curve.multiply_point(5, point)
```

### is_point_on_curve

Checks if a point lies on the elliptic curve.

```python
from ecutils.core import EllipticCurve, Point

curve = EllipticCurve(...)
point = Point(...)

is_on_curve = curve.is_point_on_curve(point)
```