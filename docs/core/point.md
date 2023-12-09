# Point

The `Point` class represents a point on an elliptic curve.

## Attributes

- **x** (Optional[int]): The x-coordinate of the point.
- **y** (Optional[int]): The y-coordinate of the point.

## Example

```python
from ecutils.core import Point

# Creating a Point on the elliptic curve
p = Point(x=10, y=20)
```