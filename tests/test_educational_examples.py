import unittest

from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.core.point import Point
from ecutils.utils.math import is_quadratic_residue, modular_sqrt


class TestEducationalExamplesZ23(unittest.TestCase):
    """Validate the educational examples from docstrings on E: y²=x³+x+1 over F₂₃."""

    def setUp(self):
        """Set up the small curve E: y² = x³ + x + 1 over F₂₃ (affine)."""
        self.curve = CurveParams(
            p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE
        )
        self.P = Point(x=0, y=1, curve=self.curve)
        self.Q = Point(x=6, y=19, curve=self.curve)

    def test_point_addition(self):
        """P(0,1) + Q(6,19) = (3,13) on E/F₂₃."""
        R = self.P + self.Q
        self.assertEqual(R.x, 3)
        self.assertEqual(R.y, 13)

    def test_point_doubling(self):
        """2·P(0,1) = (6,19) on E/F₂₃."""
        R = 2 * self.P
        self.assertEqual(R.x, 6)
        self.assertEqual(R.y, 19)

    def test_scalar_multiplication(self):
        """Scalar multiplication consistency: k*P computed step-by-step."""
        # 3*P = 2*P + P
        R2 = 2 * self.P
        R3_manual = R2 + self.P
        R3 = 3 * self.P
        self.assertEqual(R3.x, R3_manual.x)
        self.assertEqual(R3.y, R3_manual.y)

    def test_identity_element(self):
        """n*P = O (point at infinity, the identity element)."""
        identity = 28 * self.P  # n = 28
        self.assertTrue(identity.is_identity)

    def test_additive_inverse(self):
        """P + (-P) = O."""
        identity = self.P + (-self.P)
        self.assertTrue(identity.is_identity)

    def test_negation(self):
        """-P(0,1) = (0, 22) on F₂₃."""
        neg = -self.P
        self.assertEqual(neg.x, 0)
        self.assertEqual(neg.y, 22)


class TestEducationalExamplesZ7(unittest.TestCase):
    """Educational examples on a small curve over F₇."""

    def setUp(self):
        """E: y² = x³ + 2 over F₇ with n=9."""
        self.curve = CurveParams(p=7, a=0, b=2, n=9, h=1, coord=CoordinateSystem.AFFINE)

    def test_points_on_curve(self):
        """Verify some known points lie on y² = x³ + 2 mod 7."""
        # x=0: y²=2, √2 mod 7: 3²=9≡2 and 4²=16≡2 → (0,3) and (0,4)
        P = Point(x=0, y=3, curve=self.curve)
        self.assertTrue(P.is_on_curve())
        P2 = Point(x=0, y=4, curve=self.curve)
        self.assertTrue(P2.is_on_curve())

    def test_point_addition_z7(self):
        """Addition on the Z₇ curve."""
        P = Point(x=0, y=3, curve=self.curve)
        Q = Point(x=3, y=1, curve=self.curve)
        R = P + Q
        # Verify R is on the curve
        self.assertTrue(R.is_on_curve() or R.is_identity)


class TestEducationalQR(unittest.TestCase):
    """Educational examples for quadratic residues."""

    def test_qr_example_f23(self):
        """QR set of F₂₃ from the TCC: {1,2,3,4,6,8,9,12,13,16,18}."""
        expected_qr = {1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18}
        for a in range(1, 23):
            result = is_quadratic_residue(a, 23)
            self.assertEqual(result, a in expected_qr, f"QR({a}, 23)")

    def test_sqrt_example_f23(self):
        """√4 mod 23 should be ±2 (i.e., 2 or 21)."""
        r = modular_sqrt(4, 23)
        self.assertIn(r, [2, 21])
        self.assertEqual(pow(r, 2, 23), 4)

    def test_compression_small_curve(self):
        """Compress/decompress on the Z₂₃ educational curve."""
        curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
        P = Point(x=0, y=1, curve=curve)
        x, parity = P.compress()
        recovered = Point.decompress(x, parity, curve)
        self.assertEqual(recovered, P)


class TestEducationalJacobian(unittest.TestCase):
    """Verify Jacobian and affine arithmetic give the same results."""

    def test_affine_vs_jacobian_addition(self):
        """Point addition should yield the same result in both coordinate systems."""
        affine_curve = CurveParams(
            p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE
        )
        jacobian_curve = CurveParams(
            p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.JACOBIAN
        )
        Pa = Point(x=0, y=1, curve=affine_curve)
        Qa = Point(x=6, y=19, curve=affine_curve)
        Ra = Pa + Qa

        Pj = Point(x=0, y=1, curve=jacobian_curve)
        Qj = Point(x=6, y=19, curve=jacobian_curve)
        Rj = Pj + Qj

        self.assertEqual(Ra.x, Rj.x)
        self.assertEqual(Ra.y, Rj.y)

    def test_affine_vs_jacobian_scalar_mul(self):
        """Scalar multiplication should yield the same result in both systems."""
        affine_curve = CurveParams(
            p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.AFFINE
        )
        jacobian_curve = CurveParams(
            p=23, a=1, b=1, n=28, h=1, coord=CoordinateSystem.JACOBIAN
        )
        Pa = Point(x=0, y=1, curve=affine_curve)
        Pj = Point(x=0, y=1, curve=jacobian_curve)

        for k in [2, 5, 13, 27]:
            Ra = k * Pa
            Rj = k * Pj
            self.assertEqual(Ra.x, Rj.x, f"Mismatch at k={k}")
            self.assertEqual(Ra.y, Rj.y, f"Mismatch at k={k}")
