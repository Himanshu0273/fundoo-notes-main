from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

note_label_association = Table(
    "note_label_association",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)
