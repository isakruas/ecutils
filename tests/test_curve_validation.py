import unittest

from ecutils.core.curve import CoordinateSystem, CurveParams
from ecutils.curves.registry import _REGISTRY, get_curve


class TestCurveValidation(unittest.TestCase):
    """Test discriminant validation in CurveParams."""

    def test_valid_curve(self):
        """A well-formed curve should be created without errors."""
        curve = CurveParams(p=23, a=1, b=1, n=28, h=1)
        self.assertEqual(curve.p, 23)
        self.assertEqual(curve.a, 1)
        self.assertEqual(curve.b, 1)

    def test_singular_curve_raises(self):
        """A singular curve (4a³ + 27b² ≡ 0 mod p) must raise ValueError."""
        # y² = x³ (a=0, b=0) → discriminant = 0
        with self.assertRaises(
            ValueError, msg="Singular curve should raise ValueError"
        ):
            CurveParams(p=23, a=0, b=0, n=1)

    def test_singular_curve_nontrivial(self):
        """Another singular curve example: a=-3, b=2, p=7 → 4(-27)+27(4)=0 mod 7."""
        # 4*(-3)^3 + 27*(2)^2 = -108 + 108 = 0
        with self.assertRaises(ValueError):
            CurveParams(p=7, a=-3, b=2, n=1)

    def test_all_registry_curves_valid(self):
        """Every curve in the registry must pass discriminant validation."""
        for name in _REGISTRY:
            curve = get_curve(name)
            disc = (
                4 * pow(curve.a, 3, curve.p) + 27 * pow(curve.b, 2, curve.p)
            ) % curve.p
            self.assertNotEqual(
                disc, 0, f"Registry curve '{name}' has zero discriminant"
            )

    def test_valid_curve_with_affine_coord(self):
        """Valid curve with explicit AFFINE coordinate system."""
        curve = CurveParams(p=23, a=1, b=1, n=28, coord=CoordinateSystem.AFFINE)
        self.assertEqual(curve.coord, CoordinateSystem.AFFINE)
