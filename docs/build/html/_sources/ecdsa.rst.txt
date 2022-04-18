ECDSA
=====

Protocol implementation

.. class:: ECDSA(EC)

    .. attribute:: private_key

    .. attribute:: public_key

    .. function:: signature(message: int) -> tuple

    .. function:: verify_signature(message: int, r: int, s: int, public_key: tuple) -> bool


Usage::

    from ecutils import ECDSA

    message = 123457

    private_key = 7

    ecdsa = ECDSA(curve='secp192k1', private_key=private_key)

    public_key = ecdsa.public_key
    # (5370475959698699548314844898721723603195636604449975017091, 4063159672567797276483870227243726761721476925977179091340)

    r, s = ecdsa.signature(message)
    # 3896243893660249727180523716996124911121694637270467027687 4776385274595455509621853448773273410465218979854252522627

    verify = ecdsa.verify_signature(message, r, s, public_key)

    assert verify is True
