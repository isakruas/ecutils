from ecc import ECC


class ECK:
    """
    /***********************************************************************
    * Copyright (c) 2021 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * file COPYING or https://github.com/isakruas/ecc/blob/master/LICENSE.*
    ***********************************************************************/

    https://en.wikipedia.org/wiki/Elliptic-curve_cryptography
    """

    def __init__(self) -> None:
        self.ecc = ECC('secp521r1')

    def encode(self, m: str) -> tuple:

        n = len(m)

        b = 2**16

        d = 100

        m = sum(ord(m[k])*b**k for k in range(n))

        for j in range(d):
            x = (d*m + j) % self.ecc.p
            s = (x**3 + self.ecc.a*x + self.ecc.b) % self.ecc.p
            if s == pow(s, int((self.ecc.p + 1) / 2), self.ecc.p):
                y = pow(s, int((self.ecc.p + 1) / 4), self.ecc.p)
                break

        return (x, y)

    def decode(self, m: tuple) -> str:

        (x, _) = m

        b = 2**16

        d = 100

        decode = []

        m = x // d

        while m != 0:
            decode.append(chr(m % b))
            m //= b

        return ''.join(decode)
