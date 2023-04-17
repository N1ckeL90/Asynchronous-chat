import logging
import logging.handlers


# Создаем объект форматирования
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

# Встроенный обработчик
th = logging.handlers.TimedRotatingFileHandler(filename='server.log', when='midnight', encoding='utf-8', backupCount=7)
th.setLevel(logging.DEBUG)
th.setFormatter(formatter)

# Создаем объект-логгер
logger = logging.getLogger('server')
# Добавляем обработчик событий и устанавливаем уровень событий
logger.addHandler(th)
logger.setLevel(logging.DEBUG)
