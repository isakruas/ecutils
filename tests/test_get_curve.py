import unittest

from ecutils.curves.registry import get_curve, get_generator


class TestGetCurve(unittest.TestCase):
    """Test cases for the get_curve and get_generator functions."""

    def test_get_valid_curve(self):
        """Test that a valid curve name returns a CurveParams object."""
        curve = get_curve("secp256k1")
        self.assertIsNotNone(curve.p)
        self.assertIsNotNone(curve.a)
        self.assertIsNotNone(curve.b)
        self.assertIsNotNone(curve.n)
        self.assertIsNotNone(curve.h)

    def test_get_generator(self):
        """Test that get_generator returns a valid Point on the curve."""
        G = get_generator("secp256k1")
        self.assertIsNotNone(G.x)
        self.assertIsNotNone(G.y)
        self.assertTrue(G.is_on_curve(), "Generator point should be on the curve.")

    def test_get_invalid_curve(self):
        """Test that an invalid curve name raises a KeyError."""
        with self.assertRaises(
            KeyError,
            msg="Should raise KeyError with appropriate message for invalid curve name.",
        ):
            get_curve("invalidCurveName")

    def test_get_invalid_generator(self):
        """Test that an invalid curve name raises a KeyError for get_generator."""
        with self.assertRaises(KeyError):
            get_generator("invalidCurveName")
