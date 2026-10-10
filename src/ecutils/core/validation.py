# ecutils/core/validation.py

"""Public-key and domain validation for security-sensitive APIs.

A ``Point`` carries its own ``CurveParams``, and ``k * P`` reduces the
scalar modulo the point's ``n``.  Protocols that multiply a *peer-supplied*
point by a *local secret* must therefore bind that point to the locally
trusted domain first; otherwise a peer can choose a foreign curve with a
small order *r* and learn ``d mod r`` from the result (see SEC 1 §3.2.2.1
and NIST SP 800-56A §5.6.2.3).

``validate_public_key`` performs full public-key validation:

1. the point carries curve parameters equal to the trusted domain
   (p, a, b, n, h — compared structurally, ``coord`` excluded)
2. the point is not the identity O
3. 0 ≤ x, y < p  (canonical field elements)
4. y² ≡ x³ + ax + b  (mod p)
5. n·Q = O when h > 1  (subgroup membership, computed WITHOUT reducing
   n mod n — ``n * Q`` would return O by construction)
"""

from __future__ import annotations

from ecutils.core.arithmetic.jacobian import jac_mul, to_jacobian
from ecutils.core.curve import CurveParams
from ecutils.core.point import Point


def same_domain(a: CurveParams | None, b: CurveParams | None) -> bool:
    """Return ``True`` when two ``CurveParams`` describe the same domain.

    The ``coord`` field is a representation choice, not a domain
    parameter, so it is intentionally ignored.
    """
    return (
        a is not None
        and b is not None
        and a.p == b.p
        and a.a == b.a
        and a.b == b.b
        and a.n == b.n
        and a.h == b.h
    )


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_public_key(point: Point, curve: CurveParams) -> Point:
    """Validate a peer-supplied public key against a trusted curve domain.

    Args:
        point: The untrusted public key.
        curve: The trusted, locally configured domain.

    Returns:
        The same point, for chaining.

    Raises:
        ValueError: If any validation step fails.
    """
    if not isinstance(point, Point):
        raise ValueError("Public key must be a Point instance.")
    if not same_domain(point.curve, curve):
        raise ValueError("Public key does not belong to the configured curve domain.")
    if point.is_identity:
        raise ValueError("Public key must not be the point at infinity.")
    if not (
        _is_int(point.x)
        and _is_int(point.y)
        and 0 <= point.x < curve.p  # type: ignore[operator]
        and 0 <= point.y < curve.p  # type: ignore[operator]
    ):
        raise ValueError("Public key coordinates must be integers in [0, p-1].")
    if not point.is_on_curve():
        raise ValueError("Public key is not on the configured elliptic curve.")
    if curve.h != 1:
        check = jac_mul(curve.n, to_jacobian(point), curve)
        if not (check.x is None or check.y is None or check.z == 0):
            raise ValueError("Public key is not in the prime-order subgroup.")
    return point
