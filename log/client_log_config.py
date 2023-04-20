import logging


# Создаем объект-логгер
logger = logging.getLogger('client')
# Создаем объект форматирования
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
# Создаем файловый обработчик логирования
fh = logging.FileHandler('client.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
# Добавляем обработчик событий и устанавливаем уровень событий
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
