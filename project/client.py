# Run command: python server.py -address -port

from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
import logging

from common.variables import DEFAULT_IP, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, USERNAME, RESPONSE, ERROR
from common.utils import send_message, get_message
import logs.client_log_config
from decos import log

CLIENT_LOGGER = logging.getLogger('app.client')


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
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        ip_address = DEFAULT_IP
        port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.error('Значение номера порта должно быть в диапазоне от 1024 до 65535')

    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((ip_address, port))
    presence_message = generate_presence()
    send_message(client_sock, presence_message)
    try:
        answer_to_server = parse_server_message(get_message(client_sock))
        CLIENT_LOGGER.info(f'Ответ сервера: {answer_to_server}')
    except ValueError:
        CLIENT_LOGGER.error('Ошибка декодирования сообщение')


if __name__ == '__main__':
    main()
