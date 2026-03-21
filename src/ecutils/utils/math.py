# ecutils/utils/math.py

"""Modular arithmetic utilities for elliptic curve operations.

Provides quadratic residue testing and modular square root computation,
essential building blocks for point decompression and Koblitz encoding.
"""

from __future__ import annotations


def is_quadratic_residue(a: int, p: int) -> bool:
    """Check whether *a* is a quadratic residue modulo *p* using Euler's criterion.

    A non-zero integer *a* is a quadratic residue mod *p* (an odd prime) iff:

        a^((p-1)/2) ≡ 1 (mod p)

    Args:
        a: The integer to test (will be reduced mod *p*).
        p: An odd prime.

    Returns:
        ``True`` if *a* is a quadratic residue mod *p*, ``False`` otherwise.
        Returns ``False`` when ``a ≡ 0 (mod p)``.
    """
    a = a % p
    if a == 0:
        return False
    return pow(a, (p - 1) // 2, p) == 1


def modular_sqrt(a: int, p: int) -> int | None:
    """Compute a square root of *a* modulo *p*, or ``None`` if none exists.

    Uses the direct formula when ``p ≡ 3 (mod 4)`` and falls back to
    the Tonelli-Shanks algorithm for the general case.

    Args:
        a: The value whose square root is sought (reduced mod *p*).
        p: An odd prime.

    Returns:
        An integer *r* such that ``r² ≡ a (mod p)``, or ``None`` if *a*
        is not a quadratic residue mod *p*.
    """
    a = a % p
    if a == 0:
        return 0

    if not is_quadratic_residue(a, p):
        return None

    # Shortcut for p ≡ 3 (mod 4)
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Tonelli-Shanks algorithm for the general case (p ≡ 1 mod 4)
    # Factor out powers of 2: p - 1 = Q * 2^S
    s = 0
    q = p - 1
    while q % 2 == 0:
        q //= 2
        s += 1

    # Find a quadratic non-residue
    z = 2
    while is_quadratic_residue(z, p):
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while True:
        if t == 1:
            return r
        # Find the least i such that t^(2^i) ≡ 1 (mod p)
        i = 1
        temp = (t * t) % p
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
        # Update
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p
