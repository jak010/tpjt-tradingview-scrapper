from __future__ import annotations

from functools import cached_property

import rel
import requests
import websocket

from http_helper import utils
from http_helper.FakeHeader import FakeHeader
from trading_view_helper.message_helper import MessageHelper
from trading_view_helper.utils import get_random_session_id, get_random_chart_session_id


# http_session.verify = False

class ProcessStratgy: pass


class WebSocketOpenProcess(ProcessStratgy):
    def __init__(self, websocket_app, client: MyWebSocketClient):
        self.websocket_app = websocket_app
        self.client = client

    @cached_property
    def chart_session_id(self):
        return get_random_chart_session_id()

    @cached_property
    def session_id(self):
        return get_random_session_id()

    @property
    def get_authorized_token(self):
        return MessageHelper(
            func="set_auth_token",
            parameters=["unauthorized_user_token"]
        ).construct_message()

    @property
    def get_chart_create_session(self):
        return MessageHelper(
            func='chart_create_session',
            parameters=[self.chart_session_id, ""]
        ).construct_message()

    @property
    def get_quote_create_session(self):
        return MessageHelper(
            func='quote_create_session',
            parameters=[self.session_id]
        ).construct_message()

    @property
    def get_quote_add_symbols(self):
        return MessageHelper(
            func='quote_add_symbols',
            parameters=[self.session_id, "BINANCE:BTCUSDT", {"flags": ['force_permission']}]
        ).construct_message()

    @property
    def get_quote_set_fields(self):
        return MessageHelper(
            func='quote_set_fields',
            parameters=[self.session_id, "ch", "chp", "current_session", "description", "local_description", "language",
                        "exchange", "fractional", "is_tradable", "lp", "lp_time", "minmov", "minmove2", "original_name",
                        "pricescale", "pro_name", "short_name", "type", "update_mode", "volume", "currency_code",
                        "rchp", "rtc"]
        ).construct_message()

    @property
    def get_resolve_symbol(self):
        return MessageHelper(
            func='resolve_symbol',
            parameters=[self.chart_session_id, "symbol_1",
                        "={\"symbol\":\"BINANCE:BTCUSDT\",\"adjustment\":\"splits\"}"]
        ).construct_message()

    @property
    def get_create_series(self):
        return MessageHelper(
            func="create_series",
            parameters=[self.chart_session_id, "s1", "s1", "symbol_1", "1", 300]
        ).construct_message()

    @property
    def get_quote_fast_symbols(self):
        return MessageHelper(
            func="quote_fast_symbols",
            parameters=[self.session_id, "BINANCE:BTCUSDT"]
        ).construct_message()

    @property
    def get_create_study(self):
        return MessageHelper(
            func="create_study",
            parameters=[self.chart_session_id, "st1", "st1", "s1", "Volume@tv-basicstudies-118",
                        {"length": 20, "col_prev_close": "false"}]
        ).construct_message()

    @property
    def get_quote_hibernate_all(self):
        return MessageHelper(
            func="quote_hibernate_all",
            parameters=[self.session_id]
        ).construct_message()

    def send(self):

        if not self.client.process_check_flag['get_authorized_token']:
            self.websocket_app.send(self.get_authorized_token)
            self.client.process_check_flag['get_authorized_token'] = True

        if not self.client.process_check_flag['get_chart_create_session']:
            self.websocket_app.send(self.get_chart_create_session)
            self.client.process_check_flag['get_chart_create_session'] = True

        if not self.client.process_check_flag['get_quote_create_session']:
            self.websocket_app.send(self.get_quote_create_session)
            self.client.process_check_flag['get_quote_create_session'] = True

        if not self.client.process_check_flag['quote_set_field']:
            self.websocket_app.send(self.get_quote_set_fields)
            self.client.process_check_flag['quote_set_field'] = True

        if not self.client.process_check_flag['quote_add_symbols']:
            self.websocket_app.send(self.get_quote_add_symbols)
            self.client.process_check_flag['quote_add_symbols'] = True

        if not self.client.process_check_flag['get_resolve_symbol']:
            self.websocket_app.send(self.get_resolve_symbol)
            self.client.process_check_flag['get_resolve_symbol'] = True

        if not self.client.process_check_flag['get_create_series']:
            self.websocket_app.send(self.get_create_series)
            self.client.process_check_flag['get_create_series'] = True

        if not self.client.process_check_flag['get_quote_fast_symbols']:
            self.websocket_app.send(self.get_quote_fast_symbols)
            self.client.process_check_flag['get_quote_fast_symbols'] = True

        if not self.client.process_check_flag['get_create_study']:
            self.websocket_app.send(self.get_create_study)
            self.client.process_check_flag['get_create_study'] = True

        if not self.client.process_check_flag['get_quote_hibernate_all']:
            self.websocket_app.send(self.get_quote_hibernate_all)
            self.client.process_check_flag['get_quote_hibernate_all'] = True


class WebSocketMessageProcess(ProcessStratgy):
    def __init__(self, websocket_app, client: MyWebSocketClient, session_id, chart_session_id):
        self.client = client
        self.websocket_app = websocket_app
        self.session_id = session_id
        self.chart_session_id = chart_session_id

    @property
    def get_request_more_data(self):
        chunk = 1024
        return MessageHelper(
            func='request_more_data',
            parameters=[self.chart_session_id, "sds_1", chunk]
        ).construct_message()

    def send(self):
        self.websocket_app.send(self.get_request_more_data)


class MyWebSocketClient:

    def __init__(self, http_headers):
        self.cached = dict()
        self.process_check_flag = {
            "get_authorized_token": False,
            "get_chart_create_session": False,
            'get_quote_create_session': False,
            "quote_create_session": False,
            "quote_set_field": False,
            "quote_add_symbols": False,
            "get_resolve_symbol": False,
            'get_create_series': False,
            'get_quote_fast_symbols': False,
            "get_create_study": False,
            "get_quote_hibernate_all": False
        }

        # self.message_process = WebSocketMessageProcess(
        #     websocket_app=self,
        #     session_id=self.open_process.session_id,
        #     chart_session_id=self.open_process.chart_session_id
        # )

        self.ws_app = websocket.WebSocketApp(
            url=utils.get_test_websocket_uri(),
            header=http_headers,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_open=self.on_open
        )

        self.open_process = WebSocketOpenProcess(
            self.ws_app,
            client=self
        )

    def on_message(self, ws, msg):
        print("[*]")
        import re

        result = msg
        pattern = re.compile("~m~\d+~m~~h~\d+$")
        if pattern.match(result):
            print(result)
            self.ws_app.send(result)

        # self.message_process.send()

    def on_error(self, ws, msg):
        print("on_error", ws, msg)

    def on_close(self, *args, **kwargs):
        print("=" * 100)
        print(self.open_process.session_id, self.open_process.chart_session_id)
        print("DELETE AFTER")
        self.open_process = WebSocketOpenProcess(self.ws_app, client=self)
        print(self.open_process.session_id, self.open_process.chart_session_id)

        ws.ws_app.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def on_open(self, ws):
        self.open_process.send()


if __name__ == '__main__':
    fake_header = FakeHeader()
    http_session = requests.Session()

    r = http_session.get(utils.get_test_http_uri(), headers=fake_header.build())
    print(r.headers, r.status_code)

    ws = MyWebSocketClient(http_headers=r.headers)
    ws.ws_app.run_forever()

    # 1t = 80s
    # 2t(opt) = 80s
