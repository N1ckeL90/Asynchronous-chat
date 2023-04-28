import sys
from socket import *
import json
import logging
import log.server_log_config
from decorators import log
import select


logger = logging.getLogger("server")


# @log
def create_presence_response(code_num, text_info):
    response = {}
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
    


def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов"""
    msg = []
    
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode("utf-8")
            data = json.loads(data)
            # сразу отправляем presence-сообщение, если есть
            if 'action' in data:
                if data['action'] == 'presence':
                    resp = create_presence_response(200, 'Ok')
                    sock.send(resp)
                else:
                    # иначе сохраняем для отправки другим клиентам
                    msg = [data, sock]
               
        except:
            # pass
            print(f"Клиент {sock} отключился")
            all_clients.remove(sock)
    return msg


def send_messages(msg, w_clients, all_clients):
    """Ответ сервера клиентам"""

    for sock in w_clients:
        try:
            if sock != msg[1]:
                sock.send(json.dumps(msg[0]).encode('utf-8'))
        except:
            print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
            sock.close()
            all_clients.remove(sock)
    return


def mainloop():
    """Основной цикл обработки клиентов"""
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
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except ValueError:
        logger.error('Введите корректный порт (от 1024 до 65535')
    except IndexError:
        logger.error('Введите номер порта после параметра "-p"')
        
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((server_address, server_port))
    s.listen(5)
    s.settimeout(0.2)


    while True:
        try:
            conn, addr = s.accept()
        except OSError as err:
            pass
        else:
            print(f"Получен запрос на соединение {addr}")
            clients.append(conn)
        finally:
            wait = 2
            r = []
            w = []
            
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                send_messages(requests, w, clients)


if __name__ == "__main__":
    print("сервер запущен")
    mainloop()
