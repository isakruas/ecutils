import os
import subprocess
import sys
import unittest

from ecutils.curves import get


class TestSettings(unittest.TestCase):
    def test_lru_cache_setting(self):
        """
        Test that the LRU_CACHE_MAXSIZE environment variable is respected.
        """
        # Test with LRU_CACHE_MAXSIZE = 0
        env = os.environ.copy()
        env["LRU_CACHE_MAXSIZE"] = "0"
        result = subprocess.run(
            [sys.executable, "tests/lru_cache_test_helper.py"],
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertIn("Test passed", result.stdout)
        self.assertEqual(result.returncode, 0)

        # Test with LRU_CACHE_MAXSIZE = 128
        env["LRU_CACHE_MAXSIZE"] = "128"
        result = subprocess.run(
            [sys.executable, "tests/lru_cache_test_helper.py"],
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertIn("Test passed", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_projective_coordinates_setting(self):
        """
        Test that the use_projective_coordinates parameter is respected.
        """
        # Test with use_projective_coordinates=False
        curve_affine = get("secp256r1", use_projective_coordinates=False)
        self.assertFalse(curve_affine.use_projective_coordinates)

        # Test with use_projective_coordinates=True
        curve_projective = get("secp256r1", use_projective_coordinates=True)
        self.assertTrue(curve_projective.use_projective_coordinates)
