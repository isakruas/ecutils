import unittest

from ecutils.algorithms import DigitalSignature


class TestDigitalSignature(unittest.TestCase):
    """Test cases for the DigitalSignature class."""

    def setUp(self):
        """Set up digital signature environment."""
        self.private_key = 123456789
        self.ds = DigitalSignature(self.private_key)

    def test_generate_and_verify_signature(self):
        """Ensure that a signature generated can be verified as valid."""
        message_hash = hash("Signing this message")
        r, s = self.ds.generate_signature(message_hash)
        is_valid = self.ds.verify_signature(self.ds.public_key, message_hash, r, s)
        self.assertTrue(is_valid, "The signature should be valid.")

    def test_verify_signature_with_invalid_inputs(self):
        """Verify that invalid r and s raise a ValueError."""
        message_hash = hash("Signing this message")
        # Choose invalid r and s values (outside the range [1, n-1])
        invalid_r = self.ds.curve.n
        invalid_s = 0
        # Check that the appropriate exception is raised for invalid r and s
        with self.assertRaises(
            ValueError, msg="A ValueError should be raised for invalid r and s."
        ):
            self.ds.verify_signature(
                self.ds.public_key, message_hash, invalid_r, invalid_s
            )
