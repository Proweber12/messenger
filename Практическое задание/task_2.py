"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.
"""

words = ('class', 'function', 'method')

for word in words:
    byte_word = eval(f'b"{word}"')
    print(f'Тип: {type(byte_word)}\n'
          f'Содержимое: {byte_word}\n'
          f'Длина: {len(byte_word)}\n'
          f'{"-" * 60}')
