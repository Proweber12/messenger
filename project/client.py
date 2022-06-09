# Run command: python client.py -address -port -mode
import json
import socket
import sys
import time
import logging

from common.variables import DEFAULT_IP, DEFAULT_PORT, DEFAULT_MODE, ACTION, PRESENCE, TIME, USER, USERNAME, RESPONSE, ERROR, MSG, SENDER, MSG_TEXT
from common.utils import send_message, get_message
import logs.client_log_config
from decos import log

CLIENT_LOGGER = logging.getLogger('app.client')


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MSG and SENDER in message and MSG_TEXT in message:
        print(f'Полученно сообщение от пользователя {message[SENDER]}: {message[MSG_TEXT]}')
        CLIENT_LOGGER.info(f'Полученно сообщение от пользователя {message[SENDER]}: {message[MSG_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Полученно неверное сообщение сервера: {message}')


@log
def create_client_message(sock, username='Anonymous'):
    message_text = input("Введите сообщение для отправки или 'exit' для завершения: ")
    if message_text == 'exit':
        sock.close()
        CLIENT_LOGGER.info(f'Пользователь с ником {username} вышел из чата')
        print('Сеанс завершён')
        sys.exit(0)
    message = {
        ACTION: MSG,
        TIME: time.time(),
        USERNAME: username,
        MSG_TEXT: message_text
    }
    CLIENT_LOGGER.info(f'Сформированно сообщение от пользователя {username}: {message}')
    return message


@log
def generate_presence(username='Anonymous'):
    presence_msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {USERNAME: username}
    }
    CLIENT_LOGGER.info(f'Сформированно {PRESENCE} сообщение пользователем с ником - {username}')
    return presence_msg


@log
def parse_server_message(msg):
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            CLIENT_LOGGER.info(f'Сервер дал ответ с кодом {msg[RESPONSE]}')
            return 'Status code 200: OK'
        CLIENT_LOGGER.info(f'Сервер дал ответ с кодом {msg[RESPONSE]}, ошибка {msg[ERROR]}')
        return f'Status code 400: {msg[ERROR]}'
    CLIENT_LOGGER.error('Возникла ошибка переданного значения')
    raise ValueError


def main():
    try:
        ip_address = sys.argv[1]
        port = int(sys.argv[2])
        mode = sys.argv[3]
        if port < 1024 or port > 65535:
            raise ValueError
        if ip_address == "-":
            ip_address = DEFAULT_IP
        if mode not in ('listen', 'send'):
            CLIENT_LOGGER.critical('Введен не правильный режим работы. Переводим в стандартный режим на чтение.')
            print('Введен не правильный режим работы. Допустимые режимы работы: listen и send. Переводим в стандартный режим на чтение.')
            mode = DEFAULT_MODE
    except IndexError:
        ip_address = DEFAULT_IP
        port = DEFAULT_PORT
        mode = DEFAULT_MODE
    except ValueError:
        CLIENT_LOGGER.error('Значение номера порта должно быть в диапазоне от 1024 до 65535')

    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((ip_address, port))
        CLIENT_LOGGER.info(f'Клиент подключился к серверу по {ip_address} адресу, по {port} порту, в {mode} режиме')
        presence_message = generate_presence()
        send_message(client_sock, presence_message)
        answer_to_server = parse_server_message(get_message(client_sock))
        CLIENT_LOGGER.info(f'Ответ сервера: {answer_to_server}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {ip_address}:{port}')
        sys.exit(1)
    else:
        if mode == 'send':
            print('Включен режим отправки сообщений')
        else:
            print('Включен режим приёма сообщений')

        while True:
            if mode == 'send':
                try:
                    send_message(client_sock, create_client_message(client_sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {ip_address} было потеряно.')
                    sys.exit(1)

            if mode == 'listen':
                try:
                    message_from_server(get_message(client_sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {ip_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
