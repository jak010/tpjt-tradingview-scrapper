from __future__ import annotations

import csv
import os
import re
import time
from typing import List, NoReturn, Optional

import websocket

from websocketlib.method import send_functions, dto
from websocketlib.method.types.timescaleupdate_types import TimeScaleUpdateTickData


def regex_search(recv_msg):
    return re.search(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)


def regex_split(recv_msg) -> List[str]:
    """ Receieve 메시지 split 처리하기
      Return -> ['', 'length', 'data:dict', ...]
    """
    return re.split(r"~m~(?P<length>\d[0-9]+)~m~", recv_msg)


def chart_left_shift(ws_app) -> NoReturn:
    """ Chart를 왼쪽으로 이동 """
    time.sleep(5)

    try:
        if ws_app.keep_running and ws_app.sock is not None:
            ws_app.send(send_functions.get_request_more_tickmarks(
                chart_session_id=ws_app._chart_session_id
            ))
            time.sleep(5)
            ws_app.send(send_functions.get_request_more_data(
                chart_session_id=ws_app._chart_session_id
            ))
    except websocket._exceptions.WebSocketConnectionClosedException as e:
        print(e)


def cut_of_range_by_number(symbol_names: List[str], max_worker):
    # MAX CORE 만큼 인덱싱 처리하기

    count = 0
    remainder = len(symbol_names) // max_worker
    divider = len(symbol_names) % max_worker

    index_range = []
    for idx, value in enumerate(symbol_names, start=1):
        if idx % max_worker == 0:
            start_index = count * max_worker
            end_index = idx
            index_range.append((start_index, end_index))
            count += 1

            if count == remainder:
                start_index = count * max_worker
                end_index = start_index + divider

                index_range.append((start_index, end_index))
    return index_range


def root_dir():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(BASE_DIR)


def csv_save(symbol_name, tick_list: List[TimeScaleUpdateTickData]):
    """ CSV FILE SAVE """
    _SAVE_FILE_NAME = f"/{symbol_name}_1D_OHCL.csv"
    _SAVE_FILE_PATH = root_dir() + "/store" + _SAVE_FILE_NAME

    for tick in sorted(tick_list, reverse=True):
        with open(_SAVE_FILE_PATH, "a", encoding="utf-8",
                  newline='') as f:
            c = csv.writer(f)
            c.writerow([
                tick.to_humanize(), tick.date_time, tick.open, tick.high,
                tick.low, tick.close, tick.volume
            ])


def token_is_start_brace(token) -> bool:
    return token.find("{") != -1


def check_timescaleupdate_method(token) -> Optional[dto.TimeScaleUpdateMessageDto]:
    """ Receieve 메시지에 "timescaleupdate" 함수가 존재하는지 체크 """
    if 'm' in token and token['m'] == 'timescale_update':
        return dto.TimeScaleUpdateMessageDto(token)


def health_check(ws_app, recv_msg):
    """ Connection 유지를 위한 Health Check """
    pattern = re.compile("~m~\d+~m~~h~\d+$")
    if pattern.match(recv_msg):
        ws_app.send(recv_msg)


def is_connect(start_time: int, close_second: int):
    """ ws_app에서 지정한 시간이 지나면 connection 종료 """
    current_time = int(time.time())
    print(current_time - start_time, close_second)
    if current_time - start_time >= close_second:
        return True
