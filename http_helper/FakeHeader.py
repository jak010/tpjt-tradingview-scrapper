from __future__ import annotations

from fake_useragent import UserAgent

from . import utils


class FakeHeader:
    def __init__(self, host: str = None, origin: str = None):
        self.headers = dict()

        if host is not None:
            self._host = host
        else:
            self._host = "data.tradingview.com"

        if origin is not None:
            self._origin = origin
        else:
            self._origin = "https://kr.tradingview.com"

        self.fake_user_agent = UserAgent()

    def _set_fake_user_agent(self):
        # self.headers['User-Agent'] = self.fake_user_agent.random
        self.headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        return self

    def _set_host(self):
        self.headers["Host"] = self._host
        return self

    def _set_sec_websocket_version(self):
        self.headers["Sec-WebSocket-Version"] = "13"
        return self

    def _set_sec_websocket_key(self):
        self.headers["Sec-WebSocket-Key"] = utils.generator_sec_websocket_key()
        return self

    def _set_upgrade(self):
        self.headers["Upgrade"] = "websocket"
        return self

    def _set_origin(self):
        self.headers["Origin"] = self._origin
        return self

    def _set_cache_control(self):
        self.headers["Cache-Control"] = "no-cache"
        return self

    def _set_connection(self):
        self.headers["Connection"] = "Upgrade"
        return self

    def _set_pragma(self):
        self.headers["Pragma"] = "no-cache"
        return self

    def get_header(self):
        return self.headers

    def build(self):
        return self._set_fake_user_agent() \
            ._set_host() \
            ._set_sec_websocket_version() \
            ._set_sec_websocket_key() \
            ._set_upgrade() \
            ._set_origin() \
            ._set_cache_control() \
            ._set_connection() \
            ._set_pragma() \
            .get_header()
