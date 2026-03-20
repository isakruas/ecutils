# ecutils/algorithms/koblitz.py

"""Koblitz method for encoding/decoding messages as elliptic curve points.

Usage
-----
>>> from ecutils.algorithms.koblitz import Koblitz
>>>
>>> kob = Koblitz(curve_name="secp521r1")
>>> point, j = kob.encode("Hello, world!")
>>> text = kob.decode(point, j)
>>> assert text == "Hello, world!"
"""

from __future__ import annotations

from dataclasses import dataclass

from ecutils.core.point import Point
from ecutils.curves.registry import get_curve


@dataclass(frozen=True)
class Koblitz:
    """Koblitz message encoding/decoding on an elliptic curve.

    Encoding algorithm:
        1. Convert the message string to an integer *m* using base-α
           positional encoding (α = alphabet_size).
        2. For j = 1, 2, ..., d-1 compute x = d·m + j (mod p).
        3. Test if x³ + ax + b is a quadratic residue mod p (see
           :func:`ecutils.utils.math.is_quadratic_residue`).
        4. If yes, compute y = √(x³ + ax + b) mod p and return
           ``(Point(x, y), j)``.

    With d = 100 the probability of failure per attempt is ≈ 1/2, so the
    overall failure probability after 99 attempts is ≈ 2⁻⁹⁹.

    Attributes:
        curve_name: Name of the curve (e.g. ``"secp521r1"``).
                    Larger curves can encode longer messages in a single point.
        alphabet_size: Character set size. 256 for ASCII, 65536 for Unicode.
    """

    curve_name: str = "secp521r1"
    alphabet_size: int = 256

    # ----- derived properties -----

    @property
    def _curve(self):
        return get_curve(self.curve_name)

    # ----- encode -----

    def encode(self, message: str) -> tuple[Point, int]:
        """Encode a text message into a point on the curve.

        The message is first converted to an integer, then Koblitz's
        method is used to find a valid curve point derived from that integer.

        Args:
            message: The text to encode (limited by curve size).

        Returns:
            A tuple ``(point, j)`` where ``j`` is needed for decoding.

        Raises:
            ValueError: If no valid point is found (extremely unlikely).
        """
        curve = self._curve
        alpha = self.alphabet_size

        # Convert string -> integer  (base-alpha encoding)
        m = sum(ord(ch) * (alpha**i) for i, ch in enumerate(message))

        # Koblitz: try x = d*m + j until y² = x³ + ax + b has a root
        d = 100
        for j in range(1, d):
            x = (d * m + j) % curve.p
            s = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p

            # Euler criterion + Tonelli-like shortcut for p ≡ 3 (mod 4)
            if s == pow(s, (curve.p + 1) // 2, curve.p):
                y = pow(s, (curve.p + 1) // 4, curve.p)
                pt = Point(x, y, curve)
                if pt.is_on_curve():
                    return pt, j

        raise ValueError("Failed to encode message to a valid point on the curve.")

    # ----- decode -----

    def decode(self, point: Point, j: int) -> str:
        """Decode a curve point back into the original text message.

        Args:
            point: The encoded point (as returned by :meth:`encode`).
            j:     The auxiliary value returned alongside the point.

        Returns:
            The original text message.
        """
        alpha = self.alphabet_size
        d = 100
        m = (point.x - j) // d

        chars: list[str] = []
        while m > 0:
            chars.append(chr(m % alpha))
            m //= alpha
        return "".join(chars)
