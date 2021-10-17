# secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
g_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
g_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (g_x, g_y)


def dot(P, Q):

    (x_1, y_1) = P

    (x_2, y_2) = Q

    if P == Q:

        # 3*x_1**2+a (mod p)
        dy = pow(3, 1, p) * pow(x_1, 2, p) + pow(a, 1, p)

        # x_1**(p-2) (mod p) (inverso modular)
        dx = pow(2 * y_1, p - 2, p)

        m = dy * dx

        if not m:
            return (None, None)

        # m**2-(x_1+x_2) (mod p)
        x_3 = pow(pow(m, 2, p) - (x_1 + x_2), 1, p)

        # m*(x_1 - x_3)-y_1 (mod p)
        y_3 = pow(m * (x_1 - x_3) - y_1, 1, p)

        return (int(x_3), int(y_3))

    else:

        u = y_1 - y_2

        # (x_1 - x_2)**(p-2) (mod p) (inverso modular)
        v = pow(x_1 - x_2, p - 2, p)

        m = u * v

        if not m:
            return (None, None)

        # m**2-(x_1+x_2) (mod p)
        x_3 = pow(pow(m, 2, p) - (x_1 + x_2), 1, p)

        # m*(x_1 - x_3)-y_1 (mod p)
        y_3 = pow(m * (x_1 - x_3) - y_1, 1, p)

        return (int(x_3), int(y_3))


def trapdoor(G, key):
    P = G
    Q = None
    while key:
        if key & 1:
            if Q is None:
                Q = P
            else:
                Q = dot(Q, P)
        P = dot(P, P)
        key >>= 1
    return Q
