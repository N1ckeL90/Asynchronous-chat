# Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на
# запись в него. Уместно использовать модуль subprocess

# РАБОАЕТ ТОЛЬКО НА WINDOWS!
import subprocess
# Так как мое клиентское приложение работает на чтение чата и запись в него, я реализую запуск сервера и клиента

import subprocess
from time import sleep


# сначала запускаем сервер
serv = subprocess.Popen('python ../server.py')
sleep(1)
# Затем запускаем клиента
cli = subprocess.Popen('python ../client.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
