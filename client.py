import logging
from socket import *
import time
import json
import sys
import re
import log.client_log_config
from decorators import log


logger = logging.getLogger('client')


# @log
def send_presence_msg(sock, account_name='Guest'):
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
def create_msg(text, account_name='Guest'):
    """ Создание сообщения для отправки """
    msg = {
        "action": "msg",
        "time": time.time(),
        "to": "#room name",
        "from": account_name,
        "message": text
        }
    msg = json.dumps(msg)
    return msg    
                

# @log
def process_response_from_server(sock, msg):
    """ Обработка сообщения от сервера """
    try:
        msg = json.loads(msg)
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
                send_presence_msg(sock)   
    except json.JSONDecodeError as er:
        logger.error(er)
        sys.exit(1)       


def mainloop():
    server_addr = 'localhost'
    server_port = 7777
    mode = '-r' # режим работы клиента: -r - только на чтение, -s - только на запись
    try:
        server_addr = str(sys.argv[1])
        if sys.argv[2]:
            server_port = int(re.findall(r'\d+', sys.argv[2])[0])
        else:
            raise IndexError
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        if '-s' in sys.argv:
            mode = '-s'
    except IndexError:
        logger.error('Укажите IP-адрес, номер порта и режим работы клиента в формате "ip [port] -s"')
    except ValueError:
        logger.error('Порт должен быть в пределах от 1024 до 65535')
        sys.exit(1)   

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((server_addr, server_port))
        
        # Отправка presence сообщения
        send_presence_msg(sock) 
        
        # Режим отправки сообщений в чат
        if mode == '-s':
            while True:
                text = input('Ваше сообщение: ')
                if text == 'exit':
                    break
                try:
                    msg = create_msg(text)
                    sock.send(msg.encode('utf-8'))
                except Exception as er:
                    logger.error(er)
                    sys.exit(1)
                logger.debug('Сообщение отправлено')
                
        # Режим приема сообщений из чата        
        elif mode == '-r':
            while True:
                data = sock.recv(1024).decode('utf-8')
                process_response_from_server(sock, data)
                

if __name__ == '__main__':
    mainloop()
