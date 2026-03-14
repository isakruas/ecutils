# ecutils/protocols/massey_omura.py

"""Massey-Omura three-pass key exchange protocol over elliptic curves.

The protocol allows two parties to exchange a secret message (encoded as a
curve point) without sharing a key beforehand.  Each party uses only their
own private key; no public keys are ever transmitted.

Three-pass flow
---------------
1. Alice encrypts:   ``C1 = alice.encrypt(M)``
2. Bob encrypts:     ``C2 = bob.encrypt(C1)``
3. Alice decrypts:   ``C3 = alice.decrypt(C2)``
4. Bob decrypts:     ``M  = bob.decrypt(C3)``

Usage
-----
>>> from ecutils.protocols.massey_omura import MasseyOmura
>>> from ecutils.protocols.koblitz import Koblitz
>>>
>>> kob = Koblitz(curve_name="secp521r1")
>>> M, j = kob.encode("secret message")
>>>
>>> alice = MasseyOmura(private_key=0xA1, curve_name="secp521r1")
>>> bob   = MasseyOmura(private_key=0xB2, curve_name="secp521r1")
>>>
>>> c1 = alice.encrypt(M)        # Alice -> Bob
>>> c2 = bob.encrypt(c1)         # Bob -> Alice
>>> c3 = alice.decrypt(c2)       # Alice -> Bob
>>> plaintext = bob.decrypt(c3)  # Bob recovers M
>>> assert plaintext == M
"""

from __future__ import annotations

from dataclasses import dataclass

from ecutils.core.point import Point
from ecutils.curves.registry import get_curve


@dataclass(frozen=True)
class MasseyOmura:
    """Massey-Omura three-pass protocol.

    Attributes:
        private_key: The private scalar (integer), must be coprime with n.
        curve_name:  Name of the curve (e.g. ``"secp521r1"``).
    """

    private_key: int
    curve_name: str = "secp521r1"

    # ----- derived properties -----

    @property
    def _curve(self):
        return get_curve(self.curve_name)

    @property
    def _inverse_key(self) -> int:
        """Modular inverse of the private key mod n."""
        return pow(self.private_key, -1, self._curve.n)

    # ----- protocol -----

    def encrypt(self, point: Point) -> Point:
        """Encrypt (multiply) a point with the private key.

        Args:
            point: A curve point (message or partially encrypted).

        Returns:
            ``private_key * point``
        """
        return self.private_key * point

    def decrypt(self, point: Point) -> Point:
        """Decrypt (multiply) a point with the inverse of the private key.

        Args:
            point: A curve point to decrypt.

        Returns:
            ``private_key⁻¹ * point``
        """
        return self._inverse_key * point
