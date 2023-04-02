import subprocess

# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
# проверить тип и содержание соответствующих переменных. Затем с помощью
# онлайн-конвертера преобразовать строковые представление в формат Unicode и также
# проверить тип и содержимое переменных.

print('\nЗадание #1')

word1 = 'разработка'
word2 = 'сокет'
word3 = 'декоратор'

print(word1, type(word1))
print(word2, type(word2))
print(word3, type(word3))

uni_word1 = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
uni_word2 = '\u0441\u043e\u043a\u0435\u0442'
uni_word3 = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

print(uni_word1, type(uni_word1))
print(uni_word2, type(uni_word2))
print(uni_word3, type(uni_word3))

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

print('\nЗадание #2')

bytes_word1 = b'class'
bytes_word2 = b'function'
bytes_word3 = b'method'

print(bytes_word1, type(bytes_word1), len(bytes_word1))
print(bytes_word2, type(bytes_word2), len(bytes_word2))
print(bytes_word3, type(bytes_word3), len(bytes_word3))

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.

print('\nЗадание #3')
print('«класс» и «функция» невозможно записать в байтовом типе, так как кириллица не относится к ASCII')

# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование (используя
# методы encode и decode).

print('\nЗадание #4')
enc_str1 = 'разработка'
enc_str2 = 'администрирование'
enc_str3 = 'protocol'
enc_str4 = 'standard'

enc_str_bytes1 = enc_str1.encode('utf-8')
enc_str_bytes2 = enc_str2.encode('utf-8')
enc_str_bytes3 = enc_str3.encode('utf-8')
enc_str_bytes4 = enc_str4.encode('utf-8')

print(enc_str_bytes1)
print(enc_str_bytes2)
print(enc_str_bytes3)
print(enc_str_bytes4)

dec_str1 = enc_str_bytes1.decode('utf-8')
dec_str2 = enc_str_bytes2.decode('utf-8')
dec_str3 = enc_str_bytes3.decode('utf-8')
dec_str4 = enc_str_bytes4.decode('utf-8')

print(dec_str1)
print(dec_str2)
print(dec_str3)
print(dec_str4)

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
# байтовового в строковый тип на кириллице.

print('\nЗадание #5')

command_yandex = 'ping -c 4 yandex.ru'
yandex_ping = subprocess.check_output(command_yandex, shell=True)
yandex_ping.decode('cp866').encode('utf-8')
print(yandex_ping.decode('utf-8'))

command_youtube = 'ping -c 4 youtube.ru'
youtube_ping = subprocess.check_output(command_youtube, shell=True)
youtube_ping.decode('cp866').encode('utf-8')
print(youtube_ping.decode('utf-8'))

# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
# программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

print('\nЗадание #6')

with open('test_file.txt', encoding='utf-8') as f:
    for row in f:
        print(row)
