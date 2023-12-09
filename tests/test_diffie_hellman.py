import unittest

from ecutils.protocols import DiffieHellman


class TestDiffieHellman(unittest.TestCase):
    """Test cases for the Diffie-Hellman key exchange."""

    def test_compute_shared_secret(self):
        """Validate that both parties compute the same shared secret."""
        private_key_alice = 12345
        dh_alice = DiffieHellman(private_key_alice)
        private_key_bob = 67890
        dh_bob = DiffieHellman(private_key_bob)

        # Alice computes the shared secret using Bob's public key
        secret_alice = dh_alice.compute_shared_secret(dh_bob.public_key)

        # Bob computes the shared secret using Alice's public key
        secret_bob = dh_bob.compute_shared_secret(dh_alice.public_key)

        # The secrets should match
        self.assertEqual(secret_alice, secret_bob, "Shared secrets should be equal.")
