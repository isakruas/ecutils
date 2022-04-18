ECK
===

Protocol implementation

Reference: https://doi.org/10.1090/S0025-5718-1987-0866109-5

.. class:: ECK(EC)

    .. function:: encode(message: str, encode: int = 64) -> tuple

    .. function:: decode(self, P: tuple, encode: int = 64) -> str


Usage::

    from ecutils import ECK

    eck = ECK(curve='secp521r1')

    # Message (up to 64 bytes) to be encoded
    message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit integer.'

    encode = eck.encode(message)

    decode = eck.decode(encode)

    assert message == decode

    # Message (up to 32 bytes) to be encoded
    message = message[0:32]

    encode = eck.encode(message, encode=32)

    decode = eck.decode(encode, encode=32)

    assert message == decode
