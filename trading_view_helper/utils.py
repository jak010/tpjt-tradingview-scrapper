import string
import random

session_string_length = 12


def get_random_ascii():
    return [random.choice(string.ascii_lowercase) for i in range(session_string_length)]


def get_random_string():
    return ''.join(get_random_ascii())


def get_random_session_id():
    return "qs_" + get_random_string()


def get_random_chart_session_id():
    return "cs_" + get_random_string()
