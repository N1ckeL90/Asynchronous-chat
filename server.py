import sys
from socket import *
import time
import json


def create_response(info):
    if 199 < info[0] < 300:
        response = {
            'response': info[0],
            'alert': info[1]
        }
    else:
        response = {
            'response': info[0],
            'error': info[1]
        }
    return response


def process_client_message(msg: dict):
    if 'action' in msg and msg['action'] == 'presence' and 'time' in msg \
            and 'user' in msg and msg['user']['account_name'] == 'Guest':
        return [200, 'OK']
    else:
        return [400, 'Bad Request']


def main():
    server_address = ''
    server_port = 7777

    try:
        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
    except IndexError:
        print('Введите IP-адрес после параметра "-a"')
        sys.exit(1)

    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        print('Введите корректный порт (от 1024 до 65535')
    except IndexError:
        print('Введите номер порта после параметра "-p"')

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((server_address, server_port))
    s.listen()

    try:
        while True:
            client, addr_client = s.accept()
            print(f'Получен запрос на соединение от {addr_client}')
            input_data = client.recv(1024).decode('utf-8')
            msg = json.loads(input_data)
            print(msg)
            checked_msg = process_client_message(msg)
            response = create_response(checked_msg)
            client.send(json.dumps(response).encode('utf-8'))
            client.close()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
