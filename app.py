from __future__ import annotations

import re

from websocket import WebSocketApp

from lib import constant

from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher

from lib.websocket.method import interface_functions
import logging
logging.basicConfig(level=-1)

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
        print("\n")
        print("[*]", recv_msg)
        print(len(recv_msg))
        print("=" * 25)
        self.re_send(recv_msg=recv_msg)

    def on_open(self, ws):
        websocketopendispatcher = WebSocketOpenDispatcher(
            session_id=self._session_id,
            chart_session_id=self._chart_session_id
        )
        self.send(websocketopendispatcher.set_authorized_token)
        self.send(websocketopendispatcher.set_chart_create_session)
        self.send(websocketopendispatcher.set_quote_create_session)
        self.send(websocketopendispatcher.set_quote_add_symbols())
        self.send(websocketopendispatcher.set_get_quote_set_fields)
        self.send(websocketopendispatcher.set_resolve_symobl())
        self.send(websocketopendispatcher.set_create_series())
        self.send(websocketopendispatcher.set_quote_fast_symbols())
        self.send(websocketopendispatcher.set_create_study())
        self.send(websocketopendispatcher.set_quote_hibernate_all)

        def tmp():
            import time
            time.sleep(5)
            print('*' * 30)
            # self.send(interface_functions.get_request_more_tickmarks(
            #     chart_session_id=self._chart_session_id
            # ))
            self.send(interface_functions.get_request_more_data(
                chart_session_id=self._chart_session_id
            ))

        import threading
        threading.Thread(target=tmp).start()

    def on_close(self, *args, **kwargs):
        print(args, kwargs)
        exit()

    def on_error(self, ws, msg):
        print(ws, msg)

    def re_send(self, recv_msg):
        pattern = re.compile("~m~\d+~m~~h~\d+$")
        if pattern.match(recv_msg):
            self.send(recv_msg)
            # self.send(interface_functions.get_request_more_data(
            #     chart_session_id=self._chart_session_id
            # ))


if __name__ == '__main__':

    app = TradingViewScrapingWebSocketApp(
        trading_view_wss_url=constant.TRADING_VIEW_WSS_URL
    )
    app.run_forever()
