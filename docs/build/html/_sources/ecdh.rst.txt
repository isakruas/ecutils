ECDH
====

Protocol implementation

.. class:: ECDH(EC)

    .. attribute:: private_key

    .. attribute:: public_key

    .. function:: to_share(public_key: tuple) -> tuple

        Reference: https://en.wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman

Usage::

    from ecutils import ECDH

    rute = ECDH(private_key=7, curve='secp192k1')

    sibele = ECDH(private_key=21, curve='secp192k1')

    rute_shares_with_sibele = rute.to_share(sibele.public_key)

    sibele_shares_with_rute = sibele.to_share(rute.public_key)

    assert rute_shares_with_sibele == sibele_shares_with_rute
