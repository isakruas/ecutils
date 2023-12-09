from dataclasses import dataclass
from typing import Optional

from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve


@dataclass
class DiffieHellman:
    """Class to perform Diffie-Hellman key exchange using elliptic curves.

    Attributes:
        private_key (int): The private key of the user.
        curve_name (str): Name of the elliptic curve to be used. Defaults to 'secp192k1'.
        public_key (Optional[Point]): The calculated public key based on the private key and curve.
    """

    private_key: int
    curve_name: str = "secp192k1"
    public_key: Optional[Point] = None

    def __post_init__(self) -> None:
        """Initializes the Diffie-Hellman class and computes the public key if not provided."""

        self._curve = None
        if self.public_key is None:
            self.public_key = self.curve.multiply_point(self.private_key, self.curve.G)

    @property
    def curve(self) -> EllipticCurve:
        """Gets the elliptic curve based on the given curve name, if not already set."""

        if self._curve is None:
            self._curve = get_curve(self.curve_name)
        return self._curve

    def compute_shared_secret(self, other_public_key: Point) -> Point:
        """Computes the shared secret using the private key and the other party's public key.

        Args:
            other_public_key (Point): The other party's public key.

        Returns:
            Point: The resulting shared secret as a point on the elliptic curve.
        """

        return self.curve.multiply_point(self.private_key, other_public_key)


@dataclass
class MasseyOmura:
    """Class to perform Massey-Omura key exchange using elliptic curves.

    Attributes:
        private_key (int): The private key of the user.
        curve_name (str): Name of the elliptic curve to be used. Defaults to 'secp192k1'.
    """

    private_key: int
    curve_name: str = "secp192k1"

    def __post_init__(self) -> None:
        """Initializes the Massey-Omura class."""

        self._curve = None

    @property
    def curve(self) -> EllipticCurve:
        """Gets the elliptic curve based on the given curve name, if not already set."""

        if self._curve is None:
            self._curve = get_curve(self.curve_name)
        return self._curve

    def first_encryption_step(self, message: Point) -> Point:
        """Encrypts the message with the sender's private key."""

        return self.curve.multiply_point(self.private_key, message)

    def second_encryption_step(self, received_encrypted_message: Point) -> Point:
        """Applies the receiver's private key on the received encrypted message."""

        return self.first_encryption_step(received_encrypted_message)

    def partial_decryption_step(self, encrypted_message: Point) -> Point:
        """Partial decryption using the inverse of the sender's private key."""

        inverse_key = pow(self.private_key, -1, self.curve.n)
        return self.curve.multiply_point(inverse_key, encrypted_message)
