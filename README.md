# Elliptic Curve Cryptography
## Features
- ECC
- ECDH
- ECK
- ECDSA

### ECC
> Elementary mathematical operations on the curves secp192k1, secp192r1, secp224k1, secp224r1, secp256k1, secp256r1, secp384r1, secp521r1

| Methods | README |
| ------ | ------ |
| gcd | https://en.wikipedia.org/wiki/Euclidean_algorithm |
| egcd | https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm |
| mmi | https://en.wikipedia.org/wiki/Modular_multiplicative_inverse |
| dot | https://en.wikipedia.org/wiki/Elliptic_curve |
| trapdoor | https://en.wikipedia.org/wiki/Trapdoor_function |

#### Usage

```python
from ecc.ecc import ECC

# Specify the curve to be used, if you omit the secp224k1 standard curve will be chosen
ecc = ECC(curve='secp192k1')

gcd = ecc.gcd(ecc.a, ecc.b)

assert gcd == 3

gcd, x, y = ecc.egcd(ecc.a, ecc.p)

assert ecc.a*x + ecc.b*y == ecc.gcd(ecc.a, ecc.b)

mmi = ecc.mmi(ecc.b, ecc.p)

assert mmi == 4184734490257787175890526282138444277401570296306493027365

P = ecc.G

Q = ecc.G

# P + Q
dot = ecc.dot(P, Q)

assert dot == (
                5898748710631235793867485368048681928976741514058866965686,
                6215318586565457819081644608453878670902049430638930374357
              )

k = 2

# k * G, G = (x, y) in Fp
trapdoor = ecc.trapdoor(ecc.G, k)

assert trapdoor == dot
```

### ECDH
> Protocol implementation

| Methods | README |
| ------ | ------ |
| to_share | https://en.wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman |


```python
from ecc.ecdh import ECDH

rute = ECDH(private_key=7, curve='secp192k1')

sibele = ECDH(private_key=21, curve='secp192k1')

rute_shares_with_sibele = rute.to_share(sibele.public_key)

sibele_shares_with_rute = sibele.to_share(rute.public_key)

assert rute_shares_with_sibele == sibele_shares_with_rute
```

### ECK
> Protocol implementation

| Methods | README |
| ------ | ------ |
| encode | https://en.wikipedia.org/wiki/Elliptic-curve_cryptography |
| decode | https://en.wikipedia.org/wiki/Elliptic-curve_cryptography |

```python
from ecc.eck import ECK

eck = ECK(curve='secp521r1')

# Message (up to 64 bytes) to be encoded
message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit integer.'

encode = eck.encode(message)

decode  = eck.decode(encode)

assert message == decode

# Message (up to 32 bytes) to be encoded
message = message[0:32]

encode = eck.encode(message, e=32)

decode  = eck.decode(encode, e=32)

assert message == decode
```

### ECDSA
> Protocol implementation

| Methods | README |
| ------ | ------ |
| create | https://pt.wikipedia.org/wiki/ECDSA |
| verify | https://pt.wikipedia.org/wiki/ECDSA |

```python
from ecc.ecdsa import ECDSA

message = 123457

private_key = 7

ecdsa = ECDSA(curve='secp192k1', private_key=private_key)

public_key = ecdsa.public_key
# (5370475959698699548314844898721723603195636604449975017091, 4063159672567797276483870227243726761721476925977179091340)

r, s = ecdsa.create(message)
# 3896243893660249727180523716996124911121694637270467027687 4776385274595455509621853448773273410465218979854252522627

verify = ecdsa.verify(message, r, s, public_key)

assert verify == True
```
