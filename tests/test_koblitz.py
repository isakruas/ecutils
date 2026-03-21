import unittest

from ecutils.algorithms.koblitz import Koblitz


class TestKoblitz(unittest.TestCase):
    """Test cases for the Koblitz encoding and decoding methods."""

    def test_encode_decode_unicode(self):
        """Validate that encoding and then decoding retrieves the original message."""
        encoder = Koblitz(curve_name="secp192k1", alphabet_size=2**16)
        message = "Hello, EC!"
        encoded_point, j = encoder.encode(message)
        decoded_message = encoder.decode(encoded_point, j)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )

    def test_encode_decode_ascii(self):
        """Validate that encoding and then decoding retrieves the original message."""
        encoder = Koblitz(curve_name="secp192k1", alphabet_size=2**8)
        message = "Hello, EC!"
        encoded_point, j = encoder.encode(message)
        decoded_message = encoder.decode(encoded_point, j)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )

    def test_encode_decode_default(self):
        """Validate encoding/decoding with default settings (secp521r1, ASCII)."""
        encoder = Koblitz()
        message = "Hello, Elliptic Curve Cryptography!"
        encoded_point, j = encoder.encode(message)
        decoded_message = encoder.decode(encoded_point, j)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )

    def test_koblitz_encode_fail(self):
        """Test that Koblitz.encode raises ValueError if no valid point is found."""
        # Use a tiny curve where finding a point is impossible for most inputs
        from unittest.mock import patch

        from ecutils.core.curve import CurveParams

        koblitz = Koblitz(curve_name="secp192k1")

        with patch.object(
            type(koblitz),
            "_curve",
            new_callable=lambda: property(
                lambda self: CurveParams(p=7, a=1, b=1, n=7, h=1)
            ),
        ):
            # With such a small curve, Koblitz's method will likely fail
            # But to guarantee failure, we mock is_on_curve
            with patch("ecutils.core.point.Point.is_on_curve", return_value=False):
                with self.assertRaises(ValueError):
                    koblitz.encode("a")
