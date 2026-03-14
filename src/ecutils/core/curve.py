# ecutils/core/curve.py

"""Elliptic curve parameters and coordinate system definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class CoordinateSystem(Enum):
    """Coordinate system used for internal arithmetic."""

    AFFINE = auto()
    JACOBIAN = auto()


@dataclass(frozen=True)
class CurveParams:
    """Immutable parameters defining an elliptic curve y² = x³ + ax + b (mod p).

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
