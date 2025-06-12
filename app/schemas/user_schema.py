from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.utils.enums import GenderEnum


class User(BaseModel):
    username: str
    email: str
    password: str
    dob: date
    gender: GenderEnum

    model_config = ConfigDict(from_attributes=True)


class ShowUser(BaseModel):
    username: str
    email: str
    dob: date
    gender: GenderEnum


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
