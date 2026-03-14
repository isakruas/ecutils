import unittest
from dataclasses import replace

from ecutils.core.curve import CoordinateSystem
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator
from ecutils.utils.settings import LRU_CACHE_MAXSIZE


class TestSettings(unittest.TestCase):
    def test_lru_cache_maxsize_is_defined(self):
        """Test that LRU_CACHE_MAXSIZE is defined and has a reasonable value."""
        self.assertIsInstance(LRU_CACHE_MAXSIZE, int)
        self.assertGreater(LRU_CACHE_MAXSIZE, 0)

    def test_coordinate_system_setting(self):
        """Test that the CoordinateSystem enum works correctly with CurveParams."""
        curve_jacobian = get_curve("secp256r1")
        self.assertEqual(curve_jacobian.coord, CoordinateSystem.JACOBIAN)

        curve_affine = replace(curve_jacobian, coord=CoordinateSystem.AFFINE)
        self.assertEqual(curve_affine.coord, CoordinateSystem.AFFINE)

    def test_affine_vs_jacobian_same_result(self):
        """Test that affine and Jacobian coordinates produce the same results."""
        curve_jac = get_curve("secp192k1")
        curve_aff = replace(curve_jac, coord=CoordinateSystem.AFFINE)

        G_jac = get_generator("secp192k1")
        G_aff = Point(x=G_jac.x, y=G_jac.y, curve=curve_aff)

        result_jac = 42 * G_jac
        result_aff = 42 * G_aff

        self.assertEqual(result_jac.x, result_aff.x)
        self.assertEqual(result_jac.y, result_aff.y)
