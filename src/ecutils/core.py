from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


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

    use_projective_coordinates: bool = True

    @lru_cache(maxsize=1024, typed=True)
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

        if self.use_projective_coordinates:
            p1_jacobian = self.to_jacobian(p1)
            p2_jacobian = self.to_jacobian(p2)
            p3_jacobian = self.jacobian_add_points(p1_jacobian, p2_jacobian)
            return self.to_affine(p3_jacobian)

        if p1 == p2:
            return self.double_point(p1)
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

    @lru_cache(maxsize=1024, typed=True)
    def double_point(self, p: Point) -> Point:
        """Double a point on an elliptic curve."""
        if p.x is None or p.y is None:
            return p

        if not self.is_point_on_curve(p):
            raise ValueError(
                "Invalid input: One or both of the input points are not on the elliptic curve."
            )

        n = (3 * p.x**2 + self.a) % self.p
        d = (2 * p.y) % self.p
        try:
            inv = pow(d, -1, self.p)
        except ValueError:
            return Point()  # Point at infinity
        s = (n * inv) % self.p
        x_3 = (s**2 - p.x - p.x) % self.p
        y_3 = (s * (p.x - x_3) - p.y) % self.p
        return Point(x_3, y_3)

    @lru_cache(maxsize=1024, typed=True)
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

        if self.use_projective_coordinates:
            p_jacobian = self.to_jacobian(p)
            q_jacobian = self.jacobian_multiply_point(k, p_jacobian)
            p1 = self.to_affine(q_jacobian)
            if p1.x is None or p1.y is None:
                return p1
            if not self.is_point_on_curve(p1):
                raise ValueError(
                    "Invalid input: One or both of the input points are not on the elliptic curve."
                )
            return p1

        r = None

        num_bits = k.bit_length()

        for i in range(num_bits - 1, -1, -1):
            if r is None:
                r = p
                continue

            if r.x is None and r.y is None:
                r = p

            r = self.double_point(r)

            if (k >> i) & 1:
                if r.x is None and r.y is None:
                    r = p
                else:
                    r = self.add_points(r, p)
        return r

    @lru_cache(maxsize=1024, typed=True)
    def jacobian_add_points(
        self, p1: JacobianPoint, p2: JacobianPoint
    ) -> JacobianPoint:
        """Add two points on an elliptic curve using Jacobian coordinates."""
        if p1.x is None or p1.y is None:
            return p2
        if p2.x is None or p2.y is None:
            return p1

        z1z1 = p1.z * p1.z % self.p
        z2z2 = p2.z * p2.z % self.p
        u1 = p1.x * z2z2 % self.p
        u2 = p2.x * z1z1 % self.p
        s1 = p1.y * p2.z * z2z2 % self.p
        s2 = p2.y * p1.z * z1z1 % self.p

        if u1 == u2:
            if s1 != s2:
                return JacobianPoint()  # Point at infinity
            return self.jacobian_double_point(p1)

        h = u2 - u1
        i = (2 * h) * (2 * h) % self.p
        j = h * i % self.p
        r = 2 * (s2 - s1) % self.p
        v = u1 * i % self.p
        x = (r * r - j - 2 * v) % self.p
        y = (r * (v - x) - 2 * s1 * j) % self.p
        z = ((p1.z + p2.z) * (p1.z + p2.z) - z1z1 - z2z2) * h % self.p

        return JacobianPoint(x, y, z)

    @lru_cache(maxsize=1024, typed=True)
    def jacobian_double_point(self, p: JacobianPoint) -> JacobianPoint:
        """Double a point on an elliptic curve using Jacobian coordinates."""
        if p.x is None or p.y is None:
            return p

        if p.y == 0:
            return JacobianPoint()  # Point at infinity

        ysq = p.y * p.y % self.p
        zsqr = p.z * p.z % self.p
        s = (4 * p.x * ysq) % self.p
        m = (3 * p.x * p.x + self.a * zsqr * zsqr) % self.p
        nx = (m * m - 2 * s) % self.p
        ny = (m * (s - nx) - 8 * ysq * ysq) % self.p
        nz = (2 * p.y * p.z) % self.p

        return JacobianPoint(nx, ny, nz)

    @lru_cache(maxsize=1024, typed=True)
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
    @lru_cache(maxsize=1024, typed=True)
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

    @lru_cache(maxsize=1024, typed=True)
    def to_affine(self, point: JacobianPoint) -> Point:
        """Converts a point from Jacobian coordinates to affine coordinates.

        Args:
            point (JacobianPoint): The point in Jacobian coordinates.

        Returns:
            Point: The point in affine coordinates.
        """
        if point.x is None or point.y is None or point.z == 0:
            return Point()
        inv_z = pow(point.z, -1, self.p)
        return Point((point.x * inv_z**2) % self.p, (point.y * inv_z**3) % self.p)

    @lru_cache(maxsize=1024, typed=True)
    def is_point_on_curve(self, p: Point) -> bool:
        """Check if a point lies on the elliptic curve.

        Args:
            p (Point): The point to check.

        Returns:
            bool: True if the point is on the curve, False otherwise.
        """

        if p.x is None or p.y is None:
            return False

        if isinstance(p, JacobianPoint):
            p = self.to_affine(p)

        # The equation of the curve is y^2 = x^3 + ax + b. We check if the point satisfies this equation.
        left_side = p.y**2 % self.p
        right_side = (p.x**3 + self.a * p.x + self.b) % self.p
        return left_side == right_side


@dataclass(frozen=True)
class EllipticCurve(EllipticCurveOperations):
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
