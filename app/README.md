# Chat with Elliptic Curve Encryption
## Features
- SERVER
- CONNECT

### SERVER
> Module responsible for managing channel connections, making it possible for multiple users to be connected simultaneously

#### Usage

```shell
python server.py
```

### CONNECT
> Encrypts and decrypts messages, thus enabling conversation.
#### Usage
> Consider these two users
```python
from ecc.ecmo import ECMO

rute = ECMO(private_key=3)

sibele = ECMO(private_key=7)
```
> To connect to a channel, its private key is used as the first argument, and the public key of the person to connect as the second argument.

```shell
python connect.py from_private_key to_public_key
```

> Rute connect to Sibele
```shell
python connect.py 3 1164270129742194787021746298790404262615845385569632340556150609652209653392714737798593072499915146233094284387298092872206604386185768403662460504302349524,820238749192739888211492096736837212740835839662383100764162083366076000951085168184227504476659003461738201421631812073852429309662558977232294321188054299
```

> Sibele connect to Rute
```shell
python connect.py 7 5674708455687314755177411224894914551247560982429925442328503936381769479291831722549724502783064471579811889182869230569934709210549404604394803481732951421,4271801692429350493774172787940824381696861087943454989753620357811953134117882851809933515614164977926164094992857584446095333607804956469237639174332793061
```
> Once the connection is established, and the interested parties are present, the dialogue can be initiated, enjoying a very high end-to-end encryption mechanism.
