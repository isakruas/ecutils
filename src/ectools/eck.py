from ectools.ec import EC


class ECK(EC):
    """
    /***********************************************************************
    * Copyright (c) 2021 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ectools/blob/master/LICENSE.md          *
    ***********************************************************************/

    Reference: https://doi.org/10.1090/S0025-5718-1987-0866109-5
    """

    def __init__(self, curve: str = None, **kwargs) -> None:
        super().__init__(curve=curve)

    def encode(self, message: str, encode: int = 64) -> tuple:
        # 32 or 64 bytes
        if encode == 32:
            m = message[0:32]
            b = 2 ** 16
        elif encode == 64:
            m = message[0:64]
            b = 2 ** 8
        else:
            raise ValueError('encode=32 or encode=64')
        A = self.a
        B = self.b
        p = self.p
        n = len(m)
        m = sum(ord(m[k]) * b ** k for k in range(n))
        d = min(int(p / m), 100)
        j = 0
        while True:
            x = (d * m + j) % p
            s = (x ** 3 + A * x + B) % p
            if s == pow(s, (p + 1) // 2, p):
                y = pow(s, (p + 1) // 4, p)
                break
            j += 1
        return x, y, j

    def decode(self, P: tuple, encode: int = 64) -> str:
        # 32 or 64 bytes
        if encode == 32:
            b = 2 ** 16
        elif encode == 64:
            b = 2 ** 8
        else:
            raise ValueError('encode=32 or encode=64')
        x, _, j = P
        x = x - j
        d = 100
        lst = []
        m = x // d
        while m != 0:
            lst.append(chr(m % b))
            m //= b
        return ''.join(lst)
