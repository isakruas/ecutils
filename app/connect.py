import asyncio
import argparse
import json
import logging
import threading
import websockets
from ecc.ecmo import ECMO
from colorama import (
    init,
    Fore
)
init()

SERVER = 'ws://localhost:1998'

parser = argparse.ArgumentParser(
    prog='ECC-APP',
    description='Chat with Elliptic Curve Encryption',
    epilog='end-to-end encryption'
)

parser.add_argument(
    'from_private_key',
    metavar='from_private_key',
    type=int,
    help='your private key'
)

parser.add_argument(
    'to_public_key',
    metavar='to_public_key',
    type=tuple,
    help="your acquaintance's public key"
)

args = parser.parse_args()


__from = ECMO(private_key=args.from_private_key)

__to = tuple(int(i) for i in ''.join(args.to_public_key).split(','))

channel = ''.join([str(i) for i in __from.to_share(__to)])

CONNECTION = set()


async def server_conn():
    global CONNECTION
    async with websockets.connect(f'{SERVER}/ecc/{channel}/') as conn:
        CONNECTION.add(conn)
        while True:
            try:
                encrypt = await conn.recv()
                encrypt = json.loads(encrypt)
                try:
                    x = encrypt['m']['x']
                    y = encrypt['m']['y']
                    j = encrypt['m']['j']
                    r = encrypt['s']['r']
                    s = encrypt['s']['s']
                    encrypt = ((x, y), j), (r, s)
                    print(Fore.YELLOW, '\n', ' '*20, __from.decrypt(encrypt, got=__to))
                except Exception as err:
                    logging.info(err)
                    try:
                        status = encrypt['users']
                        print(Fore.GREEN, '\n', f'Existe {status} usuário(s) ativo(s) no canal.')
                    except Exception as err:
                        logging.info(err)
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as err:
                logging.info(err)
                CONNECTION.remove(conn)
                break


def __start_server_conn():
    asyncio.run(server_conn())


MESSAGES = list()


async def send_message():
    global MESSAGES, CONNECTION
    while True:
        try:
            if len(MESSAGES) != 0 and len(CONNECTION) != 0:
                encrypt_message = MESSAGES[0]
                MESSAGES = [i for i in MESSAGES if i != MESSAGES[0]]
                [await conn.send(encrypt_message) for conn in CONNECTION]
        except (EOFError, KeyboardInterrupt):
            break
        except Exception as err:
            logging.info(err)
        await asyncio.sleep(1)


def __start_send_message():
    asyncio.run(send_message())


threads = [
    threading.Thread(target=__start_server_conn),
    threading.Thread(target=__start_send_message)
]
[i.start() for i in threads]

while True:
    try:
        ((x, y), j), (r, s) = __from.encrypt(input('\n'), to=__to)
        message = {'m': {'x': x, 'y': y, 'j': j}, 's': {'r': r, 's': s}}
        MESSAGES.append(json.dumps(message))
    except (EOFError, KeyboardInterrupt):
        [i.join() for i in threads]
        break
    except Exception as err:
        logging.info(err)
