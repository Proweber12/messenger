"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import subprocess
import chardet

args_yandex, args_youtube = ('ping', '-c4', 'yandex.ru'), ('ping', '-c4', 'youtube.com')
subproc_ping_yandex, subproc_ping_youtube = subprocess.Popen(args_yandex, stdout=subprocess.PIPE),\
                                            subprocess.Popen(args_youtube, stdout=subprocess.PIPE)

ping_sites = (subproc_ping_youtube, subproc_ping_yandex)
i = 0

while i < len(ping_sites):
    for line in ping_sites[i].stdout:
        line_encoding = chardet.detect(line)
        line_coding_utf_8 = line.decode(line_encoding['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
    i += 1
