# ecutils/core/arithmetic/affine.py

"""Elliptic curve arithmetic in affine coordinates."""

from __future__ import annotations

from functools import lru_cache

from ecutils.core.curve import CurveParams
from ecutils.utils.settings import LRU_CACHE_MAXSIZE


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def affine_double(
    px: int | None, py: int | None, curve: CurveParams
) -> tuple[int | None, int | None]:
    """Double a point in affine coordinates."""
    if px is None or py is None:
        return (None, None)
    p = curve.p
    n = (3 * px**2 + curve.a) % p
    d = (2 * py) % p
    try:
        inv = pow(d, -1, p)
    except ValueError:
        return (None, None)
    s = n * inv % p
    x3 = (s**2 - 2 * px) % p
    y3 = (s * (px - x3) - py) % p
    return (x3, y3)


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def affine_add(
    p1x: int | None,
    p1y: int | None,
    p2x: int | None,
    p2y: int | None,
    curve: CurveParams,
) -> tuple[int | None, int | None]:
    """Add two points in affine coordinates."""
    if p1x is None or p1y is None:
        return (p2x, p2y)
    if p2x is None or p2y is None:
        return (p1x, p1y)
    if p1x == p2x and p1y == p2y:
        return affine_double(p1x, p1y, curve)
    p = curve.p
    n = (p2y - p1y) % p
    d = (p2x - p1x) % p
    try:
        inv = pow(d, -1, p)
    except ValueError:
        return (None, None)
    s = n * inv % p
    x3 = (s**2 - p1x - p2x) % p
    y3 = (s * (p1x - x3) - p1y) % p
    return (x3, y3)


def affine_mul(
    k: int, px: int | None, py: int | None, curve: CurveParams
) -> tuple[int | None, int | None]:
    """Scalar multiplication in affine coordinates (double-and-add)."""
    if px is None or py is None or k == 0:
        return (None, None)
    rx: int | None = None
    ry: int | None = None
    while k > 0:
        if k & 1:
            rx, ry = affine_add(rx, ry, px, py, curve)
        px, py = affine_double(px, py, curve)
        k >>= 1
    return (rx, ry)
