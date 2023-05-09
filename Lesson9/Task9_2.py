# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса. По результатам проверки должно
# выводиться соответствующее сообщение

from ipaddress import ip_address
import re
from Task9_1 import host_ping


def ip_check(ip):
    try:
        ip_address(ip)
    except ValueError:
        return False
    else:
        return True


def host_range_ping():
    while True:
        start_host_ip = input('Введите начальный IP-адрес: ')
        if ip_check(start_host_ip) is False:
            print('Неправильно введен ip-адрес.')
        else:
            last_oct = int(start_host_ip.split('.')[3])
            while True:
                range_of_addr = input('Введите диапазон проверяемых ip-адресов: ')
                if not range_of_addr.isnumeric() or not (1 <= int(range_of_addr) <= 255 - last_oct):
                    print(f'Число должно быть в диапазоне от 1 до {255 - last_oct}')
                else:
                    break
            break

    pattern = re.compile(r'\d+\.\d+\.\d+\.')
    start_ip = pattern.findall(start_host_ip)[0]
    list_of_ip_addr = []
    for i in range(last_oct, (last_oct + int(range_of_addr))):
        list_of_ip_addr.append(start_ip + str(i))
    result = host_ping(list_of_ip_addr)
    return result


if __name__ == '__main__':
    res = host_range_ping()
    for key, value in res.items():
        print(f'{key} - {value}')
