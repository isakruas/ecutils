import unittest
from dataclasses import replace

from ecutils.algorithms.digital_signature import DigitalSignature
from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.core.point import Point
from ecutils.core.validation import same_domain, validate_public_key
from ecutils.curves.registry import get_curve, get_generator
from ecutils.protocols.diffie_hellman import DiffieHellman
from ecutils.protocols.massey_omura import MasseyOmura

# Point.__mul__ reduces the scalar modulo the point's own n.  A peer that
# supplies a Point on a foreign curve with small order r would receive
# (d mod r)·Q and learn the residue of the private key d modulo r; with
# several coprime r the residues combine via the CRT.

# Toy curves over F₁₇ with points of small order 3, 5 and 7:
# (p, a, b, n, x, y)
FOREIGN_DOMAINS = [
    (17, 0, 1, 3, 0, 1),
    (17, 1, 5, 5, 5, 4),
    (17, 1, 4, 7, 4, 2),
]


def foreign_point(p, a, b, n, x, y):
    return Point(x, y, CurveParams(p=p, a=a, b=b, n=n, h=1))


# y² = x³ + x + 1 over F₂₃ has 28 = 4·7 points; (5, 4) has order 7,
# (4, 0) has order 2 and (0, 1) has order 28.
COFACTOR_CURVE = CurveParams(p=23, a=1, b=1, n=7, h=4)


class TestSameDomain(unittest.TestCase):
    """Structural comparison of curve domains."""

    def test_equal_parameters_match(self):
        self.assertTrue(same_domain(get_curve("secp256k1"), get_curve("secp256k1")))

    def test_coordinate_system_is_ignored(self):
        curve = get_curve("secp256k1")
        affine = replace(curve, coord=CoordinateSystem.AFFINE)
        self.assertTrue(same_domain(curve, affine))

    def test_different_curves_or_none_do_not_match(self):
        curve = get_curve("secp256k1")
        self.assertFalse(same_domain(curve, get_curve("secp256r1")))
        self.assertFalse(same_domain(curve, None))
        self.assertFalse(same_domain(None, curve))

    def test_single_differing_parameter_does_not_match(self):
        curve = get_curve("secp256k1")
        self.assertFalse(same_domain(curve, replace(curve, n=3)))
        self.assertFalse(same_domain(curve, replace(curve, h=2)))


class TestValidatePublicKey(unittest.TestCase):
    """Full public-key validation against a trusted domain."""

    def setUp(self):
        self.curve = get_curve("secp256k1")
        self.G = get_generator("secp256k1")

    def test_accepts_valid_point(self):
        self.assertIs(validate_public_key(self.G, self.curve), self.G)

    def test_rejects_non_point_values(self):
        with self.assertRaisesRegex(ValueError, "Point instance"):
            validate_public_key(None, self.curve)
        with self.assertRaisesRegex(ValueError, "Point instance"):
            validate_public_key((self.G.x, self.G.y), self.curve)

    def test_rejects_point_without_curve(self):
        with self.assertRaisesRegex(ValueError, "configured curve domain"):
            validate_public_key(Point(self.G.x, self.G.y), self.curve)

    def test_rejects_foreign_domains(self):
        for domain in FOREIGN_DOMAINS:
            with self.assertRaisesRegex(ValueError, "configured curve domain"):
                validate_public_key(foreign_point(*domain), self.curve)

    def test_rejects_identity(self):
        inf = Point(None, None, self.curve, _trusted=True)
        with self.assertRaisesRegex(ValueError, "point at infinity"):
            validate_public_key(inf, self.curve)

    def test_rejects_non_canonical_coordinates_even_when_trusted(self):
        big_x = Point(self.G.x + self.curve.p, self.G.y, self.curve, _trusted=True)
        with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
            validate_public_key(big_x, self.curve)
        neg_y = Point(self.G.x, -self.G.y, self.curve, _trusted=True)
        with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
            validate_public_key(neg_y, self.curve)
        bool_x = Point(True, self.G.y, self.curve, _trusted=True)
        with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
            validate_public_key(bool_x, self.curve)

    def test_rejects_off_curve_point_even_when_trusted(self):
        off = Point(self.G.x, self.G.y + 1, self.curve, _trusted=True)
        with self.assertRaisesRegex(ValueError, "not on the configured"):
            validate_public_key(off, self.curve)

    def test_cofactor_subgroup_check(self):
        in_subgroup = Point(5, 4, COFACTOR_CURVE)
        self.assertIs(validate_public_key(in_subgroup, COFACTOR_CURVE), in_subgroup)
        # order 2 and order 28: on the curve but outside the order-7 subgroup
        for x, y in [(4, 0), (0, 1)]:
            with self.assertRaisesRegex(ValueError, "prime-order subgroup"):
                validate_public_key(Point(x, y, COFACTOR_CURVE), COFACTOR_CURVE)


