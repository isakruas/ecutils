# ecutils/core/curve.py

"""Elliptic curve parameters and coordinate system definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class CoordinateSystem(Enum):
    """Coordinate system used for internal arithmetic.

    Two systems are supported:

    - **AFFINE** — points are (x, y).  Each operation requires one modular
      inversion, which is simple but relatively slow.
    - **JACOBIAN** — points are (X, Y, Z) with x = X/Z², y = Y/Z³.
      Avoids inversions during addition/doubling (~3x faster for scalar
      multiplication) at the cost of a single inversion when converting
      back to affine form.
    """

    AFFINE = auto()
    JACOBIAN = auto()


@dataclass(frozen=True)
class CurveParams:
    """Immutable parameters defining an elliptic curve y² = x³ + ax + b (mod p).

    A valid (non-singular) elliptic curve requires a non-zero discriminant:

        Δ = -16(4a³ + 27b²) ≠ 0  (mod p)

    This is verified automatically at construction time; attempting to
    create a ``CurveParams`` with 4a³ + 27b² ≡ 0 (mod p) raises
    ``ValueError``.

    .. note::

       For cryptographic security the group order *n* should be at
       least 2¹⁶⁰ (see NIST SP 800-57).  This library does not
       enforce a minimum order so that small "toy" curves can be used
       for educational purposes.

    Attributes:
        p: Prime order of the finite field.
        a: Coefficient 'a' in the curve equation.
        b: Coefficient 'b' in the curve equation.
        n: Order of the generator point.
        h: Cofactor.
        coord: Coordinate system used for internal computations.
    """

    p: int
    a: int
    b: int
    n: int
    h: int = 1
    coord: CoordinateSystem = CoordinateSystem.JACOBIAN

    def __post_init__(self) -> None:
        """Validate that the curve is non-singular: 4a³ + 27b² ≠ 0 (mod p)."""
        discriminant = (
            4 * pow(self.a, 3, self.p) + 27 * pow(self.b, 2, self.p)
        ) % self.p
        if discriminant == 0:
            raise ValueError(
                f"Singular curve: 4a³ + 27b² ≡ 0 (mod p) for a={self.a}, b={self.b}, p={self.p}. "
                "The discriminant must be non-zero for a valid elliptic curve."
            )
