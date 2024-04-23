import unittest

from ecutils.core import EllipticCurve, Point
from ecutils.curves import secp192k1


class TestEllipticCurveOperations(unittest.TestCase):
    """Test cases for the EllipticCurveOperations implemented in the EllipticCurve class."""

    def setUp(self):
        """Set up an elliptic curve environment for testing."""
        self.curve = secp192k1
        self.point1 = Point(
            x=0xF091CF6331B1747684F5D2549CD1D4B3A8BED93B94F93CB6,
            y=0xFD7AF42E1E7565A02E6268661C5E42E603DA2D98A18F2ED5,
        )
        self.point2 = Point(
            x=0x6E43B7DCAE2FD5E0BF2A1BA7615CA3B9065487C9A67B4583,
            y=0xC48DCEA47AE08E84D5FEDC3D09E4C19606A290F7A19A6A58,
        )

    def test_point_addition(self):
        """Test the addition of two points on the curve."""
        expected_sum = Point(
            x=0x3CD61E370D02CA0687C0B5F7EBF6D0373F4DD0CCCCB7CC2D,
            y=0x2C4BEFD9B02F301EB4014504F0533AA7EB19E9EA56441F78,
        )
        calculated_sum = self.curve.add_points(self.point1, self.point2)
        self.assertEqual(
            calculated_sum, expected_sum, "Point addition result is incorrect."
        )

    def test_point_doubling(self):
        """Test the doubling of a point on the curve."""
        expected_double = Point(
            x=0xEA525DD5A1353762A14E9E78B9063316D1F2D5E792F87862,
            y=0xA936D583530982690C445427CDF2C5B0BB1C88749247B02E,
        )
        calculated_double = self.curve.add_points(self.point1, self.point1)
        self.assertEqual(
            calculated_double, expected_double, "Point doubling result is incorrect."
        )

    def test_scalar_multiplication(self):
        """Test the scalar multiplication of a point on the curve."""
        scalar = 2
        expected_product = Point(
            x=0xEA525DD5A1353762A14E9E78B9063316D1F2D5E792F87862,
            y=0xA936D583530982690C445427CDF2C5B0BB1C88749247B02E,
        )
        calculated_product = self.curve.multiply_point(scalar, self.point1)
        self.assertEqual(
            calculated_product,
            expected_product,
            "Scalar multiplication result is incorrect.",
        )

    def test_point_on_curve(self):
        """Test if the given point is on the curve."""
        self.assertTrue(
            self.curve.is_point_on_curve(self.point1),
            "The point should be on the curve.",
        )
        off_curve_point = Point(x=200, y=119)
        self.assertFalse(
            self.curve.is_point_on_curve(off_curve_point),
            "The point should not be on the curve.",
        )
        off_curve_point = Point()
        self.assertFalse(
            self.curve.is_point_on_curve(off_curve_point),
            "The point should not be on the curve.",
        )

    def test_invalid_point_addition(self):
        """Test adding invalid points not on the curve."""
        off_curve_point = Point(x=200, y=119)
        with self.assertRaises(ValueError):
            self.curve.add_points(self.point1, off_curve_point)

    def test_addition_with_identity(self):
        """Test adding a point on the curve with the identity element."""
        identity = Point()  # Assuming Point at infinity
        calculated_sum = self.curve.add_points(self.point1, identity)
        self.assertEqual(
            calculated_sum,
            self.point1,
            "Adding the identity element should return the original point.",
        )
        calculated_sum = self.curve.add_points(identity, self.point1)
        self.assertEqual(
            calculated_sum,
            self.point1,
            "Adding the identity element should return the original point.",
        )

    def test_invalid_scalar_multiplication(self):
        """Test scalar multiplication with invalid scalar or point."""
        with self.assertRaises(ValueError, msg="Test multiplying by scalar 0"):
            self.curve.multiply_point(0, self.point1)  # Test multiplying by scalar 0
        with self.assertRaises(
            ValueError, msg="Test multiplying by scalar n (or larger)"
        ):
            self.curve.multiply_point(
                self.curve.n, self.point1
            )  # Test multiplying by scalar n (or larger)
        off_curve_point = Point(x=200, y=119)
        with self.assertRaises(ValueError, msg="Test with point not on the curve"):
            self.curve.multiply_point(
                2, off_curve_point
            )  # Test with point not on the curve

    def test_addition_of_inverses_leading_to_infinity(self):
        """Test adding a point on the curve to its inverse, which should lead to
        the point at infinity."""
        inverse_point = Point(
            x=self.point1.x,
            y=(-self.point1.y) % self.curve.p,  # Calculating the modular inverse for y
        )
        identity_element = Point()  # Point at infinity representation with None values

        # Adding a point to its negation will result in the point at infinity
        calculated_sum = self.curve.add_points(self.point1, inverse_point)
        self.assertEqual(
            calculated_sum,
            identity_element,
            "Adding a point to its negation should give the point at infinity.",
        )

    def test_point_doubling_to_infinity(self):
        """Test the doubling of a point with y-coordinate zero, which should lead to
        the point at infinity due to division by zero (attempting to find the
        modular inverse of zero on an elliptic curve). This condition often represents
        'adding' a point to itself when the tangent at that point is vertical."""

        # Initialize the elliptic curve with given parameters.
        curve = EllipticCurve(
            p=13,  # The prime number defining the finite field.
            a=1,  # The 'a' coefficient of the elliptic curve equation.
            b=0,  # The 'b' coefficient of the elliptic curve equation.
            G=Point(x=2, y=1),  # The generator point for the curve group.
            n=4,  # The order of the base point G.
            h=0,  # The cofactor (not relevant in this test case).
        )

        # Create a point with a y-coordinate of zero (located at the curve's x-axis).
        point_with_y_zero = Point(x=0, y=0)

        # The expected result when a point is doubled, leading to the point at infinity,
        # is represented by a Point object with None values for both x and y coordinates.
        expected_result_at_infinity = Point()

        # Perform the doubling operation by adding the point to itself. Since the y-coordinate
        # is zero, and the doubling formula involves division by 2y, this operation should
        # theoretically lead to the point at infinity.
        result = curve.add_points(point_with_y_zero, point_with_y_zero)

        # Assert that the result of point doubling is the expected point at infinity.
        # This confirms proper handling of special cases involving the point at infinity.
        self.assertEqual(
            result,
            expected_result_at_infinity,
            "Doubling a point with y=0 should result in the point at infinity.",
        )

    def test_multiply_point_at_infinity(self):
        """Test the behavior of scalar multiplication when the point at infinity is
        involved. Multiplying any point by zero, or the point at infinity by any scalar,
        should result in the point at infinity. This reflects the identity property of
        the point at infinity in the group of points on an elliptic curve."""

        # Reinitialize the elliptic curve with the same parameters as before.
        curve = EllipticCurve(
            p=13,  # The prime number defining the finite field.
            a=1,  # The 'a' coefficient of the elliptic curve equation.
            b=0,  # The 'b' coefficient of the elliptic curve equation.
            G=Point(x=2, y=1),  # The generator point for the curve group.
            n=4,  # The order of the base point G.
            h=0,  # The cofactor.
        )

        # The point at infinity, represented as a point with no coordinates.
        point_at_infinity = Point()

        # The expected result of multiplying the point at infinity by any scalar.
        expected_result_at_infinity = Point()

        # Multiply the point at infinity by a scalar (here, scalar = 3).
        result = curve.multiply_point(3, point_at_infinity)

        # Assert that the multiplication result is the point at infinity.
        # This confirms the mathematical property of the point at infinity on elliptic curves.
        self.assertEqual(
            result,
            expected_result_at_infinity,
            "Multiplying the point at infinity by any scalar should remain the point at infinity.",
        )
