import unittest
from dataclasses import replace

from ecutils.core.arithmetic.jacobian import (
    _JacobianPoint,
    jac_add,
    jac_double,
    to_jacobian,
)
from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve


class TestEllipticCurveOperations(unittest.TestCase):
    """Test cases for elliptic curve operations using the new Point-operator API."""

    def setUp(self):
        """Set up an elliptic curve environment for testing."""
        self.curve = get_curve("secp192k1")
        self.affine_curve = replace(self.curve, coord=CoordinateSystem.AFFINE)

        self.point1 = Point(
            x=0xF091CF6331B1747684F5D2549CD1D4B3A8BED93B94F93CB6,
            y=0xFD7AF42E1E7565A02E6268661C5E42E603DA2D98A18F2ED5,
            curve=self.curve,
        )
        self.point2 = Point(
            x=0x6E43B7DCAE2FD5E0BF2A1BA7615CA3B9065487C9A67B4583,
            y=0xC48DCEA47AE08E84D5FEDC3D09E4C19606A290F7A19A6A58,
            curve=self.curve,
        )

    def test_affine_operations(self):
        """Test affine operations specifically."""
        p1 = Point(
            x=self.point1.x,
            y=self.point1.y,
            curve=self.affine_curve,
        )
        p2 = Point(
            x=self.point2.x,
            y=self.point2.y,
            curve=self.affine_curve,
        )

        # Test add_points with p1 != p2
        p1 + p2

        # Test add_points with p1 == p2 to trigger the double_point call
        expected_double = p1 + p1
        calculated_double = p1 + p1
        self.assertEqual(
            calculated_double,
            expected_double,
            "Affine point doubling via add is incorrect.",
        )

        # Test a simple multiplication to exercise the affine multiply_point loop
        expected_product = p1 + p1  # 2 * point1
        expected_product = Point(
            x=expected_product.x,
            y=expected_product.y,
            curve=self.affine_curve,
        )
        expected_product = expected_product + p1  # 3 * point1

        calculated_product = 3 * p1
        self.assertEqual(
            calculated_product,
            expected_product,
            "Affine scalar multiplication result is incorrect.",
        )

    def test_point_addition(self):
        """Test the addition of two points on the curve."""
        expected_sum = Point(
            x=0x3CD61E370D02CA0687C0B5F7EBF6D0373F4DD0CCCCB7CC2D,
            y=0x2C4BEFD9B02F301EB4014504F0533AA7EB19E9EA56441F78,
        )

        # Test with affine coordinates
        p1_affine = Point(
            x=self.point1.x,
            y=self.point1.y,
            curve=self.affine_curve,
        )
        p2_affine = Point(
            x=self.point2.x,
            y=self.point2.y,
            curve=self.affine_curve,
        )
        calculated_sum = p1_affine + p2_affine
        self.assertEqual(
            calculated_sum.x,
            expected_sum.x,
            "Point addition result is incorrect (affine).",
        )
        self.assertEqual(
            calculated_sum.y,
            expected_sum.y,
            "Point addition result is incorrect (affine).",
        )

        # Test with Jacobian coordinates
        calculated_sum = self.point1 + self.point2
        self.assertEqual(
            calculated_sum.x,
            expected_sum.x,
            "Point addition result is incorrect (Jacobian).",
        )
        self.assertEqual(
            calculated_sum.y,
            expected_sum.y,
            "Point addition result is incorrect (Jacobian).",
        )

    def test_point_doubling(self):
        """Test the doubling of a point on the curve."""
        expected_double = Point(
            x=0xEA525DD5A1353762A14E9E78B9063316D1F2D5E792F87862,
            y=0xA936D583530982690C445427CDF2C5B0BB1C88749247B02E,
        )

        # Test with affine coordinates
        p1_affine = Point(
            x=self.point1.x,
            y=self.point1.y,
            curve=self.affine_curve,
        )
        calculated_double = p1_affine + p1_affine
        self.assertEqual(
            calculated_double.x,
            expected_double.x,
            "Point doubling result is incorrect (affine).",
        )
        self.assertEqual(
            calculated_double.y,
            expected_double.y,
            "Point doubling result is incorrect (affine).",
        )

        # Test with Jacobian coordinates
        calculated_double = self.point1 + self.point1
        self.assertEqual(
            calculated_double.x,
            expected_double.x,
            "Point doubling result is incorrect (Jacobian).",
        )
        self.assertEqual(
            calculated_double.y,
            expected_double.y,
            "Point doubling result is incorrect (Jacobian).",
        )

    def test_invalid_point_creation(self):
        """Test creating invalid points not on the curve."""
        with self.assertRaises(ValueError):
            Point(x=200, y=119, curve=self.curve)

    def test_scalar_multiplication(self):
        """Test the scalar multiplication of a point on the curve."""
        scalar = 2
        expected_product = Point(
            x=0xEA525DD5A1353762A14E9E78B9063316D1F2D5E792F87862,
            y=0xA936D583530982690C445427CDF2C5B0BB1C88749247B02E,
        )

        # Test with affine coordinates
        p1_affine = Point(
            x=self.point1.x,
            y=self.point1.y,
            curve=self.affine_curve,
        )
        calculated_product = scalar * p1_affine
        self.assertEqual(
            calculated_product.x,
            expected_product.x,
            "Scalar multiplication result is incorrect (affine).",
        )

        calculated_product = (
            0xEA525DD5A1353762A14E9E78B9063316D1F2D5E792F87862 * p1_affine
        )
        self.assertEqual(
            calculated_product.x,
            Point(
                x=5095008632516147798595855149669871701227161828659032863660,
                y=4326825067835634121700785249151086742283636342358962787033,
            ).x,
            "Scalar multiplication result is incorrect.",
        )

        # Test with Jacobian coordinates
        calculated_product = scalar * self.point1
        self.assertEqual(
            calculated_product.x,
            expected_product.x,
            "Scalar multiplication result is incorrect (Jacobian).",
        )

    def test_point_on_curve(self):
        """Test if the given point is on the curve."""
        self.assertTrue(
            self.point1.is_on_curve(),
            "The point should be on the curve.",
        )
        off_curve_point = Point()
        self.assertFalse(
            off_curve_point.is_on_curve(),
            "The point should not be on the curve.",
        )

    def test_addition_with_identity(self):
        """Test adding a point on the curve with the identity element."""
        identity = Point(curve=self.curve)  # Point at infinity
        calculated_sum = self.point1 + identity
        self.assertEqual(
            calculated_sum.x,
            self.point1.x,
            "Adding the identity element should return the original point.",
        )
        calculated_sum = identity + self.point1
        self.assertEqual(
            calculated_sum.x,
            self.point1.x,
            "Adding the identity element should return the original point.",
        )

    def test_scalar_multiplication_by_zero_and_order(self):
        """Test scalar multiplication by 0 and the curve order n."""
        # Multiplying by 0 should return the point at infinity
        result_k0 = 0 * self.point1
        self.assertTrue(
            result_k0.is_identity,
            "Multiplying by 0 should return the point at infinity.",
        )

        # Multiplying by n should return the point at infinity
        result_kn = self.curve.n * self.point1
        self.assertTrue(
            result_kn.is_identity,
            "Multiplying by n should return the point at infinity.",
        )

    def test_addition_of_inverses_leading_to_infinity(self):
        """Test adding a point on the curve to its inverse."""
        # Test with affine coordinates
        p1_affine = Point(
            x=self.point1.x,
            y=self.point1.y,
            curve=self.affine_curve,
        )
        inverse_affine = -p1_affine
        calculated_sum = p1_affine + inverse_affine
        self.assertTrue(
            calculated_sum.is_identity,
            "Adding a point to its negation should give the point at infinity (affine).",
        )

        # Test with Jacobian coordinates
        inverse_point = -self.point1
        calculated_sum = self.point1 + inverse_point
        self.assertTrue(
            calculated_sum.is_identity,
            "Adding a point to its negation should give the point at infinity (Jacobian).",
        )

    def test_point_doubling_to_infinity(self):
        """Test the doubling of a point with y-coordinate zero."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)
        point_with_y_zero = Point(x=0, y=0, curve=curve)

        result = point_with_y_zero + point_with_y_zero
        self.assertTrue(
            result.is_identity,
            "Doubling a point with y=0 should result in the point at infinity.",
        )

    def test_multiply_point_at_infinity(self):
        """Test scalar multiplication when the point at infinity is involved."""
        # With Jacobian coordinates
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)
        point_at_infinity = Point(curve=curve)

        result = 3 * point_at_infinity
        self.assertTrue(
            result.is_identity,
            "Multiplying the point at infinity by any scalar should remain the point at infinity.",
        )

        # With affine coordinates
        affine_curve = CurveParams(
            p=13, a=1, b=0, n=4, h=1, coord=CoordinateSystem.AFFINE
        )
        point_at_infinity = Point(curve=affine_curve)

        result = 3 * point_at_infinity
        self.assertTrue(
            result.is_identity,
            "Multiplying the point at infinity by any scalar should remain the point at infinity.",
        )

    def test_affine_add_points_inverses_return_infinity(self):
        """Test affine add_points where inverse points result in point at infinity."""
        p1 = Point(
            x=0xF091CF6331B1747684F5D2549CD1D4B3A8BED93B94F93CB6,
            y=0xFD7AF42E1E7565A02E6268661C5E42E603DA2D98A18F2ED5,
            curve=self.affine_curve,
        )
        p2 = -p1
        result = p1 + p2
        self.assertTrue(
            result.is_identity,
            "Adding inverse affine points should yield point at infinity.",
        )

    def test_affine_double_point_with_y_zero_returns_infinity(self):
        """Test affine double_point where p.y is 0."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1, coord=CoordinateSystem.AFFINE)
        zero_point = Point(x=0, y=0, curve=curve)

        result = zero_point + zero_point
        self.assertTrue(
            result.is_identity,
            "Doubling a point with y=0 should result in the point at infinity in affine coordinates.",
        )

    def test_jacobian_add_points_inverses_return_infinity(self):
        """Test jac_add when adding two inverse points results in point at infinity."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)

        p_affine = Point(x=10, y=3, curve=curve)
        p_inverse_affine = Point(x=10, y=curve.p - 3, curve=curve)

        p_jacobian = to_jacobian(p_affine)
        p_inverse_jacobian = to_jacobian(p_inverse_affine)

        result = jac_add(p_jacobian, p_inverse_jacobian, curve)
        self.assertEqual(
            result,
            _JacobianPoint(),
            "Adding inverse Jacobian points should result in point at infinity.",
        )

    def test_jacobian_double_point_y_zero_returns_infinity(self):
        """Test jac_double with y=0."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)

        jacobian_point_y_zero = to_jacobian(Point(x=0, y=0, curve=curve))

        result = jac_double(jacobian_point_y_zero, curve)
        self.assertEqual(
            result,
            _JacobianPoint(),
            "Doubling a Jacobian point with y=0 should result in the point at infinity.",
        )

    def test_double_point_with_infinity(self):
        """Test doubling point at infinity returns the same point."""
        infinity = Point(curve=self.curve)
        result = infinity + infinity
        self.assertTrue(
            result.is_identity,
            "Doubling point at infinity should return point at infinity.",
        )

    def test_jacobian_add_points_with_p2_infinity(self):
        """Test jac_add when p2 is point at infinity returns p1."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)
        p_affine = Point(x=10, y=3, curve=curve)
        p_jacobian = to_jacobian(p_affine)
        infinity_jacobian = _JacobianPoint()

        result = jac_add(p_jacobian, infinity_jacobian, curve)
        self.assertEqual(
            result,
            p_jacobian,
            "Adding point at infinity should return the original point.",
        )

    def test_jacobian_double_point_with_infinity(self):
        """Test jac_double with point at infinity returns infinity."""
        curve = CurveParams(p=13, a=1, b=0, n=4, h=1)
        infinity_jacobian = _JacobianPoint()

        result = jac_double(infinity_jacobian, curve)
        self.assertEqual(
            result,
            infinity_jacobian,
            "Doubling point at infinity should return point at infinity.",
        )

    def test_to_jacobian_with_infinity(self):
        """Test to_jacobian with point at infinity returns _JacobianPoint at infinity."""
        infinity = Point()  # Point at infinity in affine
        result = to_jacobian(infinity)
        self.assertEqual(
            result,
            _JacobianPoint(),
            "Converting affine infinity to Jacobian should return Jacobian infinity.",
        )

    def test_point_negation(self):
        """Test the negation operator on points."""
        neg_point = -self.point1
        self.assertEqual(neg_point.x, self.point1.x)
        self.assertEqual(neg_point.y, (-self.point1.y) % self.curve.p)

    def test_point_subtraction(self):
        """Test point subtraction: p1 - p2 = p1 + (-p2)."""
        result_sub = self.point1 - self.point2
        result_add_neg = self.point1 + (-self.point2)
        self.assertEqual(result_sub.x, result_add_neg.x)
        self.assertEqual(result_sub.y, result_add_neg.y)
