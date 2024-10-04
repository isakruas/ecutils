import unittest

from ecutils.algorithms import Koblitz


class TestKoblitz(unittest.TestCase):
    """Test cases for the Koblitz encoding and decoding methods."""

    def setUp(self):
        """Set up test cases environment."""
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
        encoded_messages = self.encoder.encode(
            lengthy_message, alphabet_size=2**8, lengthy=True
        )
        decoded_message = self.decoder.decode(
            encoded_messages, alphabet_size=2**8, lengthy=True
        )
        self.assertEqual(
            lengthy_message,
            decoded_message,
            "Decoded message should match the original lengthy message.",
        )
