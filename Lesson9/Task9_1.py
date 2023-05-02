# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
# доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
# узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
# перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
# («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
# помощью функции ip_address().

from ipaddress import ip_address
from subprocess import call


def host_ping(hosts):
    result = {}
    reach_ip = []
    unreach_ip = []
    for host in hosts:
        try:
            ip = ip_address(host)
        except ValueError:
            ip = host

        ret = call(f'ping {ip} -c 1', shell=True)
        if ret == 0:
            reach_ip.append(ip)
        else:
            unreach_ip.append(ip)
    result['Доступные адреса'] = reach_ip
    result['Недоступные адреса'] = unreach_ip
    return result


if __name__ == '__main__':
    HOSTS = ['gb.ru', '216.58.210.174', '5.255.255.70', '5.5.5.5']
    res = host_ping(HOSTS)
    for key, value in res.items():
        print(f'{key} - {value}')
