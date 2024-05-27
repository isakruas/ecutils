import multiprocessing
from dataclasses import dataclass
from functools import lru_cache, partial
from random import randint
from typing import Tuple, Union

from ecutils.core import EllipticCurve, Point
from ecutils.curves import get as get_curve


@dataclass(frozen=True)
class Koblitz:
    """A class implementing the Koblitz method for encoding and decoding messages using elliptic curves.

    The Koblitz method allows encoding of textual messages to points on an elliptic curve and vice versa.
    It utilizes the functionality provided by ecutils to work with different elliptic curves.

    Attributes:
        curve_name (str): The name of the elliptic curve to be used. Defaults to 'secp521r1'.
    """

    curve_name: str = "secp521r1"

    @property
    @lru_cache(maxsize=1024, typed=True)
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve associated with this `Koblitz` instance.

        The elliptic curve object is initialized based on the `curve_name` attribute when this property is accessed
        for the first time. Caching ensures efficient reuse across multiple operations.

        Returns:
            EllipticCurve: An instance of `EllipticCurve` representing the curve used for encoding and decoding messages.
        """
        return get_curve(self.curve_name)

    @lru_cache(maxsize=1024, typed=True)
    def encode(
        self, message: str, alphabet_size: int = 2**8, lengthy=False
    ) -> Union[Tuple[Tuple[Point, int]], Tuple[Point, int]]:
        """Encodes a textual message to a point on the elliptic curve using the Koblitz method.

        This method efficiently converts a textual message (represented as a string) into a point
        on the elliptic curve associated with this `Koblitz` instance. The Koblitz method leverages
        the specified `alphabet_size` to map characters in the message to integers within a valid
        range.

        Args:
            message (str): The textual message to be encoded. Each character in the message should
                be representable within the provided `alphabet_size`. Common choices for `alphabet_size`
                include 2**8 for ASCII encoding and 2**16 for Unicode encoding, depending on the character
                set used in the message.
            alphabet_size (int, optional): The size of the alphabet/character set used in the message.
                    Defaults to 2**8 (256) for ASCII encoding. Higher values accommodate larger character sets.
            lengthy (bool, optional): A flag indicating whether the message is lengthy or not. If True, the method
                treats the `message` argument as a large message to be encoded in chunks. Defaults to False.

        Returns:
            Union[Tuple[Point, int], Tuple[Tuple[Point, int]]]:
                - If `lengthy` is False, a single tuple containing two elements is returned:
                    - The first element is a `Point` object representing the encoded point on the elliptic curve.
                    - The second element is an integer `j` that serves as an auxiliary value used during the
                    encoding process.
                - If `lengthy` is True, a tuple of tuples is returned. Each inner tuple follows the same format
                as the single tuple described above.
        """

        if alphabet_size == 2**8:
            size = 64
        else:
            size = 32

        # Encode a single message
        if not lengthy:
            # Convert the string message to a single large integer
            message_decimal = sum(
                ord(char) * (alphabet_size**i) for i, char in enumerate(message[:size])
            )

            # Search for a valid curve point using the Koblitz method
            d = 100  # Scaling factor
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

        # Initialize a multiprocessing pool
        pool = multiprocessing.Pool()

        # Execute the encode function in parallel using the pool
        encoded_messages = pool.map(
            partial(self.encode, alphabet_size=alphabet_size, lengthy=False),
            [message[i : i + size] for i in range(0, len(message), size)],
        )

        # Close the pool
        pool.close()
        pool.join()

        return tuple(encoded_messages)

    @lru_cache(maxsize=1024, typed=True)
    def decode(
        self,
        encoded: Union[Point, tuple[Tuple[Point, int]]],
        j: int = 0,
        alphabet_size: int = 2**8,
        lengthy=False,
    ) -> str:
        """Decodes a point on an elliptic curve to a textual message using the Koblitz method.

        This method recovers the original textual message from a point on the elliptic curve
        associated with this `Koblitz` class. The `decode` method leverages the Koblitz method and
        the provided `j` value, which was obtained during the encoding process, to recover the message.
        The specified `alphabet_size` is crucial for interpreting the integer values derived from the
        curve point and mapping them back to characters in the message.

        Args:
            encoded (Point): The encoded point on the elliptic curve to be decoded, or a tuple of tuples
                representing multiple encoded points if `lengthy` was True during encoding.
            j (int): The auxiliary value 'j' that was generated during the encoding process and is
                used to assist in the decoding process. Defaults to 0.
            alphabet_size (int, optional): The size of the alphabet/character set used in the message.
                    Defaults to 2**8 (256) for ASCII encoding. Higher values accommodate larger character sets.
            lengthy (bool, optional): A flag indicating whether the message was encoded in chunks. If True, the method
                treats the `encoded` argument as a collection of encoded messages to be decoded individually.
                Defaults to False.

        Returns:
            str: The decoded textual message that was originally encoded using the Koblitz method.

        Raises:
            ValueError: If the provided point is not on the elliptic curve associated with this `Koblitz` instance.
        """

        # Decode single point
        if not lengthy and isinstance(encoded, Point):
            # Calculate the original large integer from the point and 'j'
            d = 100  # Assuming 'd' is a scaling factor used in encoding
            message_decimal = (encoded.x - j) // d

            # Decompose the large integer into individual characters based on `alphabet_size`
            characters = []
            while message_decimal != 0:
                characters.append(chr(message_decimal % alphabet_size))
                message_decimal //= alphabet_size

            # Convert the list of characters into a string and return it
            return "".join(characters)

        # Decode tuple of (Point, int) pairs
        is_tuple_of_point_int = lambda instance: isinstance(instance, tuple) and all(
            isinstance(elem, tuple)
            and len(elem) == 2
            and isinstance(elem[0], Point)
            and isinstance(elem[1], int)
            for elem in instance
        )

        characters = []
        if is_tuple_of_point_int(encoded):

            # Initialize a multiprocessing pool
            pool = multiprocessing.Pool()

            # Execute the decode function in parallel using the pool
            characters = pool.starmap(
                partial(self.decode, alphabet_size=alphabet_size, lengthy=False),
                [(i[0], i[1]) for i in encoded],
            )

            # Close the pool
            pool.close()
            pool.join()

        return "".join(characters)


@dataclass(frozen=True)
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

    @property
    @lru_cache(maxsize=1024, typed=True)
    def curve(self) -> EllipticCurve:
        """Retrieves the elliptic curve associated with this `DigitalSignature` instance.

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
    def generate_signature(self, message_hash: int) -> Tuple[int, int]:
        """Generates an ECDSA signature for a given message hash using the private key.

        This method employs the Elliptic Curve Digital Signature Algorithm (ECDSA) to create a cryptographic
        signature for the provided `message_hash`. The signature generation process utilizes the private key
        associated with this `DigitalSignature` instance and a cryptographically secure random number `k` that
        is chosen for each signature to ensure security.

        Args:
            message_hash (int): The hash of the message to be signed. The hash function used should
                match the one used during message verification. Common hash functions include SHA-256 and SHA-384.

        Returns:
            Tuple[int, int]: The ECDSA signature as a tuple containing two integers (r, s). The signature
                can be used to verify the authenticity of the message and the signer's identity.

        Raises:
            ValueError: If the provided `message_hash` is not of type `int`.
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

    @lru_cache(maxsize=1024, typed=True)
    def verify_signature(
        self, public_key: Point, message_hash: int, r: int, s: int
    ) -> bool:
        """
        Verifies the authenticity of an ECDSA signature against a public key and message hash.

        This method employs the Elliptic Curve Digital Signature Algorithm (ECDSA) to
        verify the validity of a signature for a given `message_hash`. The verification process
        involves the provided `public_key`, which is assumed to correspond to the signer's
        private key, and the signature components `r` and `s`.

        Args:
            public_key (Point): The public key associated with the signer.
            message_hash (bytes): The hash of the message that was supposedly signed. The hash
                function used should match the one used during message signing. Common hash functions
                include SHA-256 and SHA-384.
            r (int): The first component (r) of the ECDSA signature.
            s (int): The second component (s) of the ECDSA signature.

        Returns:
            bool: True if the signature is valid with respect to the given public key and message hash,
                False otherwise. A valid signature confirms that the message originated from the
                entity with the corresponding private key and has not been tampered with.

        Raises:
            ValueError: If r or s are not within the valid range [1, n-1], where n is the order (number
                of elements) of the elliptic curve used for signature generation. This ensures the
                mathematical integrity of the signature verification process.
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
