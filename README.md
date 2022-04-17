# Elliptic Curve Tools
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/isakruas/ectools.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/isakruas/ectools/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/isakruas/ectools.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/isakruas/ectools/alerts/)
[![Latest Version](https://img.shields.io/pypi/v/ectools.svg?style=flat)](https://pypi.python.org/pypi/ectools/)
## Features
- EC
- ECDH
- ECK
- ECDSA
- ECMO

### EC
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
from ectools import EC

# Specify the curve to be used, if you omit the secp224k1 standard curve will be chosen
ec = EC(curve='secp192k1')

gcd = ec.gcd(ec.a, ec.b)

assert gcd == 3

gcd, x, y = ec.egcd(ec.a, ec.p)

assert ec.a*x + ec.b*y == ec.gcd(ec.a, ec.b)

mmi = ec.mmi(ec.b, ec.p)

assert mmi == 4184734490257787175890526282138444277401570296306493027365

P = ec.G

Q = ec.G

# P + Q
dot = ec.dot(P, Q)

assert dot == (
                5898748710631235793867485368048681928976741514058866965686,
                6215318586565457819081644608453878670902049430638930374357
              )

k = 2

# k * G, G = (x, y) in Fp
trapdoor = ec.trapdoor(ec.G, k)

assert trapdoor == dot
```

### ECDH
> Protocol implementation

| Methods | README |
| ------ | ------ |
| to_share | https://en.wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman |


```python
from ectools import ECDH

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
from ectools import ECK

eck = ECK(curve='secp521r1')

# Message (up to 64 bytes) to be encoded
message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit integer.'

encode = eck.encode(message)

decode  = eck.decode(encode)

assert message == decode

# Message (up to 32 bytes) to be encoded
message = message[0:32]

encode = eck.encode(message, encode=32)

decode  = eck.decode(encode, encode=32)

assert message == decode
```

### ECDSA
> Protocol implementation

| Methods | README |
| ------ | ------ |
| create | https://pt.wikipedia.org/wiki/ECDSA |
| verify | https://pt.wikipedia.org/wiki/ECDSA |

```python
from ectools import ECDSA

message = 123457

private_key = 7

ecdsa = ECDSA(curve='secp192k1', private_key=private_key)

public_key = ecdsa.public_key
# (5370475959698699548314844898721723603195636604449975017091, 4063159672567797276483870227243726761721476925977179091340)

r, s = ecdsa.signature(message)
# 3896243893660249727180523716996124911121694637270467027687 4776385274595455509621853448773273410465218979854252522627

verify = ecdsa.verify_signature(message, r, s, public_key)

assert verify is True
```

### ECMO
> Protocol implementation

| Methods | README |
| ------ | ------ |
| encrypt | |
| decrypt | |

```python
from ectools import ECMO

rute = ECMO(private_key=3)

sibele = ECMO(private_key=7)

# Message (up to 64 bytes) to be encoded
message = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit integer.'

rute_encrypt_message = rute.encrypt(message, to=sibele.public_key)
# (((1857240550913749511311933146838018859984049385437909475627815302394196392116794951261872948498796224129013364419509543345205163345179842089331125585436362058,3506705573297651839782379747688631207619938669499243895588664759776552259047523714413709830928492585032896255416492668464023541566300767978601214470798534284),0),(832900723057219226235832309951309634564790965766619142337135688003093158580593783030642442689816243439307777897892309485599092775426838123977430011908592689,2725867211280709369559739856531799838050999097103997378962089699490760618311262626053354235740994426084376348161197462998112431752885856911722361899927310419))

sibele_decrypt_message = sibele.decrypt(rute_encrypt_message, got=rute.public_key)
# 'Lorem ipsum dolor sit amet, consectetur adipiscing elit integer.'

assert message == sibele_decrypt_message

# Message (up to 32 bytes) to be encoded
message = message[0:32]

rute_encrypt_message = rute.encrypt(message, to=sibele.public_key, encode=32)
# (((5514905102432971215032059168811599118609678263301496051616006183391286555697379035644243244429999155050824946116976394271676504022270025209979760865557105792, 3616882871789765664390196373675698268226539885126786831225333519076362402850831381514218685912486878712017969901932410182658098975714449511865640394996534438), 0), (704698789382865060147247327627501049009276566478897869842535881827504579525028882135386414981317402850240733513907097487477960975455036937131797327078159252, 695017146506462800084983558343280494117631989946851182810895058155576557979783716414590026260278050690043546398655256933740435522352516282285460869540420509))

sibele_decrypt_message = sibele.decrypt(rute_encrypt_message, got=rute.public_key, encode=32)
# 'Lorem ipsum dolor sit amet, cons'

assert message == sibele_decrypt_message
```
