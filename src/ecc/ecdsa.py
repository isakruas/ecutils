from ecc.ecc import ECC
from random import randint


class ECDSA(ECC):
    """
    /***********************************************************************
    * Copyright (c) 2021 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ecc/blob/master/LICENSE.md              *
    ***********************************************************************/
    https://pt.wikipedia.org/wiki/ECDSA
    """

    def __init__(self, private_key: int = None, curve: str = None, **kwargs) -> None:
        super().__init__(curve=curve)
        if curve is None:
            self.__curve = 'secp256k1'
        else:
            self.__curve = curve
        if private_key is None:
            self.__private_key = None
        else:
            self.__private_key = private_key
        self.__public_key = None

    @property
    def private_key(self) -> int:
        return self.__private_key

    @property
    def public_key(self) -> tuple:
        if self.__public_key is None and self.__private_key is not None:
            self.__public_key = self.trapdoor(self.G, self.__private_key)
            return self.__public_key
        return self.__public_key

    def signature(self, message: int) -> tuple:

        (r, s) = (0, 0)

        while r == 0 or s == 0:

            k = randint(1, self.n - 1)

            (x, _) = self.trapdoor(self.G, k)

            r = x % self.n

            s = ((message + r * self.private_key) * (self.mmi(k, self.n))) % self.n

        return r, s

    def verify_signature(self, message: int, r: int, s: int, public_key: tuple) -> bool:

        P = self.trapdoor(self.G, (message * self.mmi(s, self.n)) % self.n)

        Q = self.trapdoor(public_key, (r * self.mmi(s, self.n)) % self.n)

        (x, y) = self.dot(P, Q)

        v = x % self.n

        return r == v
