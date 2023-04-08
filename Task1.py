# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
# определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
# «отчетный» файл в формате CSV. Для этого:

#     a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
#     данными, их открытие и считывание данных. В этой функции из считанных данных
#     необходимо с помощью регулярных выражений извлечь значения параметров
#     «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
#     каждого параметра поместить в соответствующий список. Должно получиться четыре
#     списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
#     функции создать главный список для хранения данных отчета — например, main_data
#     — и поместить в него названия столбцов отчета в виде списка: «Изготовитель
#     системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
#     столбцов также оформить в виде списка и поместить в файл main_data (также для
#     каждого файла);

#     b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
#     функции реализовать получение данных через вызов функции get_data(), а также
#     сохранение подготовленных данных в соответствующий CSV-файл;
#     c. Проверить работу программы через вызов функции write_to_csv().

import re
import csv


def get_data():
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(1, 4):
        with open(f'info_{i}.txt', encoding='cp1251') as f:
            data = f.read()
            os_prod_list.append(re.findall(r'Изготовитель системы:\s*(.+?)\n', data)[0])
            os_name_list.append(re.findall(r'Название ОС:\s*(.+?)\n', data)[0])
            os_code_list.append(re.findall(r'Код продукта:\s*(.+?)\n', data)[0])
            os_type_list.append(re.findall(r'Тип системы:\s*(.+?)\n', data)[0])

    row = 1
    for i in range(0, 3):
        row_data = [row, os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]]
        main_data.append(row_data)
        row += 1

    return main_data


def write_to_csv(file):
    data = get_data()
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('report.csv')
