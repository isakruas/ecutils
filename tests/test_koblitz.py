import unittest
from unittest.mock import patch

from ecutils import settings
from ecutils.algorithms import Koblitz


class TestKoblitz(unittest.TestCase):
    """Test cases for the Koblitz encoding and decoding methods."""

    def setUp(self):
        """Set up test cases environment."""
        settings.LRU_CACHE_MAXSIZE = 0
        self.encoder = Koblitz(curve_name="secp192k1")
        self.decoder = Koblitz(curve_name="secp192k1")

    def test_encode_decode_unicode(self):
        """Validate that encoding and then decoding retrieves the original message."""
        message = "Hello, EC!"
        encoded_point, j = self.encoder.encode(message, alphabet_size=2**16)
        decoded_message = self.decoder.decode(encoded_point, j, alphabet_size=2**16)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )

    def test_encode_decode_ascii(self):
        """Validate that encoding and then decoding retrieves the original message."""
        message = "Hello, EC!"
        encoded_point, j = self.encoder.encode(message, alphabet_size=2**8)
        decoded_message = self.decoder.decode(encoded_point, j, alphabet_size=2**8)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )

    def test_encode_lengthy_message(self):
        """Test encoding and decoding a lengthy message using parallel processing."""
        self.encoder = Koblitz(curve_name="secp521r1")
        self.decoder = Koblitz(curve_name="secp521r1")
        lengthy_message = "Hello, Elliptic Curve Cryptography! " * 10
        encoded_data = self.encoder.encode(
            lengthy_message, alphabet_size=2**8, chunked=True
        )
        decoded_message = self.decoder.decode(
            encoded_data, alphabet_size=2**8, chunked=True
        )
        self.assertEqual(
            lengthy_message,
            decoded_message,
            "Decoded message should match the original lengthy message.",
        )

    def test_decode_invalid_input(self):
        """Test decoding with invalid input data."""
        with self.assertRaises(ValueError):
            self.decoder.decode("not a point", chunked=False)

    def test_decode_invalid_chunked_input(self):
        """Test decoding with invalid chunked input."""
        with self.assertRaises(ValueError):
            self.decoder.decode("not a tuple", chunked=True)

    @patch("ecutils.core.EllipticCurve.is_point_on_curve", return_value=False)
    def test_koblitz_encode_fail(self, mock_is_point_on_curve):
        """
        Test that Koblitz.encode raises a ValueError if it fails to find a point.
        """
        koblitz = Koblitz(curve_name="secp192k1")
        with self.assertRaises(ValueError):
            koblitz.encode("a")
