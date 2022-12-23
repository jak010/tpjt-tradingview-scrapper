from __future__ import annotations

import json
import re
import threading
import time

import websocket
from websocket import WebSocketApp

import constant
from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher
from lib.websocket.method import send_functions, dto
from lib.websocket.method.types.timescaleupdate_types import TimeScaleUpdateTickData
import csv


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
        print(ws, recv_msg)

        def chart_left_shift(*args):
            time.sleep(5)
            self.send(send_functions.get_request_more_tickmarks(
                chart_session_id=self._chart_session_id
            ))
            time.sleep(5)
            self.send(send_functions.get_request_more_data(
                chart_session_id=self._chart_session_id
            ))
        #
        # rex_search_payload_length = re.search(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)
        # if rex_search_payload_length is not None:
        #     if int(rex_search_payload_length.group('length')) > 1:
        #
        #         # each list in ['', 'length', 'data:dict', [...]]
        #         recv_msg_split = re.split(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)
        #
        #         for token in recv_msg_split:
        #
        #             # Token이 Websocket의 payload인 경우
        #             if token.find("{") != -1:
        #                 token = json.loads(token)
        #
        #                 # Method Name이 웹소켓 페이로드에 존재하는 경우
        #                 # - 'm' 은 메소드 네임을 뜻함
        #                 if 'm' in token and token['m'] == 'timescale_update':
        #                     timescaleupdate_dto = dto.TimeScaleUpdateMessageDto(token)
        #
        #                     if timescaleupdate_dto.p.position2:
        #                         tick_list = [TimeScaleUpdateTickData(*(each['v'])) for each in
        #                                      timescaleupdate_dto.p.position2_of_key_in_s1_in_s]
        #
        #                         print("*" * 100)
        #                         for tick in sorted(tick_list, reverse=True):
        #                             print(tick.to_humanize(), tick.date_time, tick.open, tick.low)
        #
        #                             # csv save
        #                             with open("./data2.csv", "a", encoding="utf-8", newline='') as f:
        #                                 c = csv.writer(f)
        #                                 c.writerow([
        #                                     tick.to_humanize(), tick.date_time, tick.open, tick.high,
        #                                     tick.low, tick.close, tick.volume
        #                                 ])
        #
        #                             if tick.date_time <= 31788000:
        #                                 time.sleep(5)
        #                                 exit()
        #
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
        self.send(websocketopendispatcher.on_quote_add_symbols(symbol_name="GBPUSD"))
        self.send(websocketopendispatcher.on_quote_set_fields)
        self.send(websocketopendispatcher.on_resolve_symobl(symbol_name="GBPUSD"))
        self.send(websocketopendispatcher.on_create_series())
        self.send(websocketopendispatcher.on_quote_fast_symbols(symbol_name="GBPUSD"))
        self.send(websocketopendispatcher.on_create_study())
        self.send(websocketopendispatcher.on_quote_hibernate_all)

    def on_close(self, *args, **kwargs):
        print(args, kwargs)
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
