import unittest

from ecutils.curves.registry import get_generator
from ecutils.protocols.massey_omura import MasseyOmura


class TestMasseyOmura(unittest.TestCase):
    """Test cases for the Massey-Omura encryption exchange."""

    def test_encryption_decryption(self):
        """Validate the complete encryption and decryption process."""
        private_key_sender = 123456
        mo_sender = MasseyOmura(private_key_sender)

        private_key_receiver = 654321
        mo_receiver = MasseyOmura(private_key_receiver)

        # Use the curve's generator point as the message
        message = get_generator(mo_sender.curve_name)

        # Sender encrypts the message
        encrypted_by_sender = mo_sender.encrypt(message)

        # Receiver encrypts the already encrypted message
        encrypted_by_receiver = mo_receiver.encrypt(encrypted_by_sender)

        # Sender decrypts the message partly
        partially_decrypted_by_sender = mo_sender.decrypt(encrypted_by_receiver)

        # Receiver completes decryption
        fully_decrypted_message = mo_receiver.decrypt(partially_decrypted_by_sender)

        # The fully decrypted message should match the original message
        self.assertEqual(
            message.x,
            fully_decrypted_message.x,
            "Decrypted message should match the original one.",
        )
        self.assertEqual(
            message.y,
            fully_decrypted_message.y,
            "Decrypted message should match the original one.",
        )

    def test_point_multiplication(self):
        """Validate the point multiplication with the private key."""
        private_key = 123456
        mo = MasseyOmura(private_key)

        G = get_generator(mo.curve_name)

        # Perform point multiplication using private key and generator point.
        expected_point = private_key * G

        # Check if the resulting point is on the curve.
        self.assertTrue(
            expected_point.is_on_curve(),
            "The calculated point should lie on the curve.",
        )
