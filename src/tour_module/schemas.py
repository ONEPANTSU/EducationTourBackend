from datetime import datetime
from typing import List

from loguru import logger
from pydantic import BaseModel


class TourCreate(BaseModel):
    name: str
    city: str
    description: str
    date_start: datetime
    date_end: datetime
    reg_deadline: datetime
    max_users: int
    events: List[int]

    @logger.catch
    def fix_time(self) -> None:
        self.date_start = self.date_start.replace(tzinfo=None)
        self.date_end = self.date_end.replace(tzinfo=None)
        self.reg_deadline = self.reg_deadline.replace(tzinfo=None)


class TourRead(BaseModel):
    id: int
    name: str
    city: str
    description: str
    date_start: datetime
    date_end: datetime
    reg_deadline: datetime
    max_users: int
    events: List[int]


class TourUpdate(BaseModel):
    id: int
    name: str
    city: str
    description: str
    date_start: datetime
    date_end: datetime
    reg_deadline: datetime
    max_users: int
    events: List[int]

    @logger.catch
    def fix_time(self) -> None:
        self.date_start = self.date_start.replace(tzinfo=None)
        self.date_end = self.date_end.replace(tzinfo=None)
        self.reg_deadline = self.reg_deadline.replace(tzinfo=None)