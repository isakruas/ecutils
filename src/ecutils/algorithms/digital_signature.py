# ecutils/algorithms/digital_signature.py

"""Elliptic Curve Digital Signature Algorithm (ECDSA).

Usage
-----
>>> import hashlib
>>> from ecutils.algorithms.digital_signature import DigitalSignature
>>>
>>> signer = DigitalSignature(private_key=123456, curve_name="secp256k1")
>>> msg_hash = int(hashlib.sha256(b"hello").hexdigest(), 16)
>>>
>>> r, s = signer.sign(msg_hash)
>>> assert signer.verify(signer.public_key, msg_hash, r, s)
"""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator


@dataclass(frozen=True)
class DigitalSignature:
    """ECDSA signature generation and verification.

    Attributes:
        private_key: The private scalar (integer).
        curve_name:  Name of the curve (e.g. ``"secp256k1"``).
    """

    private_key: int
    curve_name: str = "secp256k1"

    # ----- derived properties -----

    @property
    def _curve(self):
        return get_curve(self.curve_name)

    @property
    def _G(self) -> Point:
        return get_generator(self.curve_name)

    @property
    def public_key(self) -> Point:
        """Compute the public key: ``private_key * G``."""
        return self.private_key * self._G

    # ----- algorithm -----

    def sign(self, message_hash: int) -> tuple[int, int]:
        """Generate an ECDSA signature for a message hash.

        Algorithm:
            1. Choose random k ∈ [1, n-1]
            2. R = k·G,  r = R.x mod n
            3. s = (m + r·d) · k⁻¹ mod n   (d = private key, m = hash)

        .. warning::

           The nonce *k* must **never** be reused across different messages.
           Reusing *k* leaks the private key (as demonstrated in the
           2010 Sony PS3 ECDSA attack).

        Args:
            message_hash: Integer hash of the message (e.g. SHA-256).

        Returns:
            A tuple ``(r, s)`` representing the signature.
        """
        n = self._curve.n
        G = self._G
        r, s = 0, 0
        while r == 0 or s == 0:
            k = secrets.randbelow(n - 1) + 1
            R = k * G
            r = R.x % n
            s = ((message_hash + r * self.private_key) * pow(k, -1, n)) % n
        return r, s

    def verify(self, public_key: Point, message_hash: int, r: int, s: int) -> bool:
        """Verify an ECDSA signature.

        Algorithm:
            1. w  = s⁻¹ mod n
            2. u₁ = m·w mod n,  u₂ = r·w mod n
            3. R' = u₁·G + u₂·Q   (Q = public key)
            4. Accept iff R'.x mod n = r

        Args:
            public_key:   The signer's public key point.
            message_hash: Integer hash of the signed message.
            r:            First component of the signature.
            s:            Second component of the signature.

        Returns:
            ``True`` if the signature is valid, ``False`` otherwise.

        Raises:
            ValueError: If ``r`` or ``s`` are outside ``[1, n-1]``.
        """
        n = self._curve.n
        if not (1 <= r < n and 1 <= s < n):
            raise ValueError("r or s are not in the valid range [1, n-1].")

        G = self._G
        w = pow(s, -1, n)
        u1 = (message_hash * w) % n
        u2 = (r * w) % n
        R = u1 * G + u2 * public_key
        return R.x % n == r

    # ----- convenience wrappers -----

    def sign_message(self, message: bytes) -> tuple[int, int]:
        """Hash a message with SHA-256 and sign it.

        Args:
            message: The raw message bytes to sign.

        Returns:
            A tuple ``(r, s)`` representing the ECDSA signature.
        """
        message_hash = int(hashlib.sha256(message).hexdigest(), 16)
        return self.sign(message_hash)

    def verify_message(self, public_key: Point, message: bytes, r: int, s: int) -> bool:
        """Hash a message with SHA-256 and verify its ECDSA signature.

        Args:
            public_key: The signer's public key point.
            message:    The raw message bytes.
            r:          First component of the signature.
            s:          Second component of the signature.

        Returns:
            ``True`` if the signature is valid, ``False`` otherwise.
        """
        message_hash = int(hashlib.sha256(message).hexdigest(), 16)
        return self.verify(public_key, message_hash, r, s)
