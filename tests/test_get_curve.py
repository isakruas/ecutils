import unittest

from ecutils.curves import get, secp256k1


class TestGetCurve(unittest.TestCase):
    """Test cases for the get function to retrieve elliptic curves."""

    def test_get_valid_curve(self):
        """Test that a valid curve name returns the correct EllipticCurve object."""
        curve_name = "secp256k1"
        expected_curve = secp256k1
        curve = get(curve_name)
        self.assertEqual(
            curve, expected_curve, f"Should retrieve the curve {curve_name}."
        )

    def test_get_invalid_curve(self):
        """Test that an invalid curve name raises a KeyError."""
        curve_name = "invalidCurveName"
        with self.assertRaises(
            KeyError,
            msg="Should raise KeyError with appropriate message for invalid curve name.",
        ):
            get(curve_name)
