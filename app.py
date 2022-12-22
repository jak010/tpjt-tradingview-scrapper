from __future__ import annotations

import json
import re
import threading
import time
from datetime import datetime
from websocket import WebSocketApp

import constant
from ast import literal_eval
from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher
from lib.websocket.method import send_functions, dto


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
            time.sleep(5)
            self.send(send_functions.get_request_more_tickmarks(
                chart_session_id=self._chart_session_id
            ))
            time.sleep(5)
            self.send(send_functions.get_request_more_data(
                chart_session_id=self._chart_session_id
            ))

        rex_search_payload_length = re.search(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)

        if rex_search_payload_length is not None:

            if int(rex_search_payload_length.group('length')) > 1:
                recv_msg_split = re.split(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)

                for token in recv_msg_split:
                    try:
                        token_to_obj = literal_eval(token)
                        if isinstance(token_to_obj, dict):
                            timescaleupdate_dto = dto.TimeScaleUpdateMessageDto(token_to_obj)

                            if timescaleupdate_dto.parmeters.position2_of_key_in_s1_in_s:
                                # 과거 데이터
                                print("*" * 100)
                                print(timescaleupdate_dto)
                                for each in timescaleupdate_dto.parmeters.position2_of_key_in_s1_in_s:
                                    print(datetime.fromtimestamp(each['v'][0]), each['v'])

                    except Exception as e:
                        pass
                        # token_to_json = json.dumps(token)
                        # token_to_json = literal_eval(token_to_json)
                        # print(token_to_json)

        self.health_check(recv_msg=recv_msg)

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
        print("[*]Error", ws, msg)

    def health_check(self, recv_msg):
        pattern = re.compile("~m~\d+~m~~h~\d+$")
        if pattern.match(recv_msg):
            self.send(recv_msg)


if __name__ == '__main__':
    app = TradingViewScrapingWebSocketApp(
        trading_view_wss_url=constant.TRADING_VIEW_WSS_URL + constant.TEST_PARAM
    )
    app.run_forever()
