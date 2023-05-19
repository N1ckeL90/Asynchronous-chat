import sys
from socket import *
import json
import logging
import log.server_log_config
import select

from metaclasses import ServerVerifier
from descriptors import Port

logger = logging.getLogger("server")


def parsing_sys_argv():
    """ Парсинг параметров командной строки """

    server_address = ''
    server_port = 7777

    try:
        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
    except IndexError:
        logger.error('Введите IP-адрес после параметра "-a"')
        sys.exit(1)
    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
    except IndexError:
        logger.error('Введите номер порта после параметра "-p"')
    return server_address, server_port


class Server(metaclass=ServerVerifier):

    server_port = Port()

    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

        self.clients = {}

    def create_presence_response(self, code_num, text_info):
        try:
            if 199 < code_num < 300:
                response = {
                    'response': code_num,
                    'alert': text_info
                }
            else:
                response = {
                    'response': code_num,
                    'error': text_info,
                }
            response = json.dumps(response).encode('utf-8')
            return response
        except Exception as er:
            logger.error(er)

    def read_requests(self, r_clients):
        """Чтение запросов из списка клиентов"""
        msg = []

        for sock in r_clients:
            try:
                data = sock.recv(1024).decode("utf-8")
                data = json.loads(data)
                # Сразу отправляем ответ на presence-сообщение, если есть.
                # А также определяем имя клиента для этого подключения
                if 'action' in data:
                    if data['action'] == 'presence':
                        self.clients[sock] = data['user']['account_name']
                        print(f'Клиент {data["user"]["account_name"]} подключился')
                        resp = self.create_presence_response(200, 'Ok')
                        sock.send(resp)
                    else:
                        # иначе сохраняем для дальнейшей отправки другим клиенту(-ам)
                        msg = [data, sock]
            except:
                print(f"Клиент {self.clients[sock]} отключился")
                self.clients.pop(sock)
        return msg

    def send_messages(self, msg, w_clients):
        """Ответ сервера клиентам"""

        for sock in w_clients:
            try:
                if msg[0]['to'] == '#room_name':
                    if sock != msg[1]:
                        sock.send(json.dumps(msg[0]).encode('utf-8'))
                else:
                    if msg[0]['to'] == self.clients[sock]:
                        sock.send(json.dumps(msg[0]).encode('utf-8'))
            except:
                print(f"Клиент {self.clients[sock]} отключился")
                sock.close()
                self.clients.pop(sock)
        return

    def run_server(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.server_address, self.server_port))
        s.listen(5)
        s.settimeout(0.2)
        print('сервер запущен')

        while True:
            try:
                conn, addr = s.accept()
            except OSError as err:
                pass
            else:
                print(f"Получен запрос на соединение {addr}")
                self.clients[conn] = None
            finally:
                wait = 2
                r = []
                w = []

                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass

                requests = self.read_requests(r)
                if requests:
                    self.send_messages(requests, w)


def mainloop():
    """Основной цикл обработки клиентов"""
    server_address, server_port = parsing_sys_argv()
    server = Server(server_address, server_port)
    server.run_server()


if __name__ == "__main__":
    mainloop()
