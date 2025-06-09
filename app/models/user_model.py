import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from ..utils.enums import GenderEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]   
    email: Mapped[str]
    password: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[GenderEnum] = mapped_column(SQLAlchemyEnum(GenderEnum))
    secret_key: Mapped[str] = mapped_column(String(100), nullable=False)
    
    @classmethod
    def create(cls, **kwargs):
        username = kwargs.get("username")
        if not username:
            raise ValueError("Username is required to generate a secret key")
        kwargs["secret_key"] = f"{uuid.uuid4()}{username}"
        return cls(**kwargs)
