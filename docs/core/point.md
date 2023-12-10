# Point

The `Point` class represents an individual point on an elliptic curve, which is a key component in Elliptic Curve Cryptography (ECC). In ECC, operations like point addition and scalar multiplication are performed with these points.

### Attributes

- `x`: This is the x-coordinate of the point. It can be any integer within the finite field, or it can be `None` if the point represents the point at infinity.
- `y`: This is the y-coordinate, which, similarly to the x-coordinate, can either be any integer within the finite field or `None` for the point at infinity.

### Creating a Point

When you need to create a `Point`, you provide the `x` and `y` coordinates like this:

```python
from ecutils.core import Point

# Create a point with specific coordinates
point = Point(x=3, y=5)
print(f"Point coordinates: ({point.x}, {point.y})")
```

### Example: Verifying a Point on a Curve

Here's how you could verify whether a point lies on a specific curve:

```python
from ecutils.core import EllipticCurve, Point

# Curve parameters
p = 23
a = 1
b = 1
G = Point(0, 1)  # Base point
n = 28
h = 1

# Instantiate the curve
curve = EllipticCurve(p=p, a=a, b=b, G=G, n=n, h=h)

# Point to be checked
point_to_check = Point(x=1, y=7)

# Check whether the point is on the curve
is_on_curve = curve.is_point_on_curve(point_to_check)
print(f"Is the point ({point_to_check.x}, {point_to_check.y}) on the curve? {is_on_curve}")
```

### Point at Infinity

In elliptic curve operations, there is a special point known as the "point at infinity," which serves as the identity element for the group of points on the curve. In the `Point` class, this point is represented by having both `x` and `y` attributes set to `None`:

```python
# Instantiate the point at infinity
infinity_point = Point()

# Typically, the point at infinity doesn't lie on the curve
is_infinity_on_curve = curve.is_point_on_curve(infinity_point)
print(f"Does the point at infinity lie on the curve? {is_infinity_on_curve}")
```

### Important Notes

It is critical to confirm that any point you use in elliptic curve operations actually belongs to the curve you're working with. This step is crucial for maintaining cryptographic processes' security and integrity.

The `Point` class, in conjunction with the `EllipticCurve` class, provides you with the tools needed to effectively work on ECC-related tasks, ensuring proper use and management of both points and curves.
