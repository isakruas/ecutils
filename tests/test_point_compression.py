import unittest

from ecutils.core.curve import CurveParams
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator


class TestPointCompression(unittest.TestCase):
    """Tests for Point.compress() and Point.decompress()."""

    def setUp(self):
        """Set up a small test curve: y² = x³ + x + 1 over F₂₃."""
        self.curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
        self.P = Point(x=0, y=1, curve=self.curve)

    def test_compress_roundtrip(self):
        """Compressing then decompressing should recover the same point."""
        x, parity = self.P.compress()
        recovered = Point.decompress(x, parity, self.curve)
        self.assertEqual(recovered.x, self.P.x)
        self.assertEqual(recovered.y, self.P.y)

    def test_compress_roundtrip_various_points(self):
        """Roundtrip for several points on the small curve."""
        Q = Point(x=6, y=19, curve=self.curve)
        for pt in [self.P, Q]:
            x, parity = pt.compress()
            recovered = Point.decompress(x, parity, self.curve)
            self.assertEqual(recovered.x, pt.x)
            self.assertEqual(recovered.y, pt.y)

    def test_compress_identity_raises(self):
        """Compressing the identity point should raise ValueError."""
        identity = Point()
        with self.assertRaises(ValueError):
            identity.compress()

    def test_decompress_invalid_x_raises(self):
        """An x-coordinate with no valid y should raise ValueError."""
        # Find an x where x³ + x + 1 is not a QR mod 23
        # x=2: 8 + 2 + 1 = 11, check if 11 is QR mod 23: 11^11 mod 23 = 22 ≠ 1 → not QR
        with self.assertRaises(ValueError):
            Point.decompress(2, 0, self.curve)

    def test_parity_selection(self):
        """Parity bit should select the correct y-coordinate."""
        x, parity0 = self.P.compress()
        # The other parity should give the negated point
        other_parity = 1 - parity0
        other_pt = Point.decompress(x, other_parity, self.curve)
        self.assertEqual(other_pt.x, self.P.x)
        self.assertEqual(other_pt.y, (self.curve.p - self.P.y) % self.curve.p)

    def test_generator_secp256k1_roundtrip(self):
        """Roundtrip compression of the secp256k1 generator point."""
        curve = get_curve("secp256k1")
        G = get_generator("secp256k1")
        x, parity = G.compress()
        recovered = Point.decompress(x, parity, curve)
        self.assertEqual(recovered.x, G.x)
        self.assertEqual(recovered.y, G.y)
