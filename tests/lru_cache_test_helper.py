from ecutils.core.arithmetic.affine import affine_add
from ecutils.core.point import Point
from ecutils.curves.registry import get_curve, get_generator


def test_lru_cache():
    """
    Tests the LRU cache by calling a cached function multiple times and checking the cache info.
    """
    curve = get_curve("secp192k1")
    G = get_generator("secp192k1")
    p2 = 2 * G

    affine_add.cache_clear()

    # Call the function multiple times via Point operators
    # Use affine coordinates to exercise the affine_add cache
    from dataclasses import replace

    from ecutils.core.curve import CoordinateSystem

    affine_curve = replace(curve, coord=CoordinateSystem.AFFINE)
    p1_aff = Point(x=G.x, y=G.y, curve=affine_curve)
    p2_aff = Point(x=p2.x, y=p2.y, curve=affine_curve)

    for _ in range(10):
        p1_aff + p2_aff

    return affine_add.cache_info()


if __name__ == "__main__":
    cache_info = test_lru_cache()
    assert cache_info.hits > 0, "Cache should be used (hits > 0)"
    print("Test passed")
