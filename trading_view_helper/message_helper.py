import json
import websocket


class MessageHelper:
    def __init__(self, func, parameters):
        self.func = func
        self.parameter = parameters

    @property
    def payload(self):
        return {
            'm': self.func,
            'p': self.parameter
        }

    @property
    def json_payload(self):
        return json.dumps(self.payload, separators=(",", ":"))

    @property
    def json_payload_len(self):
        return len(self.json_payload)

    @property
    def _message_prefix(self):
        return "~m~"

    @property
    def _message_suffix(self):
        return "~m~"

    def construct_message(self):
        return self._message_prefix \
               + str(self.json_payload_len) \
               + self._message_suffix \
               + self.json_payload

    def __len__(self):
        return self.json_payload_len

# if __name__ == '__main__':
#     ws = websocket.WebSocketApp(url='localhost:8080')
#
#     # send_message('a', "set_auth_token", ["unauthorized_user_token"])
#
#     message = MessageHelper(
#         func='set_auth_token',
#         parameters=['a']
#     )
#
#     print(message.construct_message())
