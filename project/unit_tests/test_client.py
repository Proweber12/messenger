import sys
from unittest import TestCase, main

sys.path.append('../')
from client import generate_presence, parse_server_message
from common.variables import TIME, ACTION, PRESENCE, USER, USERNAME, RESPONSE, ERROR


class TestClient(TestCase):

    def test_generator_presence_default(self):
        test_generator = generate_presence()
        test_generator[TIME] = 1
        self.assertEqual(test_generator,
        {
            ACTION: PRESENCE,
            TIME: 1,
            USER: {USERNAME: 'Anonymous'}
        })

    def test_generator_presence_custom(self):
        username = 'Mihail'
        test_generator = generate_presence(username)
        test_generator[TIME] = 1
        self.assertEqual(test_generator,
        {
            ACTION: PRESENCE,
            TIME: 1,
            USER: {USERNAME: username}
        })

    def test_parse_server_message_200(self):
        self.assertEqual(parse_server_message({RESPONSE: 200}), 'Status code 200: OK')

    def test_parse_server_message_400(self):
        self.assertEqual(parse_server_message({RESPONSE: 400, ERROR: 'Bad Request'}), 'Status code 400: Bad Request')

    def test_parse_server_message_value_error(self):
        self.assertRaises(ValueError, parse_server_message, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    main()
