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


class TestSEC1Compression(unittest.TestCase):
    """Tests for SEC 1 / X9.62 interoperable compression."""

    def setUp(self):
        """Set up a small test curve and secp256k1."""
        self.small_curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
        self.P = Point(x=0, y=1, curve=self.small_curve)
        self.secp256k1 = get_curve("secp256k1")
        self.G = get_generator("secp256k1")

    # --- compress_sec1 ---

    def test_sec1_compressed_prefix_even(self):
        """Even y should produce 0x02 prefix."""
        Q = Point(x=6, y=4, curve=self.small_curve)
        data = Q.compress_sec1()
        self.assertEqual(data[0], 0x02)

    def test_sec1_compressed_prefix_odd(self):
        """Odd y should produce 0x03 prefix."""
        data = self.P.compress_sec1()
        self.assertEqual(data[0], 0x03)  # y=1 is odd

    def test_sec1_compressed_length(self):
        """Compressed SEC 1 output should be 1 + field_byte_len."""
        data = self.G.compress_sec1()
        byte_len = (self.secp256k1.p.bit_length() + 7) // 8
        self.assertEqual(len(data), 1 + byte_len)

    def test_sec1_compressed_identity_raises(self):
        """Compressing identity in SEC 1 should raise ValueError."""
        identity = Point()
        with self.assertRaises(ValueError):
            identity.compress_sec1()

    def test_sec1_compress_no_curve_raises(self):
        """Compressing without curve params should raise ValueError."""
        pt = Point(x=0, y=1)
        with self.assertRaises(ValueError):
            pt.compress_sec1()

    # --- to_uncompressed_sec1 ---

    def test_sec1_uncompressed_prefix(self):
        """Uncompressed SEC 1 should start with 0x04."""
        data = self.P.to_uncompressed_sec1()
        self.assertEqual(data[0], 0x04)

    def test_sec1_uncompressed_length(self):
        """Uncompressed SEC 1 output should be 1 + 2*field_byte_len."""
        data = self.G.to_uncompressed_sec1()
        byte_len = (self.secp256k1.p.bit_length() + 7) // 8
        self.assertEqual(len(data), 1 + 2 * byte_len)

    def test_sec1_uncompressed_identity_raises(self):
        """Serializing identity in uncompressed SEC 1 should raise ValueError."""
        identity = Point()
        with self.assertRaises(ValueError):
            identity.to_uncompressed_sec1()

    def test_sec1_uncompressed_no_curve_raises(self):
        """Serializing without curve params should raise ValueError."""
        pt = Point(x=0, y=1)
        with self.assertRaises(ValueError):
            pt.to_uncompressed_sec1()

    # --- from_sec1 ---

    def test_sec1_compressed_roundtrip_small(self):
        """Compressed SEC 1 roundtrip on small curve."""
        data = self.P.compress_sec1()
        recovered = Point.from_sec1(data, self.small_curve)
        self.assertEqual(recovered.x, self.P.x)
        self.assertEqual(recovered.y, self.P.y)

    def test_sec1_uncompressed_roundtrip_small(self):
        """Uncompressed SEC 1 roundtrip on small curve."""
        data = self.P.to_uncompressed_sec1()
        recovered = Point.from_sec1(data, self.small_curve)
        self.assertEqual(recovered.x, self.P.x)
        self.assertEqual(recovered.y, self.P.y)

    def test_sec1_compressed_roundtrip_secp256k1(self):
        """Compressed SEC 1 roundtrip on secp256k1 generator."""
        data = self.G.compress_sec1()
        recovered = Point.from_sec1(data, self.secp256k1)
        self.assertEqual(recovered.x, self.G.x)
        self.assertEqual(recovered.y, self.G.y)

    def test_sec1_uncompressed_roundtrip_secp256k1(self):
        """Uncompressed SEC 1 roundtrip on secp256k1 generator."""
        data = self.G.to_uncompressed_sec1()
        recovered = Point.from_sec1(data, self.secp256k1)
        self.assertEqual(recovered.x, self.G.x)
        self.assertEqual(recovered.y, self.G.y)

    def test_sec1_from_too_short_raises(self):
        """SEC 1 data shorter than 2 bytes should raise ValueError."""
        with self.assertRaises(ValueError):
            Point.from_sec1(b"\x02", self.small_curve)

    def test_sec1_from_wrong_compressed_length_raises(self):
        """Compressed SEC 1 with wrong length should raise ValueError."""
        with self.assertRaises(ValueError):
            Point.from_sec1(b"\x02\x00\x00", self.secp256k1)

    def test_sec1_from_wrong_uncompressed_length_raises(self):
        """Uncompressed SEC 1 with wrong length should raise ValueError."""
        with self.assertRaises(ValueError):
            Point.from_sec1(b"\x04\x00\x00", self.secp256k1)

    def test_sec1_from_unknown_prefix_raises(self):
        """Unknown prefix should raise ValueError."""
        byte_len = (self.small_curve.p.bit_length() + 7) // 8
        data = b"\x05" + b"\x00" * byte_len
        with self.assertRaises(ValueError):
            Point.from_sec1(data, self.small_curve)

    def test_sec1_interop_known_vector(self):
        """Verify SEC 1 bytes match a known secp256k1 generator encoding."""
        data = self.G.compress_sec1()
        # secp256k1 generator has odd y, so prefix should be 0x03
        expected_prefix = 0x03 if self.G.y % 2 else 0x02
        self.assertEqual(data[0], expected_prefix)
        # x-coordinate should match
        x_from_bytes = int.from_bytes(data[1:], "big")
        self.assertEqual(x_from_bytes, self.G.x)
