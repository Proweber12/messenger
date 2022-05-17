"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).
"""

words = ('attribute', 'класс', 'функция', 'type')

for word in words:
    try:
        print(eval(f'b"{word}"'))
    except SyntaxError:
        print(f"Строку '{word}' нельзя преобразовать в байт-код с помощью b''")
