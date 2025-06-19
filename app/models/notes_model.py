from datetime import datetime, timezone, timedelta
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import note_label_association

from app.models.label_model import NoteLabel
if TYPE_CHECKING:
    from app.models.user_model import User

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc)+timedelta(days=30))
    is_expired: Mapped[Boolean] = mapped_column(DateTime,default=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    labels: Mapped[List["NoteLabel"]] = relationship(
        NoteLabel, secondary=note_label_association, back_populates="notes"
    )
    user: Mapped["User"] = relationship("User", back_populates="notes")

