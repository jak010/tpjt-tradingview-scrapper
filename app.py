from __future__ import annotations

import re
import threading
import time

from websocket import WebSocketApp

import constant
from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher
from lib.websocket.method import interface_functions


class TradingViewScrapingWebSocketApp(WebSocketApp):

    def __init__(self, trading_view_wss_url: str):
        self._session_id = utils.get_random_session_id()
        self._chart_session_id = utils.get_random_chart_session_id()

        super().__init__(
            url=trading_view_wss_url,
            header=FakeHeader().build(),
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_open=self.on_open
        )

    def on_message(self, ws, recv_msg):
        def chart_left_shift(*args):
            time.sleep(20)
            print('*' * 30)
            self.send(interface_functions.get_request_more_tickmarks(
                chart_session_id=self._chart_session_id
            ))
            time.sleep(20)
            self.send(interface_functions.get_request_more_data(
                chart_session_id=self._chart_session_id
            ))
            print('*' * 30)

        rex_search_payload_length = re.search(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)
        if rex_search_payload_length is not None:
            f = re.split(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)
            for x in f:
                print(x)
            print("\n")

        self.re_send(recv_msg=recv_msg)

        threading.Thread(
            target=chart_left_shift,
            daemon=True
        ).start()

    def on_open(self, ws):
        websocketopendispatcher = WebSocketOpenDispatcher(
            session_id=self._session_id,
            chart_session_id=self._chart_session_id
        )
        self.send(websocketopendispatcher.on_authorized_token)
        self.send(websocketopendispatcher.on_chart_create_session)
        self.send(websocketopendispatcher.on_quote_create_session)
        self.send(websocketopendispatcher.on_quote_add_symbols())
        self.send(websocketopendispatcher.on_quote_set_fields)
        self.send(websocketopendispatcher.on_resolve_symobl())
        self.send(websocketopendispatcher.on_create_series())
        self.send(websocketopendispatcher.on_quote_fast_symbols())
        self.send(websocketopendispatcher.on_create_study())
        self.send(websocketopendispatcher.on_quote_hibernate_all)

    def on_close(self, *args, **kwargs):
        print(">>>> CLOSED")

    def on_error(self, ws, msg):
        print(ws, msg)

    def re_send(self, recv_msg):
        pattern = re.compile("~m~\d+~m~~h~\d+$")
        if pattern.match(recv_msg):
            self.send(recv_msg)


if __name__ == '__main__':
    app = TradingViewScrapingWebSocketApp(
        trading_view_wss_url=constant.TRADING_VIEW_WSS_URL
    )
    app.run_forever()
