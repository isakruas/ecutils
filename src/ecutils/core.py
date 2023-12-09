from dataclasses import dataclass
from typing import Optional


@dataclass
class Point:
    """Represents a point on an elliptic curve.

    Attributes:
        x (Optional[int]): The x-coordinate of the point.
        y (Optional[int]): The y-coordinate of the point.
    """

    x: Optional[int] = None
    y: Optional[int] = None


class EllipticCurveOperations:
    """Implements mathematical operations for elliptic curves."""

    def add_points(self, p1: Point, p2: Point) -> Point:
        """Add two points on an elliptic curve.

        Args:
            p1 (Point): The first point to add.
            p2 (Point): The second point to add.

        Returns:
            Point: The resulting point after addition.

        Raises:
            ValueError: If the input point is not on the elliptic curve.
        """

        if p1.x is None or p1.y is None:
            return p2

        if p2.x is None or p2.y is None:
            return p1

        if not self.is_point_on_curve(p1) or not self.is_point_on_curve(p2):
            raise ValueError(
                "Invalid input: One or both of the input points are not on the elliptic curve."
            )

        if p1 == p2:
            n = (3 * p1.x**2 + self.a) % self.p
            d = (2 * p1.y) % self.p
            try:
                inv = pow(d, -1, self.p)
            except ValueError:
                return Point()  # Point at infinity
            s = (n * inv) % self.p
            x_3 = (s**2 - p1.x - p1.x) % self.p
            y_3 = (s * (p1.x - x_3) - p1.y) % self.p
            return Point(x_3, y_3)
        else:
            n = (p2.y - p1.y) % self.p
            d = (p2.x - p1.x) % self.p
            try:
                inv = pow(d, -1, self.p)
            except ValueError:
                return Point()  # Point at infinity
            s = (n * inv) % self.p
            x_3 = (s**2 - p1.x - p2.x) % self.p
            y_3 = (s * (p1.x - x_3) - p1.y) % self.p
            return Point(x_3, y_3)

    def multiply_point(self, k: int, p: Point) -> Point:
        """Multiply a point on an elliptic curve by an integer scalar.

        Args:
            k (int): The scalar to multiply by.
            p (Point): The point to be multiplied.

        Returns:
            Point: The resulting point after multiplication.

        Raises:
            ValueError: If k is not in the range 0 < k < n.
        """

        if k == 0 or k >= self.n:
            raise ValueError("k is not in the range 0 < k < n")

        r = None

        num_bits = k.bit_length()

        for i in range(num_bits - 1, -1, -1):
            if r is None:
                r = p
                continue

            if r.x is None and r.y is None:
                r = p

            r = self.add_points(r, r)

            if (k >> i) & 1:
                if r.x is None and r.y is None:
                    r = p
                else:
                    r = self.add_points(r, p)
        return r

    def is_point_on_curve(self, p: Point) -> bool:
        """Check if a point lies on the elliptic curve.

        Args:
            p (Point): The point to check.

        Returns:
            bool: True if the point is on the curve, False otherwise.
        """

        if p.x is None or p.y is None:
            return False
        # The equation of the curve is y^2 = x^3 + ax + b. We check if the point satisfies this equation.
        left_side = p.y**2 % self.p
        right_side = (p.x**3 + self.a * p.x + self.b) % self.p
        return left_side == right_side


@dataclass
class EllipticCurve(EllipticCurveOperations):
    """Represents the parameters and operations of an elliptic curve.

    Attributes:
        p (int): The prime order of the finite field.
        a (int): The coefficient 'a' in the curve equation y^2 = x^3 + ax + b.
        b (int): The coefficient 'b' in the curve equation.
        G (Point): The base point (generator) of the curve.
        n (int): The order of the base point.
        h (int): The cofactor.
    """

    p: int
    a: int
    b: int
    G: Point
    n: int
    h: int
