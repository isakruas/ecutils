# ecutils/core/arithmetic/affine.py

"""Elliptic curve arithmetic in affine coordinates.

In affine coordinates a point on the curve y² = x³ + ax + b (mod p) is
represented directly by its (x, y) pair.  Each addition or doubling
requires one modular inversion, making this system straightforward but
slower than projective alternatives for scalar multiplication.

.. note::

   These routines are **not** constant-time and should not be used in
   production contexts where timing side-channels are a concern.
   See RFC 6090, Section 4 for background on secure implementation
   considerations.
"""

from __future__ import annotations

from functools import lru_cache

from ecutils.core.curve import CurveParams
from ecutils.utils.settings import LRU_CACHE_MAXSIZE


@lru_cache(maxsize=LRU_CACHE_MAXSIZE)
def affine_double(
    px: int | None, py: int | None, curve: CurveParams
) -> tuple[int | None, int | None]:
    """Double a point in affine coordinates.

    Computes 2P using the tangent-line formula:

        λ = (3x₁² + a) · (2y₁)⁻¹  (mod p)
        x₃ = λ² - 2x₁              (mod p)
        y₃ = λ(x₁ - x₃) - y₁      (mod p)

    Example (E: y² = x³ + x + 1 over F₂₃):

        >>> curve = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)
        >>> affine_double(0, 1, curve)
        (6, 19)
    """
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
    """Add two distinct points in affine coordinates.

    Given P₁ = (x₁, y₁) and P₂ = (x₂, y₂) with P₁ ≠ P₂, the chord-line
    formula is:

        λ  = (y₂ - y₁) · (x₂ - x₁)⁻¹  (mod p)
        x₃ = λ² - x₁ - x₂              (mod p)
        y₃ = λ(x₁ - x₃) - y₁           (mod p)

    If P₁ = P₂ the call is forwarded to :func:`affine_double`.

    Example (E: y² = x³ + x + 1 over F₂₃, P(0,1) + Q(6,19)):

        >>> curve = CurveParams(p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE)
        >>> affine_add(0, 1, 6, 19, curve)
        (3, 13)
    """
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
    """Scalar multiplication in affine coordinates (double-and-add).

    Computes k·P by scanning the bits of *k* from LSB to MSB,
    accumulating the result and doubling the base at each step.
    Runs in O(log k) doublings and at most O(log k) additions.

    .. warning::

       The double-and-add algorithm is **not** constant-time: the number
       of additions depends on the Hamming weight of *k*.  For
       constant-time requirements see RFC 6090, Section 4.
    """
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
