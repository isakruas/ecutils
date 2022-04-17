class EC:
    """
    /***********************************************************************
    * Copyright (c) 2021 Isak Ruas                                        *
    * Distributed under the MIT software license, see the accompanying    *
    * https://github.com/isakruas/ecutils/blob/master/LICENSE.md          *
    ***********************************************************************/
    Supported curves: secp192k1, secp192r1, secp224k1, secp224r1, secp256k1,
    secp256r1, secp384r1, secp521r1

    Reference: https://www.secg.org/sec2-v2.pdf
    """

    parameters = {

        'secp192k1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFEE37,
            0x000000000000000000000000000000000000000000000000,
            0x000000000000000000000000000000000000000000000003,
            [0xDB4FF10EC057E9AE26B07D0280B7F4341DA5D1B1EAE06C7D,
             0x9B2F2F6D9C5628A7844163D015BE86344082AA88D95E2F9D],
            0xFFFFFFFFFFFFFFFFFFFFFFFE26F2FC170F69466A74DEFD8D,
            0x000000000000000000000000000000000000000000000001,
        ],

        'secp192r1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFC,
            0x64210519E59C80E70FA7E9AB72243049FEB8DEECC146B9B1,
            [0x188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012,
             0x07192B95FFC8DA78631011ED6B24CDD573F977A11E794811],
            0xFFFFFFFFFFFFFFFFFFFFFFFF99DEF836146BC9B1B4D22831,
            0x000000000000000000000000000000000000000000000001,
        ],

        'secp224k1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFE56D,
            0x00000000000000000000000000000000000000000000000000000000,
            0x00000000000000000000000000000000000000000000000000000005,
            [0xA1455B334DF099DF30FC28A169A467E9E47075A90F7E650EB6B7A45C,
             0x7E089FED7FBA344282CAFBD6F7E319F7C0B0BD59E2CA4BDB556D61A5],
            0x010000000000000000000000000001DCE8D2EC6184CAF0A971769FB1F7,
            0x00000000000000000000000000000000000000000000000000000001
        ],

        'secp224r1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF000000000000000000000001,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFE,
            0xB4050A850C04B3ABF54132565044B0B7D7BFD8BA270B39432355FFB4,
            [0xB70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21,
             0xBD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34],
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF16A2E0B8F03E13DD29455C5C2A3D,
            0x00000000000000000000000000000000000000000000000000000001
        ],

        'secp256k1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
            0x0000000000000000000000000000000000000000000000000000000000000000,
            0x0000000000000000000000000000000000000000000000000000000000000007,
            [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
             0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8],
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            0x000000000000000000000000000000000000000000000000000000
        ],

        'secp256r1': [
            0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
            0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC,
            0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
            [0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
             0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5],
            0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
            0x0000000000000000000000000000000000000000000000000000000000000001
        ],

        'secp384r1': [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC,
            0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF,
            [0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7,
             0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F],
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973,
            0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
        ],

        'secp521r1': [
            0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
            0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC,
            0x0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF109E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B503F00,
            [
                0x00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66,
                0x011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650],
            0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386409,
            0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
        ]

    }

    def __init__(self, curve: str = None, **kwargs) -> None:
        self.__curve = curve

    @property
    def p(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[0]

    @property
    def a(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[1]

    @property
    def b(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[2]

    @property
    def G(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[3]

    @property
    def n(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[4]

    @property
    def h(self):
        return self.parameters.get(self.__curve, self.parameters.get('secp256k1'))[5]

    def gcd(self, m: int, n: int) -> int:
        """
        Reference: https://en.wikipedia.org/wiki/Euclidean_algorithm
        """

        if m < n:
            m, n = (n, m)
        if n == 0: return m
        return self.gcd(n, m % n)

    def egcd(self, m: int, n: int) -> tuple:
        """
        Reference: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        """

        if n == 0:
            (d, x, y) = (m, 1, 0)
        else:
            (d, p, q) = self.egcd(n, m % n)
            x = q
            y = p - q * (m // n)
        return d, x, y

    def mmi(self, m: int, n: int) -> int:
        """
        Reference: https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
        """

        d, x, _ = self.egcd(m, n)
        if d != 1:
            raise ValueError('d != 1')
        else:
            return x % n

    def dot(self, P: tuple, Q: tuple) -> tuple:
        """
        Reference: https://en.wikipedia.org/wiki/Elliptic_curve
        """

        (x_1, y_1) = P

        (x_2, y_2) = Q

        if P == Q:

            # 3*x_1**2+a (mod p)
            dy = pow(3, 1, self.p) * pow(x_1, 2, self.p) + pow(self.a, 1, self.p)

            # x_1**(p-2) (mod p) (inverso modular)
            # dx = pow(2 * y_1, p - 2, p)
            dx = self.mmi(2 * y_1, self.p)

            m = dy * dx

            if not m:
                # infinity point
                return None, None

            # m**2-(x_1+x_2) (mod p)
            x_3 = pow(pow(m, 2, self.p) - (x_1 + x_2), 1, self.p)

            # m*(x_1 - x_3)-y_1 (mod p)
            y_3 = pow(m * (x_1 - x_3) - y_1, 1, self.p)

            return int(x_3), int(y_3)

        else:

            u = y_1 - y_2

            # (x_1 - x_2)**(p-2) (mod p) (inverso modular)
            # v = pow(x_1 - x_2, p - 2, p)
            v = self.mmi(x_1 - x_2, self.p)

            m = u * v

            if not m:
                # infinity point
                return None, None

            # m**2-(x_1+x_2) (mod p)
            x_3 = pow(pow(m, 2, self.p) - (x_1 + x_2), 1, self.p)

            # m*(x_1 - x_3)-y_1 (mod p)
            y_3 = pow(m * (x_1 - x_3) - y_1, 1, self.p)

            return int(x_3), int(y_3)

    def trapdoor(self, G: tuple, k: int) -> tuple:
        """
        Reference: https://en.wikipedia.org/wiki/Trapdoor_function
        """

        if k == 0 or k >= self.n:
            raise ValueError('k is not in 0 < k < n')

        P = G
        Q = None
        while k:
            if k & 1:
                if Q is None:
                    Q = P
                else:
                    Q = self.dot(Q, P)
            P = self.dot(P, P)
            k >>= 1
        return Q
