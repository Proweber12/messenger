DEFAULT_IP = '127.0.0.2'
DEFAULT_PORT = 7778
DEFAULT_MODE = 'listen'
MAX_CONNECTIONS = 10
MAX_PACKAGE_SIZE = 1024

ACTION = 'action'
PRESENCE = 'presence'
PROBE = 'prоbe'
MSG = 'msg'
QUIT = 'quit'
AUTHENTICATE = 'authenticate'
JOIN = 'join'
LEAVE = 'leave'
EXIT = 'exit'
DESTINATION = 'to'
SENDER = 'from'

TIME = 'time'
USER = 'user'
USERNAME = 'username'
RESPONSE = 'response'
ERROR = 'error'
MSG_TEXT = 'msg_text'

ENCODING = 'utf-8'

RESPONSE_200 = {RESPONSE: 200}

RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
