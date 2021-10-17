# https://en.wikipedia.org/wiki/Elliptic-curve_Diffie-Hellman
import os
from ecc import ECC


ecc = ECC()

rute_private_key = int.from_bytes(os.urandom(32), byteorder='little')

rute_public_key = ecc.trapdoor(ecc.G, rute_private_key)

print('-'*50)
print('Chave privada de Rute:', rute_private_key)

print('-'*50)
print('Chave pública de Rute:', rute_public_key)

sibele_private_key = int.from_bytes(os.urandom(32), byteorder='little')

sibele_public_key = ecc.trapdoor(ecc.G, sibele_private_key)

print('-'*50)
print('Chave privada de Sibele:', sibele_private_key)

print('-'*50)
print('Chave pública de Sibele:', sibele_public_key)

rute_shared_key = ecc.trapdoor(sibele_public_key, rute_private_key)

print('-'*50)
print('Chave compartilhada de Rute:', rute_shared_key)

sibele_shared_key = ecc.trapdoor(rute_public_key, sibele_private_key)

print('-'*50)
print('Chave compartilhada de Sibele:', sibele_shared_key)


print('-'*50)
print('As chaves compartilhadas de Sibele e Rute são as mesmas?:', sibele_shared_key == rute_shared_key)
print('-'*50)
