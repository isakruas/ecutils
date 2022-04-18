EC
==

Elementary mathematical operations on the curves secp192k1, secp192r1, secp224k1, secp224r1, secp256k1, secp256r1, secp384r1, secp521r1

.. class:: EC

    .. attribute:: p

    .. attribute:: a

    .. attribute:: b

    .. attribute:: G

    .. attribute:: n

    .. attribute:: h

    .. function:: gcd(m: int, n: int) -> int

        Reference: https://en.wikipedia.org/wiki/Euclidean_algorithm

    .. function:: egcd(m: int, n: int) -> tuple:

        Reference: Reference: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

    .. function:: mmi(m: int, n: int) -> int:

        Reference: https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

    .. function:: dot(P: tuple, Q: tuple) -> tuple

        Reference: https://en.wikipedia.org/wiki/Elliptic_curve

    .. function:: trapdoor(G: tuple, k: int) -> tuple

        Reference: https://en.wikipedia.org/wiki/Trapdoor_function


Usage::

    from ecutils import EC

    # Specify the curve to be used, if you omit the secp224k1 standard curve will be chosen
    ec = EC(curve='secp192k1')

    gcd = ec.gcd(ec.a, ec.b)

    assert gcd == 3

    gcd, x, y = ec.egcd(ec.a, ec.p)

    assert ec.a * x + ec.b * y == ec.gcd(ec.a, ec.b)

    mmi = ec.mmi(ec.b, ec.p)

    assert mmi == 4184734490257787175890526282138444277401570296306493027365

    P = ec.G

    Q = ec.G

    # P + Q
    dot = ec.dot(P, Q)

    assert dot == (
        5898748710631235793867485368048681928976741514058866965686,
        6215318586565457819081644608453878670902049430638930374357
    )

    k = 2

    # k * G, G = (x, y) in Fp
    trapdoor = ec.trapdoor(ec.G, k)

    assert trapdoor == dot
