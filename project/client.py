from socket import socket, AF_INET, SOCK_STREAM
import sys
import time

from common.variables import DEFAULT_IP, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, USERNAME, RESPONSE, ERROR
from common.utils import send_message, get_message


def generate_presence(username='Anonymous'):
    presence_msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {USERNAME: username}
    }

    return presence_msg


def parse_server_message(msg):
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return 'Status code 200: OK'
        return f'Status code 400: {msg[ERROR]}'
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
        print("Значение номера порта должно быть в диапазоне от 1024 до 65535")

    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.connect((ip_address, port))
    presence_message = generate_presence()
    send_message(client_sock, presence_message)
    try:
        answer_to_server = parse_server_message(get_message(client_sock))
        print(answer_to_server)
    except ValueError:
        print('Не получилось декодировать сообщение')

    


if __name__ == '__main__':
    main()
