from __future__ import annotations

import base64
import random

WEBSOCKET_URL = "wss://data.tradingview.com/socket.io/websocket"
HTTP_URL = "https://data.tradingview.com/socket.io/websocket"

TEST_PARAM = "?from=symbols%2FEURUSD%2F&date=2022_12_16-12_49"


def get_random_16_byte() -> bytes:
    return bytes([random.randint(0, 255) for _ in range(16)])


def generator_sec_websocket_key() -> str:
    return base64.b64encode(get_random_16_byte()).decode()


def get_test_websocket_uri():
    return WEBSOCKET_URL + TEST_PARAM


def get_test_http_uri():
    return HTTP_URL + TEST_PARAM
