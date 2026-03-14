# ecutils/core/point.py

"""The Point class — public-facing representation of a point on an elliptic curve."""

from __future__ import annotations

from dataclasses import dataclass, field

from ecutils.core.arithmetic.affine import affine_add, affine_mul
from ecutils.core.arithmetic.jacobian import jac_add, jac_mul, to_affine, to_jacobian
from ecutils.core.curve import CoordinateSystem, CurveParams


@dataclass(frozen=True)
class Point:
    """A point on an elliptic curve that supports arithmetic operators.

    Usage
    -----
    >>> curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
    >>> P = Point(x=0, y=1, curve=curve)
    >>> Q = Point(x=6, y=19, curve=curve)
    >>> P + Q          # point addition
    >>> 5 * P          # scalar multiplication
    >>> -P             # point negation
    >>> P == Q         # equality

    To switch coordinate systems, create a new CurveParams with a
    different ``coord`` field:

    >>> affine_curve = CurveParams(p=23, a=1, b=1, n=28, coord=CoordinateSystem.AFFINE)
    >>> P_affine = Point(x=0, y=1, curve=affine_curve)
    """

    x: int | None = None
    y: int | None = None
    curve: CurveParams | None = field(default=None, repr=False, compare=False)
    _trusted: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        # Points produced by internal arithmetic are already valid.
        if self._trusted:
            return
        # Identity point (point at infinity) is always valid.
        if self.x is None or self.y is None:
            return
        # Without curve params we can't validate — skip silently.
        if self.curve is None:
            return
        lhs = pow(self.y, 2, self.curve.p)
        rhs = (
            pow(self.x, 3, self.curve.p) + self.curve.a * self.x + self.curve.b
        ) % self.curve.p
        if lhs != rhs:
            raise ValueError(
                f"Point({self.x}, {self.y}) is not on the curve "
                f"y² = x³ + {self.curve.a}x + {self.curve.b} (mod {self.curve.p})."
            )

    # ----- helpers -----

    @property
    def is_identity(self) -> bool:
        """True when this point represents the point at infinity (identity element)."""
        return self.x is None or self.y is None

    def is_on_curve(self) -> bool:
        """Check whether this point satisfies y² ≡ x³ + ax + b (mod p)."""
        if self.is_identity or self.curve is None:
            return False
        lhs = pow(self.y, 2, self.curve.p)  # type: ignore[arg-type]
        rhs = (
            pow(self.x, 3, self.curve.p) + self.curve.a * self.x + self.curve.b  # type: ignore[operator]
        ) % self.curve.p
        return lhs == rhs

    def _require_curve(self) -> CurveParams:
        if self.curve is None:
            raise ValueError(
                "Cannot perform arithmetic on a Point without curve parameters. "
                "Pass a CurveParams instance via the 'curve' argument."
            )
        return self.curve

    def _coerce(self, other: Point) -> Point:
        """Ensure *other* carries curve params (borrow ours if needed)."""
        if other.curve is None and self.curve is not None:
            return Point(other.x, other.y, self.curve)
        return other

    def _wrap(self, x: int | None, y: int | None) -> Point:
        return Point(x, y, self.curve, _trusted=True)

    # ----- operators -----

    def __neg__(self) -> Point:
        """Return the additive inverse (negation) of this point."""
        if self.is_identity:
            return self
        curve = self._require_curve()
        return Point(self.x, (-self.y) % curve.p, curve, _trusted=True)  # type: ignore[operator]

    def __add__(self, other: Point) -> Point:
        """Add two points on the same curve."""
        curve = self._require_curve()
        other = self._coerce(other)

        if curve.coord is CoordinateSystem.JACOBIAN:
            jp1 = to_jacobian(self)
            jp2 = to_jacobian(other)
            jp3 = jac_add(jp1, jp2, curve)
            return self._wrap(*to_affine(jp3, curve))

        return self._wrap(*affine_add(self.x, self.y, other.x, other.y, curve))

    def __sub__(self, other: Point) -> Point:
        """Subtract: self + (-other)."""
        return self.__add__(-other)

    def __mul__(self, k: int) -> Point:
        """Scalar multiplication: Point * k."""
        curve = self._require_curve()
        k = k % curve.n

        if curve.coord is CoordinateSystem.JACOBIAN:
            jp = to_jacobian(self)
            jp_result = jac_mul(k, jp, curve)
            return self._wrap(*to_affine(jp_result, curve))

        return self._wrap(*affine_mul(k, self.x, self.y, curve))

    def __rmul__(self, k: int) -> Point:
        """Scalar multiplication: k * Point."""
        return self.__mul__(k)

    # ----- display -----

    def __repr__(self) -> str:
        if self.is_identity:
            return "Point(∞)"
        return f"Point(x={self.x}, y={self.y})"
