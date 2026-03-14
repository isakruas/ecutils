# ecutils/core/arithmetic/jacobian.py

"""Elliptic curve arithmetic in Jacobian (projective) coordinates."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from ecutils.core.curve import CurveParams
from ecutils.utils.settings import LRU_CACHE_MAXSIZE

if TYPE_CHECKING:
    from ecutils.core.point import Point


@dataclass(frozen=True)
class _JacobianPoint:
    """A point in Jacobian projective coordinates (X, Y, Z).

    The affine point (x, y) corresponds to (X/Z², Y/Z³).
    The identity element is represented by x=None, y=None.
    """

    x: int | None = None
    y: int | None = None
    z: int = 1


def to_jacobian(pt: Point) -> _JacobianPoint:
    """Convert an affine Point to Jacobian coordinates."""
    if pt.is_identity:
        return _JacobianPoint()
    return _JacobianPoint(pt.x, pt.y, 1)


def to_affine(jp: _JacobianPoint, curve: CurveParams) -> tuple[int | None, int | None]:
    """Convert a _JacobianPoint back to affine (x, y) coordinates."""
    if jp.x is None or jp.y is None or jp.z == 0:
        return (None, None)
    inv_z = pow(jp.z, -1, curve.p)
    return (
        (jp.x * inv_z**2) % curve.p,
        (jp.y * inv_z**3) % curve.p,
    )


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def jac_double(jp: _JacobianPoint, curve: CurveParams) -> _JacobianPoint:
    """Double a point in Jacobian coordinates."""
    if jp.x is None or jp.y is None or jp.y == 0:
        return _JacobianPoint()
    p = curve.p
    ysq = jp.y * jp.y % p
    zsqr = jp.z * jp.z % p
    s = 4 * jp.x * ysq % p
    m = (3 * jp.x * jp.x + curve.a * zsqr * zsqr) % p
    nx = (m * m - 2 * s) % p
    ny = (m * (s - nx) - 8 * ysq * ysq) % p
    nz = 2 * jp.y * jp.z % p
    return _JacobianPoint(nx, ny, nz)


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def jac_add(
    jp1: _JacobianPoint, jp2: _JacobianPoint, curve: CurveParams
) -> _JacobianPoint:
    """Add two points in Jacobian coordinates."""
    if jp1.x is None or jp1.y is None:
        return jp2
    if jp2.x is None or jp2.y is None:
        return jp1
    p = curve.p
    z1z1 = jp1.z * jp1.z % p
    z2z2 = jp2.z * jp2.z % p
    u1 = jp1.x * z2z2 % p
    u2 = jp2.x * z1z1 % p
    s1 = jp1.y * jp2.z * z2z2 % p
    s2 = jp2.y * jp1.z * z1z1 % p
    if u1 == u2:
        if s1 != s2:
            return _JacobianPoint()
        return jac_double(jp1, curve)
    h = u2 - u1
    i = (2 * h) * (2 * h) % p
    j = h * i % p
    r = 2 * (s2 - s1) % p
    v = u1 * i % p
    x = (r * r - j - 2 * v) % p
    y = (r * (v - x) - 2 * s1 * j) % p
    z = ((jp1.z + jp2.z) ** 2 - z1z1 - z2z2) * h % p
    return _JacobianPoint(x, y, z)


def jac_mul(k: int, jp: _JacobianPoint, curve: CurveParams) -> _JacobianPoint:
    """Scalar multiplication in Jacobian coordinates (double-and-add)."""
    if k == 0 or jp.x is None or jp.y is None:
        return _JacobianPoint()
    result = _JacobianPoint()
    bits = bin(k)[2:]
    for i in range(len(bits)):
        if bits[-i - 1] == "1":
            result = jac_add(result, jp, curve)
        jp = jac_double(jp, curve)
    return result
