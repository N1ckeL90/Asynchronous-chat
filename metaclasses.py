import dis


class ClientVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        is_tcp_method = False
        for item in clsdict:
            try:
                ret = dis.get_instructions(clsdict[item])
            except TypeError:
                pass
            else:
                for el in ret:
                    if el.opname == 'LOAD_GLOBAL' or el.opname == 'LOAD_METHOD':
                        if el.argval == "accept" or el.argval == "listen" or el.argval == "socket":
                            raise TypeError(f'Использование метода {el.argval} в классе запрещено')
                        if el.argval == "send" or el.argval == "recv":
                            is_tcp_method = True
        if not is_tcp_method:
            raise TypeError('Отсутствие вызовов функций, работающих с сокетами по TCP')

        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        is_tcp_method = False
        for item in clsdict:
            try:
                ret = dis.get_instructions(clsdict[item])
            except TypeError:
                pass
            else:
                for el in ret:
                    if el.opname == 'LOAD_GLOBAL' or el.opname == 'LOAD_METHOD':
                        if el.argval == "connect":
                            raise TypeError('Использование метода "connect" в классе запрещено')
                        if el.argval == "send" or el.argval == "recv":
                            is_tcp_method = True

        if not is_tcp_method:
            raise TypeError('Отсутствие вызовов функций, работающих с сокетами по TCP')

        super().__init__(clsname, bases, clsdict)
