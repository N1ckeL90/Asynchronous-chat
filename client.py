import logging
from socket import *
import time
import json
import sys
import re
from threading import Thread
import log.client_log_config

# from decorators import log

logger = logging.getLogger('client')


# @log
def send_presence_msg(sock, account_name):
    """ Отправка presence сообщения """
    presence = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "Yep, I am here!"
        }
    }
    presence = json.dumps(presence)
    sock.send(presence.encode('utf-8'))


# @log
def create_msg(text, account_name, to):
    """ Создание сообщения для отправки """
    msg = {
        "action": "msg",
        "time": time.time(),
        "to": to,
        "from": account_name,
        "message": text
    }
    msg = json.dumps(msg)
    return msg


# @log
def process_response_from_server(sock, account_name='Guest'):
    """ Обработка сообщения от сервера """
    while True:
        try:
            msg = json.loads(sock.recv(1024).decode('utf-8'))
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
                    send_presence_msg(sock, account_name)
        except json.JSONDecodeError as er:
            logger.error(er)
            sys.exit(1)


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


def mainloop():
    with socket(AF_INET, SOCK_STREAM) as sock:
        connect_param = parsing_sys_argv()
        sock.connect((connect_param[0], connect_param[1]))

        # Отправка presence сообщения
        send_presence_msg(sock, connect_param[2])

        # while True:
            # режим работы клиента
            # mode = input('Используйте\n'
            #              '"1" для отправки сообщения в общий чат\n'
            #              '"2" для отправки сообщения пользователю\n'
            #              '"!exit" для выхода\n')
            # if mode == '!exit':
            #     sys.exit(0)
            # elif mode == '1':
            #     message_to = '#room_name'
            #     print('Приятного общения!\n')
            #     break
            # elif mode == '2':
            #     message_to = input('Введите пользователя, которому хотите отправить сообщение: ')
            #     print('Приятного общения!\n')
            #     break
            # else:
            #     print(f'Команды "{mode}" не существует')

        # Создание дополнительного потока для получения сообщений
        t = Thread(target=process_response_from_server, args=(sock, connect_param[2]))
        t.daemon = True
        t.start()

        # Отправка сообщений
        message_to = '#room_name'
        while True:
            text = input('')
            if text == '!exit':
                break
            try:
                msg = create_msg(text,  connect_param[2], message_to)
                sock.send(msg.encode('utf-8'))
            except Exception as er:
                logger.error(er)
                sys.exit(1)
            logger.debug('Сообщение отправлено')


if __name__ == '__main__':
    mainloop()
