import unittest

from ecutils.algorithms import Koblitz


class TestKoblitz(unittest.TestCase):
    """Test cases for the Koblitz encoding and decoding methods."""

    def setUp(self):
        """Set up test cases environment."""
        self.encoder = Koblitz(curve_name="secp192k1")
        self.decoder = Koblitz(curve_name="secp192k1")

    def test_encode_decode(self):
        """Validate that encoding and then decoding retrieves the original message."""
        message = "Hello, EC!"
        encoded_point, j = self.encoder.encode(message)
        decoded_message = self.decoder.decode(encoded_point, j)
        self.assertEqual(
            message, decoded_message, "Decoded message should match the original."
        )
