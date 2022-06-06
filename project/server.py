# Run command: python server.py -port -address

from socket import socket, AF_INET, SOCK_STREAM
import sys
import logging

from common.variables import DEFAULT_IP, DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, USERNAME,\
    RESPONSE, ERROR
from common.utils import get_message, send_message
import logs.server_log_config
from decos import log

SERVER_LOGGER = logging.getLogger('app.server')


@log
def processing_client_msg(msg):
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg and msg[USER][USERNAME] == 'Anonymous':
        SERVER_LOGGER.info('Успешный запрос от клиента к серверу, статус код 200')
        return {RESPONSE: 200}
    SERVER_LOGGER.info('Неверный запрос от клиента к серверу, статус код 400')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error('После параметра -p должен быть указан номер порта.')
    except ValueError:
        SERVER_LOGGER.error('Значение номера порта должно быть в диапазоне от 1024 до 65535')

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP

    except IndexError:
        SERVER_LOGGER.error('После параметра -a должен быть указан IP-адрес')

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((listen_address, listen_port))
    
    server_sock.listen(MAX_CONNECTIONS)
    
    while True:
        client_sock, client_address = server_sock.accept()
        try:
            message_from_client = get_message(client_sock)
            SERVER_LOGGER.info(f'Сообщение от клиента: {message_from_client}')
            response = processing_client_msg(message_from_client)
            send_message(client_sock, response)
            client_sock.close()
        except ValueError:
            SERVER_LOGGER.error('Принято некорретное сообщение от клиента.')
            client_sock.close()


if __name__ == '__main__':
    main()
