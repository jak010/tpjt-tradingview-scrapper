from ..method import send_functions
import json


class WebSocketOpenDispatcher:
    """ 웹소켓 open 시점에 발송되는 함수들

    Method List
        'set_auth_token', 'chart_create_session', 'quote_create_session',
        'quote_add_symbols','quote_set_fields','resolve_symbol', 'create_series': False,
        'quote_fast_symbols','create_study','quote_hibernate_all'
    """

    def __init__(self, session_id, chart_session_id):
        self._session_id = session_id
        self._chart_session_id = chart_session_id

    @property
    def on_authorized_token(self) -> str:
        return send_functions.get_authorized_token()

    @property
    def on_chart_create_session(self) -> str:
        return send_functions.get_chart_create_session(
            chart_session_id=self._chart_session_id
        )

    @property
    def on_quote_create_session(self) -> str:
        return send_functions.get_quote_create_session(
            session_id=self._session_id
        )

    @property
    def on_quote_set_fields(self) -> str:
        return send_functions.get_quote_set_fields(
            session_id=self._session_id
        )

    @property
    def on_quote_hibernate_all(self):
        return send_functions.get_quote_hibernate_all(
            session_id=self._session_id
        )

    def on_quote_add_symbols(self, symbol_name):
        """
        symbol_name - > FX:EURUSD
        """

        # sendMessage(ws, "quote_add_symbols", [session, "BINANCE:BTCUSDT", {"flags": ['force_permission']}])

        return send_functions.get_quote_add_symobls_v2(
            chart_session_id=self._session_id,
            param1=f"FX:{symbol_name}",
            param2='{"flags": ["force_permission"]}'
        )

    def on_resolve_symobl(self, symbol_name):
        """
        symbol_name - > FX:EURUSD
        """

        # _template = '={"adjustment":"splits","sds_sym_1", "symbols":"FX:"%s"}' % symbol_name
        _template2 = "={\"symbol\":\"FX:%s\",\"adjustment\":\"splits\"}" % symbol_name

        return send_functions.get_resolve_symbol(
            chart_session_id=self._chart_session_id,
            param1="symbol_1",
            param2=_template2
        )

    def on_create_series(self):
        return send_functions.get_create_series(
            chart_session_id=self._chart_session_id,
            param1="s1",
            param2="s1",
            param3="symbol_1",
            param4="D",
            param5=300
        )

    def on_quote_fast_symbols(self, symbol_name):
        return send_functions.get_quote_fast_symbols(
            session_id=self._session_id,
            symbols="FX:" + symbol_name
        )

    def on_create_study(self):
        return send_functions.get_create_study(
            chart_session_id=self._chart_session_id,
            param1="st1",
            param2="st1",
            param3="s1",
            param4="Volume@tv-basicstudies-118",
            param5={"length": 20, "col_prev_close": "false"}
        )
