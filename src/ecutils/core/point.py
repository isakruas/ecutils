# ecutils/core/point.py

"""The Point class — public-facing representation of a point on an elliptic curve.

A point on the short Weierstrass curve y² = x³ + ax + b (mod p) belongs
to an abelian group with the following properties:

- **Closure**: P + Q is also on the curve.
- **Associativity**: (P + Q) + R = P + (Q + R).
- **Identity**: There exists a special "point at infinity" O such that P + O = P.
- **Inverse**: For every P = (x, y), the inverse is -P = (x, -y mod p), and P + (-P) = O.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ecutils.core.arithmetic.affine import affine_add, affine_mul
from ecutils.core.arithmetic.jacobian import jac_add, jac_mul, to_affine, to_jacobian
from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.utils.math import modular_sqrt


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

    # ----- compression -----

    def compress(self) -> tuple[int, int]:
        """Compress this point to its x-coordinate and parity bit.

        Returns:
            A tuple ``(x, parity)`` where *parity* is ``y % 2``.

        Raises:
            ValueError: If this point is the identity (point at infinity).
        """
        if self.is_identity:
            raise ValueError("Cannot compress the identity point (point at infinity).")
        return (self.x, self.y % 2)  # type: ignore[operator]

    @classmethod
    def decompress(cls, x: int, parity: int, curve: CurveParams) -> Point:
        """Reconstruct a point from its compressed form.

        Args:
            x:      The x-coordinate.
            parity: The parity bit (0 or 1) indicating which y to select.
            curve:  The curve parameters.

        Returns:
            The decompressed ``Point``.

        Raises:
            ValueError: If *x* does not correspond to a valid point on the curve.
        """
        rhs = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p
        y = modular_sqrt(rhs, curve.p)
        if y is None:
            raise ValueError(
                f"x={x} does not correspond to a valid point on the curve "
                f"y² = x³ + {curve.a}x + {curve.b} (mod {curve.p})."
            )
        if y % 2 != parity:
            y = curve.p - y
        return cls(x, y, curve)

    # ----- SEC 1 compression (interoperable) -----

    def compress_sec1(self) -> bytes:
        """Compress this point to SEC 1 / X9.62 format.

        The output is a single byte prefix (``0x02`` for even y, ``0x03``
        for odd y) followed by the x-coordinate as a big-endian unsigned
        integer, zero-padded to the field size.

        Returns:
            Compressed point as bytes.

        Raises:
            ValueError: If this point is the identity or has no curve params.
        """
        if self.is_identity:
            raise ValueError("Cannot compress the identity point (point at infinity).")
        curve = self._require_curve()
        byte_len = (curve.p.bit_length() + 7) // 8
        prefix = b"\x03" if self.y % 2 else b"\x02"  # type: ignore[operator]
        return prefix + self.x.to_bytes(byte_len, "big")  # type: ignore[union-attr]

    def to_uncompressed_sec1(self) -> bytes:
        """Serialize this point to SEC 1 / X9.62 uncompressed format.

        The output is ``0x04 || x || y``, where x and y are big-endian
        unsigned integers zero-padded to the field size.

        Returns:
            Uncompressed point as bytes.

        Raises:
            ValueError: If this point is the identity or has no curve params.
        """
        if self.is_identity:
            raise ValueError("Cannot serialize the identity point (point at infinity).")
        curve = self._require_curve()
        byte_len = (curve.p.bit_length() + 7) // 8
        return (
            b"\x04"
            + self.x.to_bytes(byte_len, "big")  # type: ignore[union-attr]
            + self.y.to_bytes(byte_len, "big")  # type: ignore[union-attr]
        )

    @classmethod
    def from_sec1(cls, data: bytes, curve: CurveParams) -> Point:
        """Deserialize a point from SEC 1 / X9.62 format.

        Supports both compressed (``0x02``/``0x03`` prefix) and
        uncompressed (``0x04`` prefix) encodings.

        Args:
            data:  The SEC 1 encoded point bytes.
            curve: The curve parameters.

        Returns:
            The deserialized ``Point``.

        Raises:
            ValueError: If the data is malformed or the point is invalid.
        """
        if len(data) < 2:
            raise ValueError("SEC 1 data too short.")
        byte_len = (curve.p.bit_length() + 7) // 8
        prefix = data[0]

        if prefix in (0x02, 0x03):
            if len(data) != 1 + byte_len:
                raise ValueError(
                    f"Compressed SEC 1 data must be {1 + byte_len} bytes, "
                    f"got {len(data)}."
                )
            x = int.from_bytes(data[1:], "big")
            parity = prefix - 0x02  # 0 for even, 1 for odd
            return cls.decompress(x, parity, curve)

        if prefix == 0x04:
            if len(data) != 1 + 2 * byte_len:
                raise ValueError(
                    f"Uncompressed SEC 1 data must be {1 + 2 * byte_len} bytes, "
                    f"got {len(data)}."
                )
            x = int.from_bytes(data[1 : 1 + byte_len], "big")
            y = int.from_bytes(data[1 + byte_len :], "big")
            return cls(x, y, curve)

        raise ValueError(
            f"Unknown SEC 1 prefix: 0x{prefix:02x}. Expected 0x02, 0x03, or 0x04."
        )

    # ----- operators -----

    def __neg__(self) -> Point:
        """Return the additive inverse: -P = (x, -y mod p)."""
        if self.is_identity:
            return self
        curve = self._require_curve()
        return Point(self.x, (-self.y) % curve.p, curve, _trusted=True)  # type: ignore[operator]

    def __add__(self, other: Point) -> Point:
        """Add two points on the same curve using the group law.

        Delegates to affine or Jacobian arithmetic depending on
        ``curve.coord``.  The chord-and-tangent formulas are:

        Addition (P ≠ Q):
            λ  = (y₂ - y₁) · (x₂ - x₁)⁻¹
            x₃ = λ² - x₁ - x₂
            y₃ = λ(x₁ - x₃) - y₁

        Doubling (P = Q):
            λ  = (3x₁² + a) · (2y₁)⁻¹
            x₃ = λ² - 2x₁
            y₃ = λ(x₁ - x₃) - y₁
        """
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
        """Scalar multiplication: k · P via double-and-add in O(log k)."""
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
