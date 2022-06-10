# Run command: python server.py -p -port -a -address
import select
import socket
import sys
import logging
import time

from common.variables import DEFAULT_IP, DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, MSG, TIME, USER, USERNAME,\
    RESPONSE, ERROR, MSG_TEXT, SENDER
from common.utils import get_message, send_message
import logs.server_log_config
from decos import log

SERVER_LOGGER = logging.getLogger('app.server')


@log
def processing_client_msg(msg, msg_list, client):
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg and msg[USER][USERNAME] == 'Anonymous':
        SERVER_LOGGER.info('Успешный запрос от клиента к серверу, статус код 200')
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in msg and msg[ACTION] == MSG and TIME in msg and MSG_TEXT in msg:
        SERVER_LOGGER.info(f'Пришло сообщение от {msg[USERNAME]}: {msg[MSG_TEXT]}')
        msg_list.append((msg[USERNAME], msg[MSG_TEXT]))
        return
    else:
        SERVER_LOGGER.info('Неверный запрос от клиента к серверу, статус код 400')
        send_message(client, {RESPONSE: 400, ERROR: 'Bad Request'})
        return


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

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((listen_address, listen_port))
    server_sock.settimeout(0.5)

    clients = []
    messages = []

    server_sock.listen(MAX_CONNECTIONS)

    while True:
        try:
            client_sock, client_address = server_sock.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f"Подключен новый клиент {client_address}")
            clients.append(client_sock)

        read_data_list = []
        send_data_list = []
        error_data_list = []
        wait = 0

        try:
            if clients:
                read_data_list, send_data_list, error_data_list = select.select(clients, clients, [], wait)
        except OSError:
            pass

        if read_data_list:
            for client_with_message in read_data_list:
                try:
                    processing_client_msg(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                ACTION: MSG,
                SENDER: messages[0][0],
                TIME: time.time(),
                MSG_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
