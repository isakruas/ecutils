# ecutils/protocols/diffie_hellman.py

"""Elliptic Curve Diffie-Hellman key exchange protocol.

Usage
-----
>>> from ecutils.protocols.diffie_hellman import DiffieHellman
>>>
>>> alice = DiffieHellman(private_key=0xA, curve_name="secp256k1")
>>> bob   = DiffieHellman(private_key=0xB, curve_name="secp256k1")
>>>
>>> shared_alice = alice.compute_shared_secret(bob.public_key)
>>> shared_bob   = bob.compute_shared_secret(alice.public_key)
>>> assert shared_alice == shared_bob
"""

from __future__ import annotations

from dataclasses import dataclass

from ecutils.core.point import Point
from ecutils.curves.registry import get_generator


@dataclass(frozen=True)
class DiffieHellman:
    """Elliptic Curve Diffie-Hellman key exchange.

    Protocol:
        1. Alice computes her public key: H_A = d_A · G
        2. Bob computes his public key:   H_B = d_B · G
        3. Shared secret: S = d_A · H_B = d_B · H_A = d_A · d_B · G

    Security relies on the Elliptic Curve Discrete Logarithm Problem
    (ECDLP): given G and Q = d·G, it is computationally infeasible to
    recover the private scalar *d*.

    Attributes:
        private_key: The private scalar (integer).
        curve_name:  Name of the curve (e.g. ``"secp256k1"``).
    """

    private_key: int
    curve_name: str = "secp256k1"

    # ----- derived properties -----

    @property
    def _G(self) -> Point:
        return get_generator(self.curve_name)

    @property
    def public_key(self) -> Point:
        """Compute the public key: ``private_key * G``."""
        return self.private_key * self._G

    # ----- protocol -----

    def compute_shared_secret(self, other_public_key: Point) -> Point:
        """Compute the shared secret from another party's public key.

        Args:
            other_public_key: The other party's public key point.

        Returns:
            The shared secret point ``private_key * other_public_key``.
        """
        return self.private_key * other_public_key
