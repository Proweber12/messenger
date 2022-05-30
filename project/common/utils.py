import json

from common.variables import ENCODING, MAX_PACKAGE_SIZE


def get_message(client):

    encoded_response = client.recv(MAX_PACKAGE_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(socket, msg):
    conversion_to_json = json.dumps(msg).encode(ENCODING)
    socket.send(conversion_to_json)