class TestPointCanonicalCoordinates(unittest.TestCase):
    """Point construction rejects coordinates outside [0, p-1]."""

    def setUp(self):
        self.curve = get_curve("secp256k1")
        self.G = get_generator("secp256k1")

    def test_constructor_rejects_out_of_range_coordinates(self):
        p = self.curve.p
        for x, y in [
            (self.G.x + p, self.G.y),
            (self.G.x, self.G.y + p),
            (self.G.x, self.G.y - p),
        ]:
            with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
                Point(x, y, self.curve)

    def test_from_sec1_rejects_compressed_x_equal_p_plus_one(self):
        data = b"\x02" + (self.curve.p + 1).to_bytes(32, "big")
        with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
            Point.from_sec1(data, self.curve)

    def test_from_sec1_rejects_uncompressed_x_out_of_range(self):
        data = b"\x04" + b"\xff" * 32 + self.G.y.to_bytes(32, "big")
        with self.assertRaisesRegex(ValueError, r"\[0, p-1\]"):
            Point.from_sec1(data, self.curve)


class TestDiffieHellmanPeerValidation(unittest.TestCase):
    """compute_shared_secret binds the peer key to the configured curve."""

    def setUp(self):
        self.victim = DiffieHellman(23, "secp256k1")

    def test_rejects_small_order_foreign_points(self):
        for domain in FOREIGN_DOMAINS:
            with self.assertRaisesRegex(ValueError, "configured curve domain"):
                self.victim.compute_shared_secret(foreign_point(*domain))

    def test_rejects_key_from_another_named_curve(self):
        other = DiffieHellman(5, "secp256r1")
        with self.assertRaisesRegex(ValueError, "configured curve domain"):
            self.victim.compute_shared_secret(other.public_key)

    def test_rejects_identity_peer_key(self):
        inf = Point(None, None, get_curve("secp256k1"), _trusted=True)
        with self.assertRaisesRegex(ValueError, "point at infinity"):
            self.victim.compute_shared_secret(inf)

    def test_rejects_identity_shared_secret(self):
        zero_key = DiffieHellman(get_curve("secp256k1").n, "secp256k1")
        peer = DiffieHellman(7, "secp256k1")
        with self.assertRaisesRegex(ValueError, "Shared secret is the point"):
            zero_key.compute_shared_secret(peer.public_key)

    def test_accepts_same_domain_with_other_coordinate_system(self):
        affine = replace(get_curve("secp256k1"), coord=CoordinateSystem.AFFINE)
        H = DiffieHellman(99, "secp256k1").public_key
        s1 = self.victim.compute_shared_secret(H)
        s2 = self.victim.compute_shared_secret(Point(H.x, H.y, affine))
        self.assertEqual(s1, s2)


class TestMasseyOmuraInputValidation(unittest.TestCase):
    """encrypt/decrypt reject points outside the configured curve."""

    def setUp(self):
        self.mo = MasseyOmura(0xA1, "secp521r1")

    def test_encrypt_and_decrypt_reject_foreign_points(self):
        for domain in FOREIGN_DOMAINS:
            with self.assertRaisesRegex(ValueError, "configured curve domain"):
                self.mo.encrypt(foreign_point(*domain))
            with self.assertRaisesRegex(ValueError, "configured curve domain"):
                self.mo.decrypt(foreign_point(*domain))

    def test_encrypt_rejects_identity(self):
        inf = Point(None, None, get_curve("secp521r1"), _trusted=True)
        with self.assertRaisesRegex(ValueError, "point at infinity"):
            self.mo.encrypt(inf)


class TestDigitalSignaturePublicKeyValidation(unittest.TestCase):
    """verify rejects public keys outside the configured curve."""

    def setUp(self):
        self.ds = DigitalSignature(12345)
        self.r, self.s = self.ds.sign(42)

    def test_verify_rejects_foreign_public_key(self):
        with self.assertRaisesRegex(ValueError, "configured curve domain"):
            self.ds.verify(foreign_point(*FOREIGN_DOMAINS[0]), 42, self.r, self.s)

    def test_verify_rejects_identity_public_key(self):
        inf = Point(None, None, get_curve("secp256k1"), _trusted=True)
        with self.assertRaisesRegex(ValueError, "point at infinity"):
            self.ds.verify(inf, 42, self.r, self.s)


if __name__ == "__main__":
    unittest.main()
