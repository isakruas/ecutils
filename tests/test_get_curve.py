import unittest

from ecutils.curves import get, secp256k1


class TestGetCurve(unittest.TestCase):
    """Test cases for the get function to retrieve elliptic curves."""

    def test_get_valid_curve(self):
        """Test that a valid curve name returns the correct EllipticCurve object."""
        curve_name = "secp256k1"
        expected_curve = secp256k1
        curve = get(curve_name)
        self.assertEqual(curve.p, expected_curve.p)
        self.assertEqual(curve.a, expected_curve.a)
        self.assertEqual(curve.b, expected_curve.b)
        self.assertEqual(curve.G, expected_curve.G)
        self.assertEqual(curve.n, expected_curve.n)
        self.assertEqual(curve.h, expected_curve.h)
        self.assertEqual(
            curve.use_projective_coordinates, expected_curve.use_projective_coordinates
        )

    def test_get_invalid_curve(self):
        """Test that an invalid curve name raises a KeyError."""
        curve_name = "invalidCurveName"
        with self.assertRaises(
            KeyError,
            msg="Should raise KeyError with appropriate message for invalid curve name.",
        ):
            get(curve_name)
