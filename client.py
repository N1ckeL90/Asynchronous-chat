import logging
from socket import *
import time
import json
import sys
import re
import log.client_log_config


logger = logging.getLogger('client')


def create_presence_msg(account_name='Guest'):
    logger.debug('Создание presence сообщения')
    presence = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "Yep, I am here!"
        }
    }
    return presence


def process_response_from_server(msg):
    logger.debug('Обработка ответа от сервера')
    if msg['response'] == 200:
        return '200: Ok'
    else:
        return f'400: {msg["error"]}'


def main():
    server_addr = ''
    server_port = 7777
    try:
        server_addr = str(sys.argv[1])
        if len(sys.argv) == 3:
            server_port = int(re.findall(r'\d+', sys.argv[2])[0])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        logger.error('Укажите IP-адрес и номер порта в формате "ip [port]"')
    except ValueError:
        logger.error('Порт должен быть в пределах от 1024 до 65535')
        sys.exit(1)

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_addr, server_port))
    out_msg = json.dumps(create_presence_msg())
    s.send(out_msg.encode('utf-8'))
    in_msg = s.recv(1024)
    response = process_response_from_server(json.loads(in_msg.decode('utf-8')))
    print(response)
    s.close()


if __name__ == '__main__':
    main()
