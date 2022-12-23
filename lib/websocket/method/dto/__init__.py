from __future__ import annotations
from ..types.timescaleupdate_types import TimeScaleUpdateDict

from typing import Union, Dict, Optional

from datetime import datetime


class TimeScaleUpdateMessageDto:
    def __init__(self, recv_msg):
        self.recv_msg: TimeScaleUpdateDict = recv_msg

    @property
    def m(self) -> str:
        return self.recv_msg.get('m', None)

    @property
    def p(self) -> Union[TiemScaleUpdateMessageParamterData, list]:
        parameter = self.recv_msg.get("p", None)
        return TiemScaleUpdateMessageParamterData(parameter) if parameter is not None else list()

    @property
    def t(self) -> int:
        return self.recv_msg.get('t', None)

    @property
    def t_ms(self) -> int:
        return self.recv_msg.get('t_ms', None)

    def __str__(self):
        return f"{self.__class__.__name__}(t: {datetime.fromtimestamp(self.t)}, t_ms:{self.t_ms})"


class TiemScaleUpdateMessageParamterData:
    def __init__(self, tiemscaleupdate_message_paramter: list):
        self.tiemscaleupdate_message_paramter = tiemscaleupdate_message_paramter

    @property
    def chart_session_id(self) -> str:
        return self.tiemscaleupdate_message_paramter[0]

    @property
    def position2(self) -> dict:
        return self.tiemscaleupdate_message_paramter[1]

    @property
    def position2_of_key_in_s1(self) -> dict:
        return self.tiemscaleupdate_message_paramter[1].get('s1', None)

    @property
    def position2_of_key_in_s1_in_node(self) -> dict:
        return self.position2_of_key_in_s1.get('node', None)

    @property
    def position2_of_key_in_s1_in_s(self) -> dict[int, list]:
        """ 과거 OHCL 데이터가 포함되있는 것으로보임(`22.12.22)
        Eg. {'i': 0, 'v': [1635454800.0, 1.1677899999999999, 1.16902, 1.1535199999999999, 1.15611, 224123.0]}
        """
        return self.position2_of_key_in_s1.get('s', None)

    @property
    def position2_of_key_in_s1_in_ns(self) -> dict:
        return self.position2_of_key_in_s1.get('ns', None)

    @property
    def position2_of_key_in_s1_in_t(self) -> dict:
        return self.position2_of_key_in_s1.get('t', None)

    @property
    def position2_of_key_in_s1_in_lbs(self) -> dict:
        return self.position2_of_key_in_s1.get('lbs', None)

    @property
    def position3(self) -> dict:
        return self.tiemscaleupdate_message_paramter[2]

    @property
    def position3_of_key_name_in_index(self) -> int:
        return self.tiemscaleupdate_message_paramter[2].get("index", None)

    @property
    def position3_of_key_name_in_zoffset(self) -> int:
        return self.tiemscaleupdate_message_paramter[2].get("zoffset", None)

    @property
    def position3_of_key_name_in_changes(self) -> list:
        return self.tiemscaleupdate_message_paramter[2].get("changes", None)

    @property
    def position3_of_key_name_in_marks(self) -> list[list]:
        return self.tiemscaleupdate_message_paramter[2].get("marks", None)

    @property
    def position3_of_key_name_in_indexdiff(self) -> list:
        return self.tiemscaleupdate_message_paramter[2].get("indexdiff", None)
