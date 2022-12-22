import json

from ..method import interface_functions


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
        return interface_functions.get_authorized_token()

    @property
    def on_chart_create_session(self) -> str:
        return interface_functions.get_chart_create_session(
            chart_session_id=self._chart_session_id
        )

    @property
    def on_quote_create_session(self) -> str:
        return interface_functions.get_quote_create_session(
            session_id=self._session_id
        )

    @property
    def on_quote_set_fields(self) -> str:
        return interface_functions.get_quote_set_fields(
            session_id=self._session_id
        )

    @property
    def on_quote_hibernate_all(self):
        return interface_functions.get_quote_hibernate_all(
            session_id=self._session_id
        )

    def on_quote_add_symbols(self):
        return interface_functions.get_quote_add_symbols(
            session_id=self._session_id,
            symbols="FX:EURUSD",
            flags={"flags": ['force_permission']}
        )

    def on_resolve_symobl(self):
        """
        symbol_name - > FX:EURUSD
        """
        return interface_functions.get_resolve_symbol(
            chart_session_id=self._chart_session_id,
            param1="symbol_1",
            param2="={\"adjustment\":\"splits\",\"symbol\":\"FX:EURUSD\"}"
        )

    def on_create_series(self):
        return interface_functions.get_create_series(
            chart_session_id=self._chart_session_id,
            param1="s1",
            param2="s1",
            param3="symbol_1",
            param4="D",
            param5=300
        )

    def on_quote_fast_symbols(self):
        return interface_functions.get_quote_fast_symbols(
            session_id=self._session_id,
            symbols="FX:EURUSD"
        )

    def on_create_study(self):
        return interface_functions.get_create_study(
            chart_session_id=self._chart_session_id,
            param1="st1",
            param2="st1",
            param3="s1",
            param4="Volume@tv-basicstudies-118",
            param5={"length": 20, "col_prev_close": "false"}
        )