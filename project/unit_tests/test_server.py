import sys
from unittest import TestCase, main

sys.path.append('../')
from server import processing_client_msg
from common.variables import TIME, ACTION, PRESENCE, USER, USERNAME, RESPONSE, ERROR, PROBE


class TestServer(TestCase):

    def test_processing_client_msg_default(self):
        client_msg = processing_client_msg({ACTION: PRESENCE, TIME: 1, USER: {USERNAME: 'Anonymous'}})
        self.assertEqual(client_msg, {RESPONSE: 200})

    def test_processing_client_msg_custom(self):
        username = 'Mihail'
        client_msg = processing_client_msg({ACTION: PRESENCE, TIME: 1, USER: {USERNAME: username}})
        self.assertEqual(client_msg, {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_processing_client_msg_wrong_action(self):
        client_msg = processing_client_msg({ACTION: PROBE, TIME: 1, USER: {USERNAME: 'Anonymous'}})
        self.assertEqual(client_msg, {RESPONSE: 400, ERROR: 'Bad Request'})


if __name__ == '__main__':
    main()
