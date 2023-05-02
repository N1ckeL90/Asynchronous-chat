# Реализовать скрипт, запускающий указанное количество клиентских приложений

# РАБОАЕТ ТОЛЬКО НА WINDOWS!

import subprocess


PROCESS = []
num_proc = int(input("Введите количество запускаемых скриптов: "))
for i in range(num_proc):
    PROCESS.append(subprocess.Popen(f'python ../client.py localhost [7777] test{i}',
                                    creationflags=subprocess.CREATE_NEW_CONSOLE))
