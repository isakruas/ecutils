from dataclasses import dataclass
from functools import lru_cache

from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve
from ecutils.settings import LRU_CACHE_MAXSIZE


@dataclass(frozen=True)
class BaseProtocol:
    """Base class for cryptographic protocols providing common functionalities."""

    private_key: int
    curve_name: str = "secp192k1"

    @property
    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve for the protocol."""
        return get_curve(self.curve_name)

    @property
    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def public_key(self) -> Point:
        """Computes the public key from the private key."""
        return self.curve.multiply_point(self.private_key, self.curve.G)


@dataclass(frozen=True)
class DiffieHellman(BaseProtocol):
    """Class to perform Diffie-Hellman key exchange using elliptic curves."""

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def compute_shared_secret(self, other_public_key: Point) -> Point:
        """Computes the shared secret using the private key and the other party's public key.

        Args:
            other_public_key (Point): The other party's public key.

        Returns:
            Point: The resulting shared secret as a point on the elliptic curve.
        """
        return self.curve.multiply_point(self.private_key, other_public_key)


@dataclass(frozen=True)
class MasseyOmura(BaseProtocol):
    """Class to perform Massey-Omura key exchange using elliptic curves."""

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def first_encryption_step(self, message: Point) -> Point:
        """Encrypts the message with the sender's private key."""
        return self.curve.multiply_point(self.private_key, message)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def second_encryption_step(self, received_encrypted_message: Point) -> Point:
        """Applies the receiver's private key on the received encrypted message."""
        return self.first_encryption_step(received_encrypted_message)

    @lru_cache(maxsize=LRU_CACHE_MAXSIZE, typed=True)
    def partial_decryption_step(self, encrypted_message: Point) -> Point:
        """Partial decryption using the inverse of the sender's private key."""
        inverse_key = pow(self.private_key, -1, self.curve.n)
        return self.curve.multiply_point(inverse_key, encrypted_message)
