import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.notes_model import Notes
from app.utils.enums import GenderEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str]
    dob: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[GenderEnum] = mapped_column(SQLAlchemyEnum(GenderEnum))
    secret_key: Mapped[str] = mapped_column(String(100), nullable=False)
    is_verfied: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notes = relationship("Notes", back_populates="user", cascade="all, delete-orphan")

    @classmethod
    def create(cls, **kwargs):
        username = kwargs.get("username")
        if not username:
            raise ValueError("Username is required to generate a secret key")
        kwargs["secret_key"] = f"{uuid.uuid4()}{username}"
        return cls(**kwargs)
