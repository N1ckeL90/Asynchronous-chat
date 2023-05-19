import logging
from socket import *
import time
import json
import sys
import re
from threading import Thread
import log.client_log_config
from metaclasses import ClientVerifier


logger = logging.getLogger('client')


def parsing_sys_argv():
    """ Парсинг параметров командной строки """

    server_addr = 'localhost'
    server_port = 7777
    account_name = 'Guest'
    try:
        if len(sys.argv) >= 2:
            server_addr = str(sys.argv[1])
        if len(sys.argv) >= 3:
            server_port = int(re.findall(r'\d+', sys.argv[2])[0])
            if 1024 < server_port < 65535:
                pass
            else:
                raise ValueError
        if len(sys.argv) == 4:
            account_name = sys.argv[3]
    except IndexError:
        logger.error('Укажите IP-адрес, номер порта и режим работы клиента в формате "ip [port] account_name"')
    except ValueError:
        logger.error('Порт должен быть в пределах от 1024 до 65535')
        sys.exit(1)
    return server_addr, server_port, account_name


class Client(metaclass=ClientVerifier):
    def __init__(self, sock, account_name):
        self.sock = sock
        self.account_name = account_name

    def send_presence_msg(self):
        """ Отправка presence сообщения """
        presence = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": self.account_name,
                "status": "Yep, I am here!"
            }
        }
        presence = json.dumps(presence)
        self.sock.send(presence.encode('utf-8'))

    # @log
    def send_msg(self, text, to):
        """ Отправка сообщения """
        msg = {
            "action": "msg",
            "time": time.time(),
            "to": to,
            "from": self.account_name,
            "message": text
        }
        msg = json.dumps(msg)
        self.sock.send(msg.encode('utf-8'))

    def process_response_from_server(self):
        """ Обработка сообщения от сервера """
        while True:
            try:
                msg = json.loads(self.sock.recv(1024).decode('utf-8'))
                if 'response' in msg:
                    if msg['response'] == 200:
                        logger.debug('200: OK')
                    else:
                        logger.error(msg)
                        sys.exit(1)
                elif 'action' in msg:
                    if msg['action'] == 'msg':
                        print('Пользователь ' + msg['from'] + ': ' + msg['message'])
                    elif msg['action'] == 'probe':
                        self.send_presence_msg()
            except json.JSONDecodeError as er:
                logger.error(er)
                sys.exit(1)


def mainloop():

    with socket(AF_INET, SOCK_STREAM) as sock:
        server_addr, server_port, account_name = parsing_sys_argv()
        sock.connect((server_addr, server_port))
        client = Client(sock, account_name)
        # Отправка presence сообщения
        client.send_presence_msg()

        while True:
            # режим работы клиента
            mode = input('Используйте\n'
                         '"1" для отправки сообщения в общий чат\n'
                         '"2" для отправки сообщения пользователю\n'
                         '"!exit" для выхода\n')
            if mode == '!exit':
                sys.exit(0)
            elif mode == '1':
                message_to = '#room_name'
                print('Приятного общения!\n')
                break
            elif mode == '2':
                message_to = input('Введите пользователя, которому хотите отправить сообщение: ')
                print('Приятного общения!\n')
                break
            else:
                print(f'Команды "{mode}" не существует')

        # Создание дополнительного потока для получения сообщений
        t = Thread(target=client.process_response_from_server)
        t.daemon = True
        t.start()

        # Отправка сообщений
        while True:
            text = input('')
            if text == '!exit':
                break
            try:
                client.send_msg(text, message_to)
            except Exception as er:
                logger.error(er)
                sys.exit(1)


if __name__ == '__main__':
    mainloop()
