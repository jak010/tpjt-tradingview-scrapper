from __future__ import annotations

import os
import concurrent.futures
import csv
import json
import re
import threading
import time

import websocket

import constant
from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket.dispatcher.open_dispatcher import WebSocketOpenDispatcher
from lib.websocket.method import send_functions, dto
from lib.websocket.method.types.timescaleupdate_types import TimeScaleUpdateTickData


class TradingViewScrapingWebSocketApp(websocket.WebSocketApp):

    def __call__(self, *args, **kwargs):
        self.run_forever()

    def __init__(self, symbol_name: str):
        self._session_id = utils.get_random_session_id()
        self._chart_session_id = utils.get_random_chart_session_id()
        self.symbol_name = symbol_name

        import os
        print(os.getpid(), self.symbol_name)

        self._start_timer = int(time.time())

        super().__init__(
            url=constant.TRADING_VIEW_WSS_URL + constant.TEST_PARAM2,
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

        self.health_check(recv_msg=recv_msg)

        rex_search_payload_length = re.search(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)
        if rex_search_payload_length is not None:
            if int(rex_search_payload_length.group('length')) > 1:

                # each list in ['', 'length', 'data:dict', [...]]
                recv_msg_split = re.split(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)

                for token in recv_msg_split:

                    # Token이 Websocket의 payload인 경우
                    if token.find("{") != -1:
                        token = json.loads(token)

                        # Method Name이 웹소켓 페이로드에 존재하는 경우
                        # - 'm' 은 메소드 네임을 뜻함
                        if 'm' in token and token['m'] == 'timescale_update':
                            timescaleupdate_dto = dto.TimeScaleUpdateMessageDto(token)

                            if timescaleupdate_dto.p.position2:
                                # print(timescaleupdate_dto.p.position2)
                                tick_list = [TimeScaleUpdateTickData(*(each['v'])) for each in
                                             timescaleupdate_dto.p.position2_of_key_in_s1_in_s]

                                for tick in sorted(tick_list, reverse=True):
                                    # print(self.symbol_name, tick.to_humanize(), tick.date_time)

                                    # csv save
                                    with open(f"./store/{self.symbol_name}_1D_OHCL.csv", "a", encoding="utf-8",
                                              newline='') as f:
                                        c = csv.writer(f)
                                        c.writerow([
                                            tick.to_humanize(), tick.date_time, tick.open, tick.high,
                                            tick.low, tick.close, tick.volume
                                        ])

            threading.Thread(
                target=chart_left_shift,
                daemon=True
            ).start()

            self._end_time = int(time.time())
            print(self.symbol_name, ":", self._end_time - self._start_timer)
            LIMIT_TIME = 180

            if self._end_time - self._start_timer >= LIMIT_TIME:
                self.close()

    def on_open(self, ws):
        websocketopendispatcher = WebSocketOpenDispatcher(
            session_id=self._session_id,
            chart_session_id=self._chart_session_id
        )
        try:
            self.send(websocketopendispatcher.on_authorized_token)
            self.send(websocketopendispatcher.on_chart_create_session)
            self.send(websocketopendispatcher.on_quote_create_session)
            self.send(websocketopendispatcher.on_quote_set_fields)

            self.send(websocketopendispatcher.on_quote_add_symobls_v2(symbol_name=self.symbol_name))
            self.send(websocketopendispatcher.on_resolve_symobl(symbol_name=self.symbol_name))
            self.send(websocketopendispatcher.on_create_series())

            self.send(websocketopendispatcher.on_quote_fast_symbols(symbol_name=self.symbol_name))

            self.send(websocketopendispatcher.on_create_study())

            self.send(websocketopendispatcher.on_quote_hibernate_all)
        except Exception as e:
            self.close()
            pass

    def on_close(self, *args, **kwargs):
        # print(args, kwargs)
        print(">>>> CLOSED")
        self.close()

    def on_error(self, ws, msg):
        # print("[*]Error", ws, msg)
        self.close()

    def health_check(self, recv_msg):
        pattern = re.compile("~m~\d+~m~~h~\d+$")
        if pattern.match(recv_msg):
            self.send(recv_msg)


def task_app(symbol_name):
    app = TradingViewScrapingWebSocketApp(symbol_name=symbol_name)
    app.run_forever()


if __name__ == '__main__':
    SYMBOL_CODES_SELECT_28 = {
        'EURUSD': '1',
        'GBPUSD': '2',
        'USDJPY': '3',
        'GBPJPY': '4',
    }

    symbol_names = [symbol_name for symbol_name in SYMBOL_CODES_SELECT_28.keys()]

    MAX_WORKER = os.cpu_count()

    count = 0
    remainder = len(symbol_names) // 10
    divider = len(symbol_names) % 10

    # MAX CORE 만큼 인덱싱 처리하기
    index_range = []
    for idx, value in enumerate(symbol_names, start=1):
        if idx % MAX_WORKER == 0:
            start_index = count * MAX_WORKER
            end_index = idx
            index_range.append((start_index, end_index))
            count += 1

            if count == remainder:
                start_index = count * MAX_WORKER
                end_index = start_index + divider

                index_range.append((start_index, end_index))

    for name in symbol_names:
        task_app(name)
