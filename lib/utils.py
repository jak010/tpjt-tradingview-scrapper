import string
import random
import base64

session_string_length = 12


def get_random_ascii():
    return [random.choice(string.ascii_lowercase) for i in range(session_string_length)]


def get_random_string():
    return ''.join(get_random_ascii())


def get_random_session_id():
    return "qs_" + get_random_string()


def get_random_chart_session_id():
    return "cs_" + get_random_string()


def get_random_16_byte() -> bytes:
    return bytes([random.randint(0, 255) for _ in range(16)])


def generator_sec_websocket_key() -> str:
    return base64.b64encode(get_random_16_byte()).decode()


