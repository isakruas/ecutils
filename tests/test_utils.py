import unittest

from ecutils.core.arithmetic.affine import affine_add, affine_double
from ecutils.core.arithmetic.jacobian import jac_add, jac_double
from ecutils.utils.settings import LRU_CACHE_MAXSIZE


class TestUtils(unittest.TestCase):
    """Test cases for utility functions and settings."""

    def test_lru_cache_maxsize(self):
        """Test that LRU_CACHE_MAXSIZE has the expected default value."""
        self.assertEqual(LRU_CACHE_MAXSIZE, 256)

    def test_cached_functions_have_cache_info(self):
        """Test that cached arithmetic functions support cache_info."""
        # Verify the lru_cache decorator is applied
        self.assertTrue(hasattr(affine_add, "cache_info"))
        self.assertTrue(hasattr(affine_double, "cache_info"))
        self.assertTrue(hasattr(jac_add, "cache_info"))
        self.assertTrue(hasattr(jac_double, "cache_info"))
