from datetime import date, datetime

from sqlalchemy import Date, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..enums import GenderEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]   
    email: Mapped[str]
    password: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[GenderEnum] = mapped_column(SQLAlchemyEnum(GenderEnum))
