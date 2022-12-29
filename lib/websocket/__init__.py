from __future__ import annotations

import json
import re
import threading
import time

import websocket

import constant
from lib.websocket import utils as ws_utils
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher
from lib.websocket.method import dto
from lib.websocket.method.types.timescaleupdate_types import TimeScaleUpdateTickData


class TradingViewScrapingWebSocketApp(websocket.WebSocketApp):

    def __init__(self, symbol_name: str, session_id, chart_session_id, fake_header):
        self.symbol_name = symbol_name
        self._session_id = session_id
        self._chart_session_id = chart_session_id
        self.fake_header = fake_header

        self.CONNECTION_LIMIT_SEC = 180

        self.start_time = int(time.time())

        super().__init__(
            url=constant.TRADING_VIEW_WSS_URL + constant.TEST_PARAM2,
            header=self.fake_header,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_open=self.on_open
        )

    def on_message(self, ws, recv_msg):
        print("Working...", self.symbol_name)

        if ws_utils.is_connect(
                start_time=self.start_time,
                close_second=self.CONNECTION_LIMIT_SEC
        ):
            self.close()

        ws_utils.health_check(ws_app=self, recv_msg=recv_msg)

        search_message_length = ws_utils.regex_search(recv_msg)
        if search_message_length is not None:
            message_lenth_minimum = 1
            message_lenth = search_message_length.group('length')

            if int(message_lenth) > message_lenth_minimum:
                recv_msg_split = ws_utils.regex_split(recv_msg)

                for token in recv_msg_split:
                    if ws_utils.token_is_start_brace(token):
                        token = json.loads(token)

                        timescaleupdate_dto = ws_utils.check_timescaleupdate_method(token)
                        if timescaleupdate_dto and timescaleupdate_dto is not None:
                            tick_list = [TimeScaleUpdateTickData(*(each['v'])) for each in
                                         timescaleupdate_dto.p.position2_of_key_in_s1_in_s]

                            ws_utils.csv_save(
                                symbol_name=self.symbol_name,
                                tick_list=tick_list
                            )

            threading.Thread(
                target=ws_utils.chart_left_shift, args=(self,),
                daemon=True
            ).start()

    def on_open(self, ws):
        websocketopendispatcher = WebSocketOpenDispatcher(
            session_id=self._session_id,
            chart_session_id=self._chart_session_id
        )
        try:
            # WebSocket 연결 시 전송하는 메서드
            # - send 순서는 아래 정의된 순서에 따라야됨
            self.send(websocketopendispatcher.on_authorized_token)
            self.send(websocketopendispatcher.on_chart_create_session)
            self.send(websocketopendispatcher.on_quote_create_session)
            self.send(websocketopendispatcher.on_quote_set_fields)

            self.send(websocketopendispatcher.on_quote_add_symbols(symbol_name=self.symbol_name))
            self.send(websocketopendispatcher.on_resolve_symobl(symbol_name=self.symbol_name))
            self.send(websocketopendispatcher.on_create_series())

            self.send(websocketopendispatcher.on_quote_fast_symbols(symbol_name=self.symbol_name))
            self.send(websocketopendispatcher.on_create_study())
            self.send(websocketopendispatcher.on_quote_hibernate_all)
        except Exception as e:
            print(e)
            self.close()

    def on_close(self, *args, **kwargs):
        print("[-]CLOSED:", args, kwargs)
        self.close()

    def on_error(self, ws, msg):
        print("[-]Error", ws, msg)

    def __repr__(self):
        return self.symbol_name
