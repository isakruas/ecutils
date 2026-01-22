from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional

from ecutils.settings import LRU_CACHE_MAXSIZE


@dataclass(frozen=True)
class Point:
    """Represents a point on an elliptic curve.

    Attributes:
        x (Optional[int]): The x-coordinate of the point.
        y (Optional[int]): The y-coordinate of the point.
    """

    x: Optional[int] = None
    y: Optional[int] = None


@dataclass(frozen=True)
class JacobianPoint:
    """Represents a point on an elliptic curve in Jacobian coordinates.

    Attributes:
        x (Optional[int]): The x-coordinate of the point.
        y (Optional[int]): The y-coordinate of the point.
        z (int): The additional coordinate for projective representation.
    """

    x: Optional[int] = None
    y: Optional[int] = None
    z: int = 1


class EllipticCurveOperations:
    """Implements mathematical operations for elliptic curves."""

    def __init__(self, curve: "EllipticCurve"):
        self.curve = curve

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
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

        if not self.curve.is_point_on_curve(p1) or not self.curve.is_point_on_curve(p2):
            raise ValueError(
                "Invalid input: One or both of the input points are not on the elliptic curve."
            )

        if self.curve.use_projective_coordinates:
            p1_jacobian = self.to_jacobian(p1)
            p2_jacobian = self.to_jacobian(p2)
            p3_jacobian = self.jacobian_add_points(p1_jacobian, p2_jacobian)
            return self.to_affine(p3_jacobian)

        if p1 == p2:
            return self.double_point(p1)
        n = (p2.y - p1.y) % self.curve.p
        d = (p2.x - p1.x) % self.curve.p
        try:
            inv = pow(d, -1, self.curve.p)
        except ValueError:
            return Point()  # Point at infinity
        s = (n * inv) % self.curve.p
        x_3 = (s**2 - p1.x - p2.x) % self.curve.p
        y_3 = (s * (p1.x - x_3) - p1.y) % self.curve.p
        return Point(x_3, y_3)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def double_point(self, p: Point) -> Point:
        """Double a point on an elliptic curve."""
        if p.x is None or p.y is None:
            return p

        if not self.curve.is_point_on_curve(p):
            raise ValueError(
                "Invalid input: One or both of the input points are not on the elliptic curve."
            )

        n = (3 * p.x**2 + self.curve.a) % self.curve.p
        d = (2 * p.y) % self.curve.p
        try:
            inv = pow(d, -1, self.curve.p)
        except ValueError:
            return Point()  # Point at infinity
        s = (n * inv) % self.curve.p
        x_3 = (s**2 - p.x - p.x) % self.curve.p
        y_3 = (s * (p.x - x_3) - p.y) % self.curve.p
        return Point(x_3, y_3)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def multiply_point(self, k: int, p: Point) -> Point:
        """Multiply a point on an elliptic curve by an integer scalar.

        Args:
            k (int): The scalar to multiply by.
            p (Point): The point to be multiplied.

        Returns:
            Point: The resulting point after multiplication.
        """

        if p.x is None or p.y is None or k == 0:
            return Point()

        k = k % self.curve.n

        if self.curve.use_projective_coordinates:
            p_jacobian = self.to_jacobian(p)
            q_jacobian = self.jacobian_multiply_point(k, p_jacobian)
            p1 = self.to_affine(q_jacobian)
            if p1.x is None or p1.y is None:
                return p1
            if not self.curve.is_point_on_curve(p1):
                raise ValueError(
                    "Invalid input: One or both of the input points are not on the elliptic curve."
                )
            return p1

        r = Point()
        while k > 0:
            if k & 1:
                r = self.add_points(r, p)
            p = self.double_point(p)
            k >>= 1
        return r

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def jacobian_add_points(
        self, p1: JacobianPoint, p2: JacobianPoint
    ) -> JacobianPoint:
        """Add two points on an elliptic curve using Jacobian coordinates."""
        if p1.x is None or p1.y is None:
            return p2
        if p2.x is None or p2.y is None:
            return p1

        z1z1 = p1.z * p1.z % self.curve.p
        z2z2 = p2.z * p2.z % self.curve.p
        u1 = p1.x * z2z2 % self.curve.p
        u2 = p2.x * z1z1 % self.curve.p
        s1 = p1.y * p2.z * z2z2 % self.curve.p
        s2 = p2.y * p1.z * z1z1 % self.curve.p

        if u1 == u2:
            if s1 != s2:
                return JacobianPoint()  # Point at infinity
            return self.jacobian_double_point(p1)

        h = u2 - u1
        i = (2 * h) * (2 * h) % self.curve.p
        j = h * i % self.curve.p
        r = 2 * (s2 - s1) % self.curve.p
        v = u1 * i % self.curve.p
        x = (r * r - j - 2 * v) % self.curve.p
        y = (r * (v - x) - 2 * s1 * j) % self.curve.p
        z = ((p1.z + p2.z) * (p1.z + p2.z) - z1z1 - z2z2) * h % self.curve.p

        return JacobianPoint(x, y, z)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def jacobian_double_point(self, p: JacobianPoint) -> JacobianPoint:
        """Double a point on an elliptic curve using Jacobian coordinates."""
        if p.x is None or p.y is None:
            return p

        if p.y == 0:
            return JacobianPoint()  # Point at infinity

        ysq = p.y * p.y % self.curve.p
        zsqr = p.z * p.z % self.curve.p
        s = (4 * p.x * ysq) % self.curve.p
        m = (3 * p.x * p.x + self.curve.a * zsqr * zsqr) % self.curve.p
        nx = (m * m - 2 * s) % self.curve.p
        ny = (m * (s - nx) - 8 * ysq * ysq) % self.curve.p
        nz = (2 * p.y * p.z) % self.curve.p

        return JacobianPoint(nx, ny, nz)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def jacobian_multiply_point(self, k: int, p: JacobianPoint) -> JacobianPoint:
        """Multiply a point on an elliptic curve by an integer scalar using repeated addition."""
        if k == 0 or p.x is None or p.y is None:
            return JacobianPoint()  # Identity point

        result = JacobianPoint()  # Initialize with the identity point
        k_bin = bin(k)[2:]  # Binary representation of k
        for i in range(len(k_bin)):
            if k_bin[-i - 1] == "1":
                result = self.jacobian_add_points(result, p)
            p = self.jacobian_double_point(p)

        return result

    @staticmethod
    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def to_jacobian(point: Point) -> JacobianPoint:
        """Converts a point from affine coordinates to Jacobian coordinates.

        Args:
            point (Point): The point in affine coordinates.

        Returns:
            JacobianPoint: The point in Jacobian coordinates.
        """
        if point.x is None or point.y is None:
            return JacobianPoint()
        return JacobianPoint(point.x, point.y, 1)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def to_affine(self, point: JacobianPoint) -> Point:
        """Converts a point from Jacobian coordinates to affine coordinates.

        Args:
            point (JacobianPoint): The point in Jacobian coordinates.

        Returns:
            Point: The point in affine coordinates.
        """
        if point.x is None or point.y is None or point.z == 0:
            return Point()
        inv_z = pow(point.z, -1, self.curve.p)
        return Point(
            (point.x * inv_z**2) % self.curve.p, (point.y * inv_z**3) % self.curve.p
        )


