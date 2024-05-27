from dataclasses import dataclass
from functools import lru_cache

from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve


@dataclass(frozen=True)
class DiffieHellman:
    """Class to perform Diffie-Hellman key exchange using elliptic curves.

    Attributes:
        private_key (int): The private key of the user.
        curve_name (str): Name of the elliptic curve to be used. Defaults to 'secp192k1'.
    """

    private_key: int
    curve_name: str = "secp192k1"

    @property
    @lru_cache(maxsize=1024, typed=True)
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve associated with this `DiffieHellman` instance.

        The `curve_name` attribute is used to fetch the corresponding elliptic curve object. If the
        curve object hasn't been retrieved yet, it is fetched from the `get_curve` function and
        cached for efficient reuse within the instance.

        Returns:
            EllipticCurve: The elliptic curve object used for ECDSA operations.
        """
        return get_curve(self.curve_name)

    @property
    @lru_cache(maxsize=1024, typed=True)
    def public_key(self) -> Point:
        """Computes and returns the public key corresponding to the private key.

        This property leverages the `curve` property to access the elliptic curve and the
        `multiply_point` method provided by the underlying elliptic curve library to
        calculate the public key. The public key is derived by multiplying the generator
        point (`G`) of the curve with the private key.

        Caching ensures efficient retrieval of the public key across multiple calls within the same instance.

        Returns:
            Point: The public key point on the elliptic curve associated with this instance.
        """
        return self.curve.multiply_point(self.private_key, self.curve.G)

    @lru_cache(maxsize=1024, typed=True)
    def compute_shared_secret(self, other_public_key: Point) -> Point:
        """Computes the shared secret using the private key and the other party's public key.

        Args:
            other_public_key (Point): The other party's public key.

        Returns:
            Point: The resulting shared secret as a point on the elliptic curve.
        """

        return self.curve.multiply_point(self.private_key, other_public_key)


@dataclass(frozen=True)
class MasseyOmura:
    """Class to perform Massey-Omura key exchange using elliptic curves.

    Attributes:
        private_key (int): The private key of the user.
        curve_name (str): Name of the elliptic curve to be used. Defaults to 'secp192k1'.
    """

    private_key: int
    curve_name: str = "secp192k1"

    @property
    @lru_cache(maxsize=1024, typed=True)
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve associated with this `MasseyOmura` instance.

        The `curve_name` attribute is used to fetch the corresponding elliptic curve object. If the
        curve object hasn't been retrieved yet, it is fetched from the `get_curve` function and
        cached for efficient reuse within the instance.

        Returns:
            EllipticCurve: The elliptic curve object used for ECDSA operations.
        """
        return get_curve(self.curve_name)

    @property
    @lru_cache(maxsize=1024, typed=True)
    def public_key(self) -> Point:
        """Computes and returns the public key corresponding to the private key.

        This property leverages the `curve` property to access the elliptic curve and the
        `multiply_point` method provided by the underlying elliptic curve library to
        calculate the public key. The public key is derived by multiplying the generator
        point (`G`) of the curve with the private key.

        Caching ensures efficient retrieval of the public key across multiple calls within the same instance.

        Returns:
            Point: The public key point on the elliptic curve associated with this instance.
        """
        return self.curve.multiply_point(self.private_key, self.curve.G)

    @lru_cache(maxsize=1024, typed=True)
    def first_encryption_step(self, message: Point) -> Point:
        """Encrypts the message with the sender's private key."""

        return self.curve.multiply_point(self.private_key, message)

    @lru_cache(maxsize=1024, typed=True)
    def second_encryption_step(self, received_encrypted_message: Point) -> Point:
        """Applies the receiver's private key on the received encrypted message."""

        return self.first_encryption_step(received_encrypted_message)

    @lru_cache(maxsize=1024, typed=True)
    def partial_decryption_step(self, encrypted_message: Point) -> Point:
        """Partial decryption using the inverse of the sender's private key."""

        inverse_key = pow(self.private_key, -1, self.curve.n)
        return self.curve.multiply_point(inverse_key, encrypted_message)
