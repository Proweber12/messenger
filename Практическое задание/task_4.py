"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).
"""

words = ('разработка', 'администрирование', 'protocol', 'standard')

for word in words:
    byte_word = word.encode('utf-8')
    string_word = byte_word.decode('utf-8')
    print(f'Байтовое слово: {byte_word}, строковое слово: {string_word}')
