from ecc.ecc import ECC


class ECK(ECC):
    """
    /***********************************************************************
    * Copyright (c) 2021 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ecc/blob/master/LICENSE.md              *
    ***********************************************************************/

    https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
    """

    def __init__(self, curve: str = None) -> None:
        super().__init__(curve=curve)

    def encode(self, m: str, a: int) -> tuple:

        n = len(m)

        b = 2**16

        m = sum(ord(m[k])*b**k for k in range(n))

        z = 1

        while True:
            x = (a*m + z) % self.p
            y = (x**3 + self.a*x + self.b) % self.p
            if y == pow(y, int((self.p + 1) / 2), self.p):
                y = pow(y, int((self.p + 1) / 4), self.p)
                break
            z += 1

        return (x, y, z)

    def decode(self, m: tuple, a: int) -> str:

        (x, y, z) = m

        b = 2**16

        decode = []

        m = (x - z) // a

        while m != 0:
            decode.append(chr(m % b))
            m //= b

        return ''.join(decode)
