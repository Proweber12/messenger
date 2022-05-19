"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import re


def get_data():
    pattern_prod = re.compile(r'^Изготовитель системы: +')
    pattern_name_os = re.compile(r'^Название ОС: +')
    pattern_code = re.compile(r'^Код продукта: +')
    pattern_type_system = re.compile(r'^Тип системы: +')

    main_data = ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    backslash_n = '\n'

    for num in range(1, 4):
        with open(f'info_{num}.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if re.search(r"^Изготовитель системы:", line):
                    os_prod_list.append(f'{pattern_prod.split(line)[1].replace(f"{backslash_n}", "")}')
                if re.search(r"^Название ОС:", line):
                    os_name_list.append(f'{pattern_name_os.split(line)[1].split(" ")[1]} {pattern_name_os.split(line)[1].split(" ")[2]}')
                if re.search(r"^Код продукта:", line):
                    os_code_list.append(f'{pattern_code.split(line)[1].replace(f"{backslash_n}", "")}')
                if re.search(r"^Тип системы:", line):
                    os_type_list.append(f'{pattern_type_system.split(line)[1].split(" ")[0]}')

    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list


def write_to_csv(filename_csv):
    data = get_data()
    with open(filename_csv, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data[0])
        for el in range(len(data[0]) - 1):
            specs = []
            specs.append(el+1)
            for data_list in range(1, len(data)):
                specs.append(data[data_list][el])
#            f.write('\n')
            writer.writerow(specs)


write_to_csv('data_report.csv')
