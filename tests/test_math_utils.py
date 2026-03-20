import unittest

from ecutils.utils.math import is_quadratic_residue, modular_sqrt


class TestIsQuadraticResidue(unittest.TestCase):
    """Tests for the Euler-criterion based QR check."""

    def test_known_qr(self):
        """1 is always a QR mod any prime."""
        self.assertTrue(is_quadratic_residue(1, 7))
        self.assertTrue(is_quadratic_residue(1, 23))

    def test_known_non_qr(self):
        """3 is not a QR mod 7 (3^3 = 27 ≡ 6 mod 7 ≠ 1)."""
        self.assertFalse(is_quadratic_residue(3, 7))

    def test_zero_is_not_qr(self):
        """0 mod p should return False."""
        self.assertFalse(is_quadratic_residue(0, 7))
        self.assertFalse(is_quadratic_residue(7, 7))

    def test_qr_mod_23(self):
        """Quadratic residues mod 23: {1,2,3,4,6,8,9,12,13,16,18}."""
        qr_set = {1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18}
        for a in range(1, 23):
            expected = a in qr_set
            self.assertEqual(
                is_quadratic_residue(a, 23),
                expected,
                f"QR check failed for a={a} mod 23",
            )

    def test_large_value_reduced(self):
        """Values larger than p should be reduced before testing."""
        # 25 ≡ 2 mod 23, and 2 is a QR mod 23
        self.assertTrue(is_quadratic_residue(25, 23))


class TestModularSqrt(unittest.TestCase):
    """Tests for modular square root computation."""

    def test_sqrt_p_3_mod_4(self):
        """p=23 ≡ 3 mod 4 → uses the direct formula."""
        # 4² = 16 ≡ 16 mod 23
        r = modular_sqrt(16, 23)
        self.assertIsNotNone(r)
        self.assertEqual(pow(r, 2, 23), 16)

    def test_sqrt_p_1_mod_4(self):
        """p=13 ≡ 1 mod 4 → uses Tonelli-Shanks."""
        # 3 is a QR mod 13: 4² = 16 ≡ 3 mod 13
        r = modular_sqrt(3, 13)
        self.assertIsNotNone(r)
        self.assertEqual(pow(r, 2, 13), 3)

    def test_non_residue_returns_none(self):
        """Non-QR should return None."""
        self.assertIsNone(modular_sqrt(5, 7))

    def test_sqrt_zero(self):
        """√0 = 0."""
        self.assertEqual(modular_sqrt(0, 7), 0)

    def test_roundtrip_all_qr_mod_23(self):
        """For every QR mod 23, sqrt should round-trip correctly."""
        for a in range(1, 23):
            r = modular_sqrt(a, 23)
            if r is not None:
                self.assertEqual(pow(r, 2, 23), a, f"sqrt({a}) mod 23 failed roundtrip")

    def test_tonelli_shanks_p_17(self):
        """p=17 ≡ 1 mod 4, testing Tonelli-Shanks with another prime."""
        # QR mod 17: 1,2,4,8,9,13,15,16
        for a in [1, 2, 4, 8, 9, 13, 15, 16]:
            r = modular_sqrt(a, 17)
            self.assertIsNotNone(r, f"{a} should be QR mod 17")
            self.assertEqual(pow(r, 2, 17), a)

    def test_tonelli_shanks_non_residue_p_17(self):
        """Non-QR mod 17 should return None."""
        for a in [3, 5, 6, 7, 10, 11, 12, 14]:
            self.assertIsNone(modular_sqrt(a, 17), f"{a} should not be QR mod 17")

    def test_tonelli_shanks_p_41(self):
        """p=41 ≡ 1 mod 8, higher power of 2 in factorization."""
        # 2 is a QR mod 41: 17² = 289 ≡ 2 mod 41
        r = modular_sqrt(2, 41)
        self.assertIsNotNone(r)
        self.assertEqual(pow(r, 2, 41), 2)
