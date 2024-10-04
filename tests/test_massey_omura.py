import unittest

from ecutils.protocols import MasseyOmura


class TestMasseyOmura(unittest.TestCase):
    """Test cases for the Massey-Omura encryption exchange."""

    def test_encryption_decryption(self):
        """Validate the complete encryption and decryption process."""
        private_key_sender = 123456
        mo_sender = MasseyOmura(private_key_sender)

        private_key_receiver = 654321
        mo_receiver = MasseyOmura(private_key_receiver)

        message = (
            mo_sender.curve.G
        )  # Let's use the curve's generator point for simplicity

        # Sender encrypts the message
        encrypted_by_sender = mo_sender.first_encryption_step(message)

        # Receiver encrypts the already encrypted message
        encrypted_by_receiver = mo_receiver.second_encryption_step(encrypted_by_sender)

        # Sender decrypts the message partly
        partially_decrypted_by_sender = mo_sender.partial_decryption_step(
            encrypted_by_receiver
        )

        # Receiver completes decryption
        fully_decrypted_message = mo_receiver.partial_decryption_step(
            partially_decrypted_by_sender
        )

        # The fully decrypted message should match the original message
        self.assertEqual(
            message,
            fully_decrypted_message,
            "Decrypted message should match the original one.",
        )

    def test_point_multiplication(self):
        """Validate the point multiplication with the private key."""
        private_key = 123456  # Define a test private key.
        mo = MasseyOmura(private_key)  # Initialize MasseyOmura instance.

        # Perform point multiplication using private key and generator point.
        public_key = mo.public_key
        expected_point = mo.curve.multiply_point(private_key, mo.curve.G)

        # Check if the resulting point is on the curve.
        self.assertTrue(
            mo.curve.is_point_on_curve(expected_point),
            "The calculated public key should lie on the curve.",
        )

        # Validate that the public_key computed using `multiply_point` matches what we derived directly.
        self.assertEqual(
            public_key,
            expected_point,
            "The public key calculated does not match the expected point from multiplication.",
        )
