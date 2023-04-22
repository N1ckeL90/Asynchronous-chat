# 1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к
# декорируемой функции. Он сохраняет ее имя и аргументы.
# 2. В декораторе @log реализовать фиксацию функции, из которой была вызвана
# декорированная. Если имеется такой код:
# @log
# def func_z():
# pass
# def main():
# func_z()
# ...в логе должна быть отражена информация:
# "<дата-время> Функция func_z() вызвана из функции main"

import inspect
import os
import sys
import logging
import inspect


if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):
    def call(*args, **kwargs):
        func(*args, **kwargs)
        logger.debug(f'Вызвана функция {func.__name__}{args}, {kwargs} из функции {inspect.stack()[1][3]}')
        return func(*args, **kwargs)
    return call
