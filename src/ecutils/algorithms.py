from dataclasses import dataclass
from random import randint
from typing import Optional, Tuple

from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve


@dataclass
class Koblitz:
    """A class implementing the Koblitz method for encoding and decoding messages using elliptic curves.

    The Koblitz method allows encoding of textual messages to points on an elliptic curve and vice versa.
    It utilizes the functionality provided by ecutils to work with different elliptic curves.

    Attributes:
        curve_name (str): The name of the elliptic curve to be used. Defaults to 'secp521r1'.
    """

    curve_name: str = "secp521r1"

    def __post_init__(self) -> None:
        """Initializes the internal curve representation once the class instance is created."""
        self._curve = None

    @property
    def curve(self) -> EllipticCurve:
        """Lazy-loads and returns the elliptic curve used for encoding and decoding.

        The elliptic curve object is initialized based on the curve name when this property is accessed
        for the first time.

        Returns:
            EllipticCurve: An instance of `EllipticCurve` associated with the specified `curve_name`.
        """

        if self._curve is None:
            self._curve = get_curve(self.curve_name)
        return self._curve

    def encode(self, message: str, alphabet_size: int = 2**8) -> Tuple[Point, int]:
        """Encodes a textual message to a curve point using the Koblitz method.

        Args:
            message (str): The message to be encoded. Each character should be representable
                within the specified `alphabet_size`.
            alphabet_size (int): The size of the alphabet/character set to consider for encoding.
                Common values are 2**8 for ASCII and 2**16 for Unicode, which correspond to
                the number of values a single character can take.

        Returns:
            Tuple[Point, int]: A tuple with the encoded point on the elliptic curve and
                an auxiliary value j used in the encoding process.
        """

        # Convert the string message to a single large integer
        message_decimal = sum(
            ord(char) * (alphabet_size**i) for i, char in enumerate(message)
        )

        # Search for a valid curve point using the Koblitz method
        d = 100
        for j in range(1, d - 1):
            x = (d * message_decimal + j) % self.curve.p
            s = (x**3 + self.curve.a * x + self.curve.b) % self.curve.p

            # Check if 's' is a quadratic residue modulo 'p', meaning 'y' can be computed
            if s == pow(s, (self.curve.p + 1) // 2, self.curve.p):
                y = pow(s, (self.curve.p + 1) // 4, self.curve.p)

                # Verify that the computed point is on the curve
                if self.curve.is_point_on_curve(Point(x, y)):
                    break

        return Point(x, y), j

    @staticmethod
    def decode(point: Point, j: int, alphabet_size: int = 2**8) -> str:
        """Decodes a point on an elliptic curve to a textual message using the Koblitz method.

        Args:
            point (Point): The encoded point on the elliptic curve.
            j (int): The auxiliary value 'j' used during the encoding process.
            alphabet_size (int): The size of the alphabet/character set considered for decoding.

        Returns:
            str: The decoded textual message.
        """

        # Calculate the original large integer from the point and 'j'
        d = 100
        message_decimal = (point.x - j) // d

        # Decompose the large integer into individual characters based on `alphabet_size`
        characters = []
        while message_decimal != 0:
            characters.append(chr(message_decimal % alphabet_size))
            message_decimal //= alphabet_size

        # Convert the list of characters into a string and return it
        return "".join(characters)


@dataclass
class DigitalSignature:
    """Class to perform digital signature and verification using the ECDSA scheme.

    Attributes:
        private_key (int): The private key used for generating a signature.
        curve_name (str): The name of the elliptic curve to use. Defaults to 'secp192k1'.
        public_key (Optional[Point]): The public key corresponding to the private key.
            Automatically generated if not provided.
    """

    private_key: int
    curve_name: str = "secp192k1"
    public_key: Optional[Point] = None

    def __post_init__(self) -> None:
        """Initializes the DigitalSignature class and sets the public key."""

        self._curve = None
        if self.public_key is None:
            self.public_key = self.curve.multiply_point(self.private_key, self.curve.G)

    @property
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve based on the curve_name, if not already set."""

        if self._curve is None:
            self._curve = get_curve(self.curve_name)
        return self._curve

    def generate_signature(self, message_hash: int) -> Tuple[int, int]:
        """
        Generates an ECDSA signature for a given private key and message hash.

        Args:
            message_hash (int): The hash of the message to be signed.

        Returns:
            Tuple[int, int]: The ECDSA signature (r, s).

        Note:
            The random number k used in the signature process is chosen unpredictably for each signature.
        """

        (r, s) = (0, 0)
        while r == 0 or s == 0:
            k = randint(a=1, b=self.curve.n - 1)
            p = self.curve.multiply_point(k, self.curve.G)
            r = p.x % self.curve.n
            s = (
                (message_hash + r * self.private_key) * pow(k, -1, self.curve.n)
            ) % self.curve.n
        return r, s

    def verify_signature(
        self, public_key: Point, message_hash: int, r: int, s: int
    ) -> bool:
        """
        Verifies the validity of an ECDSA signature against a public key and message hash.

        Args:
            public_key (Point): The public key corresponding to the signer's private key.
            message_hash (int): The hash of the message that was signed.
            r (int): The first component of the signature.
            s (int): The second component of the signature.

        Returns:
            bool: True if the signature is valid with respect to the given public key and message hash, False otherwise.

        Raises:
            ValueError: If r or s are not in the valid range [1, n-1], where n is the order of the curve.

        Examples:
            >>> ds = DigitalSignature(private_key=123456)
            >>> public_key = ds.public_key
            >>> message_hash = hash('message')
            >>> r, s = ds.generate_signature(message_hash)
            >>> ds.verify_signature(public_key, message_hash, r, s)
            True
        """

        if not (1 <= r < self.curve.n and 1 <= s < self.curve.n):
            raise ValueError("r or s are not in the valid range [1, curve order - 1].")

        w = pow(s, -1, self.curve.n)
        u_1 = (message_hash * w) % self.curve.n
        u_2 = (r * w) % self.curve.n
        p = self.curve.add_points(
            self.curve.multiply_point(u_1, self.curve.G),
            self.curve.multiply_point(u_2, public_key),
        )
        v = p.x % self.curve.n
        return v == r
