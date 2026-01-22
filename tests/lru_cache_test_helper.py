import os

from ecutils.core import EllipticCurveOperations
from ecutils.curves import get


def test_lru_cache():
    """
    Tests the LRU cache by calling a cached function multiple times and checking the cache info.
    """
    curve = get("secp256r1")
    p1 = curve.G
    p2 = curve.multiply_point(2, curve.G)

    EllipticCurveOperations.add_points.cache_clear()

    # Call the function multiple times
    for _ in range(10):
        curve.add_points(p1, p2)

    return EllipticCurveOperations.add_points.cache_info()


if __name__ == "__main__":
    cache_info = test_lru_cache()
    if os.environ.get("LRU_CACHE_MAXSIZE") == "0":
        assert (
            cache_info.hits == 0
        ), "Cache should not be used when LRU_CACHE_MAXSIZE is 0"
    else:
        assert (
            cache_info.hits > 0
        ), "Cache should be used when LRU_CACHE_MAXSIZE is not 0"
    print("Test passed")
