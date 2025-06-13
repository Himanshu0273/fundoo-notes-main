from typing import List
from pydantic import BaseModel
from app.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, String, Date, ForeignKey
from datetime import date, datetime
from app.models import user_model

class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    body: Mapped[str]
    created_at: Mapped[date] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship("User", back_populates="notes")