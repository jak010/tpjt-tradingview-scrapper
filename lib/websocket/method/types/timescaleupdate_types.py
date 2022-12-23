from __future__ import annotations
from typing import TypedDict
from dataclasses import dataclass

from datetime import datetime


class TimeScaleUpdateDict(TypedDict):
    m: str
    p: list
    t: int
    t_ms: int


class TimeScaleUpdateParmeter2(TypedDict):
    s: dict


@dataclass(order=True)
class TimeScaleUpdateTickData:
    date_time: float

    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_humanize(self) -> datetime:
        return datetime.fromtimestamp(self.date_time)
