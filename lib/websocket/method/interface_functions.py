from lib.websocket.message.payload import Payload


def get_authorized_token():
    return Payload(
        func="set_auth_token",
        parameters=["unauthorized_user_token"]
    ).get_payload()


def get_chart_create_session(chart_session_id):
    return Payload(
        func='chart_create_session',
        parameters=[chart_session_id, ""]
    ).get_payload()


def get_quote_create_session(session_id):
    return Payload(
        func='quote_create_session',
        parameters=[session_id]
    ).get_payload()


def get_quote_add_symbols(session_id, symbols, flags):
    """
    Ex.
        symbols -> "BINANCE:BTCUSDT"
        flags -> {"flags": ['force_permission']}
    """

    return Payload(
        func='quote_add_symbols',
        parameters=[session_id, symbols, flags]
    ).get_payload()


def get_quote_set_fields(session_id):
    return Payload(
        func='quote_set_fields',
        parameters=[session_id, "base-currency-logoid", "ch", "chp", "currency-logoid", "currency_code", "currency_id",
                    "base_currency_id", "current_session", "description", "exchange", "format", "fractional",
                    "is_tradable", "language", "local_description", "listed_exchange", "logoid", "lp", "lp_time",
                    "minmov", "minmove2", "original_name", "pricescale", "pro_name", "short_name", "type", "typespecs",
                    "update_mode", "volume", "value_unit_id"]
    ).get_payload()


def get_resolve_symbol(chart_session_id, param1, param2):
    """
    Argument Example
        param1 -> "symbol_1"
        param2 -> "={\"symbol\":\"BINANCE:BTCUSDT\",\"adjustment\":\"splits\"}"

    """
    return Payload(
        func='resolve_symbol',
        parameters=[chart_session_id, param1, param2]
    ).get_payload()


def get_create_series(chart_session_id, param1, param2, param3, param4, param5):
    """
    Argument Example
        param1 -> "s1"
        param2 -> "s1"
        param3 -> "symbol_1"
        param4 -> "1"
        param5 -> 300
    """
    return Payload(
        func="create_series",
        parameters=[chart_session_id, param1, param2, param3, param4, param5, ""]
    ).get_payload()


def get_quote_fast_symbols(session_id, symbols):
    """
    Argument Example
        symbols -> "BINANCE:BTCUSDT"
    """
    return Payload(
        func="quote_fast_symbols",
        parameters=[session_id, symbols]
    ).get_payload()


def get_create_study(chart_session_id, param1, param2, param3, param4, param5):
    """ Arugment Example
        param1 - > "st1",
        param2 -> "st1",
        param3 -> "s1",
        param4 -> "Volume@tv-basicstudies-118",
        param5 -> {"length": 20, "col_prev_close": "false"}
    """
    return Payload(
        func="create_study",
        parameters=[chart_session_id, param1, param2, param3, param4, param5]
    ).get_payload()


def get_quote_hibernate_all(session_id):
    return Payload(
        func="quote_hibernate_all",
        parameters=[session_id]
    ).get_payload()


def get_request_more_tickmarks(chart_session_id):
    return Payload(
        func="request_more_tickmarks",
        parameters=[chart_session_id, "s1", 5]
    ).get_payload()


def get_request_more_data(chart_session_id):
    return Payload(
        func="request_more_data",
        parameters=[chart_session_id, "sds_1", 10]
    ).get_payload()
