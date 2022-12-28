from __future__ import annotations

import concurrent.futures
import time
from typing import List, Tuple

import constant
from lib import utils
from lib.http.FakeHeader import FakeHeader
from lib.websocket import TradingViewScrapingWebSocketApp
from lib.websocket import utils as ws_utils


def task_app(symbol_name):
    app = TradingViewScrapingWebSocketApp(
        symbol_name=symbol_name,
        session_id=utils.get_random_session_id(),
        chart_session_id=utils.get_random_chart_session_id(),
        fake_header=FakeHeader().build()
    )
    app.run_forever()


if __name__ == '__main__':
    TRADING_VIEW_ENABLE_MAX_WORKER = 6
    symbol_names = [symbol_name for symbol_name in
                    constant.SYMBOL_CODES_SELECT_28.keys()]

    cut_of_range: List[Tuple[int, int]] = ws_utils.cut_of_range_by_number(
        symbol_names, TRADING_VIEW_ENABLE_MAX_WORKER
    )

    # TradingView에서 연결을 제한하는 듯 보임
    # - Handshake status 429 Too Many Requests
    #  - MAX_WORKER의 수는 위 Error가 안 나는 수준에서 제한함

    with concurrent.futures.ProcessPoolExecutor(6) as executor:
        for start, end in cut_of_range:
            print("[*] Current:", start, end, symbol_names[start:end])
            futures = executor.map(task_app, symbol_names[start:end])
            time.sleep(15)