@dataclass(eq=False)
class EllipticCurve:
    """Represents the parameters and operations of an elliptic curve.

    Attributes:
        p (int): The prime order of the finite field.
        a (int): The coefficient 'a' in the curve equation y^2 = x^3 + ax + b.
        b (int): The coefficient 'b' in the curve equation.
        G (Point): The base point (generator) of the curve.
        n (int): The order of the base point.
        h (int): The cofactor.
        use_projective_coordinates (bool): If True, Jacobian coordinates will be used in curve operations.
    """

    p: int
    a: int
    b: int
    G: Point
    n: int
    h: int
    use_projective_coordinates: bool = True
    _ops: EllipticCurveOperations = field(init=False, repr=False)

    def __post_init__(self):
        self._ops = EllipticCurveOperations(self)

    def __hash__(self):
        return hash((self.p, self.a, self.b, self.G, self.n, self.h))

    def add_points(self, p1: Point, p2: Point) -> Point:
        return self._ops.add_points(p1, p2)

    def double_point(self, p: Point) -> Point:
        return self._ops.double_point(p)

    def multiply_point(self, k: int, p: Point) -> Point:
        return self._ops.multiply_point(k, p)

    def to_jacobian(self, point: Point) -> "JacobianPoint":
        return self._ops.to_jacobian(point)

    def to_affine(self, point: "JacobianPoint") -> Point:
        return self._ops.to_affine(point)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def is_point_on_curve(self, p: Point) -> bool:
        """Check if a point lies on the elliptic curve.

        Args:
            p (Point): The point to check.

        Returns:
            bool: True if the point is on the curve, False otherwise.
        """
        if isinstance(p, JacobianPoint):
            p = self.to_affine(p)

        if p.x is None or p.y is None:
            return False

        # The equation of the curve is y^2 = x^3 + ax + b. We check if the point satisfies this equation.
        left_side = p.y**2 % self.p
        right_side = (p.x**3 + self.a * p.x + self.b) % self.p
        return left_side == right_side
