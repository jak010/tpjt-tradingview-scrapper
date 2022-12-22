from __future__ import annotations
from typing import TypedDict


class TimeScaleUpdateDict(TypedDict):
    m: str
    p: list
    t: int
    t_ms: int


class TimeScaleUpdateParmeter2(TypedDict):
    s: dict

