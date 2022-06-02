import json
import sys
sys.path.append('../')
from common.utils import get_message, send_message
from common.variables import TIME, ACTION, PRESENCE, USER, USERNAME, RESPONSE, ERROR, ENCODING, MAX_PACKAGE_SIZE
import unittest
from errors import NonDictInputError


class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    def send(self, message_to_send):
        json_test_message = json.dumps(self.testdict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len=MAX_PACKAGE_SIZE):
        json_test_message = json.dumps(self.testdict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 1,
        USER: {
            USERNAME: 'Mihail'
        }
    }

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        self.assertRaises(NonDictInputError, send_message, test_socket, 7777)

    def test_get_message(self):
        test_sock_ok = TestSocket({RESPONSE: 200})
        test_sock_err = TestSocket({RESPONSE: 400, ERROR: 'Bad Request'})
        self.assertEqual(get_message(test_sock_ok), {RESPONSE: 200})
        self.assertEqual(get_message(test_sock_err), {RESPONSE: 400, ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
