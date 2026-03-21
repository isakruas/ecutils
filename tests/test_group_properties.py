import unittest
from dataclasses import replace

from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator


class TestGroupProperties(unittest.TestCase):
    """Verify that points on an elliptic curve form an abelian group."""

    def setUp(self):
        """Set up a small curve y² = x³ + x + 1 (mod 23), n=28."""
        self.curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
        self.P = Point(0, 1, self.curve)
        self.Q = Point(6, 19, self.curve)
        self.inf = Point(curve=self.curve)

    def test_identity_element_right(self):
        """P + O = P."""
        result = self.P + self.inf
        self.assertEqual(result, self.P)

    def test_identity_element_left(self):
        """O + P = P."""
        result = self.inf + self.P
        self.assertEqual(result, self.P)

    def test_inverse_element(self):
        """P + (-P) = O."""
        result = self.P + (-self.P)
        self.assertTrue(result.is_identity)

    def test_order_times_point(self):
        """n * P = O."""
        result = self.curve.n * self.P
        self.assertTrue(result.is_identity)

    def test_zero_times_point(self):
        """0 * P = O."""
        result = 0 * self.P
        self.assertTrue(result.is_identity)

    def test_one_times_point(self):
        """1 * P = P."""
        result = 1 * self.P
        self.assertEqual(result, self.P)

    def test_associativity(self):
        """(P + Q) + R == P + (Q + R)."""
        R = 3 * self.P
        lhs = (self.P + self.Q) + R
        rhs = self.P + (self.Q + R)
        self.assertEqual(lhs, rhs)

    def test_commutativity(self):
        """P + Q == Q + P."""
        self.assertEqual(self.P + self.Q, self.Q + self.P)

    def test_distributivity(self):
        """(a + b) * P == a * P + b * P."""
        a, b = 7, 13
        lhs = (a + b) * self.P
        rhs = a * self.P + b * self.P
        self.assertEqual(lhs, rhs)

    def test_double_equals_scalar_two(self):
        """P + P == 2 * P."""
        self.assertEqual(self.P + self.P, 2 * self.P)

    def test_rmul_equals_mul(self):
        """k * P == P * k."""
        self.assertEqual(5 * self.P, self.P * 5)


class TestJacobianAffineConsistency(unittest.TestCase):
    """Verify Jacobian and Affine arithmetic produce identical results."""

    def setUp(self):
        self.curve_jac = CurveParams(p=23, a=1, b=1, n=28, h=1)
        self.curve_aff = replace(self.curve_jac, coord=CoordinateSystem.AFFINE)
        self.P_jac = Point(0, 1, self.curve_jac)
        self.P_aff = Point(0, 1, self.curve_aff)

    def test_all_multiples_match(self):
        """k * P must agree for k = 1..n-1 in both coordinate systems."""
        for k in range(1, self.curve_jac.n):
            rj = k * self.P_jac
            ra = k * self.P_aff
            self.assertEqual(
                (rj.x, rj.y),
                (ra.x, ra.y),
                f"Mismatch at k={k}: jac={rj} aff={ra}",
            )

    def test_n_times_both_identity(self):
        """n * P = O in both systems."""
        self.assertTrue((self.curve_jac.n * self.P_jac).is_identity)
        self.assertTrue((self.curve_aff.n * self.P_aff).is_identity)

    def test_addition_matches(self):
        """P + Q must agree in both coordinate systems."""
        Q_jac = Point(6, 19, self.curve_jac)
        Q_aff = Point(6, 19, self.curve_aff)
        rj = self.P_jac + Q_jac
        ra = self.P_aff + Q_aff
        self.assertEqual((rj.x, rj.y), (ra.x, ra.y))


class TestGroupPropertiesRealCurve(unittest.TestCase):
    """Same group-law checks on a real-world curve (secp256k1)."""

    def setUp(self):
        self.curve = get_curve("secp256k1")
        self.G = get_generator("secp256k1")

    def test_generator_on_curve(self):
        self.assertTrue(self.G.is_on_curve())

    def test_order_times_generator(self):
        """n * G = O."""
        result = self.curve.n * self.G
        self.assertTrue(result.is_identity)

    def test_associativity(self):
        P = 7 * self.G
        Q = 13 * self.G
        R = 42 * self.G
        self.assertEqual((P + Q) + R, P + (Q + R))

    def test_commutativity(self):
        P = 7 * self.G
        Q = 13 * self.G
        self.assertEqual(P + Q, Q + P)

    def test_distributivity(self):
        a, b = 123, 456
        lhs = (a + b) * self.G
        rhs = a * self.G + b * self.G
        self.assertEqual(lhs, rhs)

    def test_inverse(self):
        P = 42 * self.G
        result = P + (-P)
        self.assertTrue(result.is_identity)
