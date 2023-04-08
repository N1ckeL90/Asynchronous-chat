# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
# сохранение данных в файле YAML-формата. Для этого:

#     a. Подготовить данные для записи в виде словаря, в котором первому ключу
#     соответствует список, второму — целое число, третьему — вложенный словарь, где
#     значение каждого ключа — это целое число с юникод-символом, отсутствующим в
#     кодировке ASCII (например, €);

#     b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
#     При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
#     также установить возможность работы с юникодом: allow_unicode = True;

#     c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
#     с исходными.

import yaml

DATA = {'cars': ['KIA Sonet 1.5', 'Ford EcoSport 1.5', 'Changan CS35'],
        'cars_count': 3,
        'cars_prices': {'KIA Sonet 1.5': '99960¥', 'Ford EcoSport 1.5': '97800¥', 'Changan CS35': '97980¥'}
        }

with open('file.yaml', 'w', encoding='Utf-8') as f:
    yaml.dump(DATA, f, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f:
    read_data = yaml.load(f, Loader=yaml.SafeLoader)

print(DATA == read_data)
