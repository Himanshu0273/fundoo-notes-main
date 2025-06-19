from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import oauth
from app.config.logger_config import note_func_logger
from app.database import get_db
from app.models import label_model, notes_model
from app.models.notes_model import Notes
from app.schemas import notes_schema, user_schema
from app.utils.exceptions import (
    LabelNotOwnedException,
    NoteNotFoundException,
    NoValidLabelsProvidedException,
)
from datetime import datetime, timezone, timedelta
from app.utils.redis_client import get_cache, set_cache, r

notes_router = APIRouter(prefix="/note", tags=["Notes"])


@notes_router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(
    request: notes_schema.Notes,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    note_func_logger.info("POST /note - Create new note")

    label_objs = (
        db.query(label_model.NoteLabel)
        .filter(
            label_model.NoteLabel.label_name.in_(request.labels),
            label_model.NoteLabel.user_id == current_user.id,
        )
        .all()
    )

    if not label_objs:
        raise NoValidLabelsProvidedException()

    found_label_names = {label.label_name for label in label_objs}
    missing_labels = [l for l in request.labels if l not in found_label_names]
    if missing_labels:
        raise LabelNotOwnedException(label_names=missing_labels)

    new_note = Notes(title=request.title, body=request.body, user_id=current_user.id)
    new_note.labels = label_objs

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    note_func_logger.info("Created!!")

    return {
        "message": f"The note with id: {new_note.id} for user with id: {current_user.id} was created!!",
        "payload": new_note,
        "status": status.HTTP_201_CREATED,
    }


# Get all notes of a user
@notes_router.get("/", status_code=status.HTTP_200_OK)
def get_all_notes(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    cache_key = f"recent_notes_user_{current_user.id}"

    cached_notes = get_cache(cache_key)

    if cached_notes:
        return {
            "message": "Notes from redis cache",
            "payload": cached_notes,
            "status_code": status.HTTP_200_OK,
        }
        
    note_func_logger.info("GET /note - Retrieve all notes of a user")
    notes = (
        db.query(notes_model.Notes)
        .filter(notes_model.Notes.user_id == current_user.id)
        .all()
    )
    note_func_logger.info("Displayed!!")

    return {
        "message": f"These are all the notes of the user with user id: {current_user.id}",
        "payload": notes,
        "status": status.HTTP_200_OK,
    }


# Get specific note of a user
@notes_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_specific_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    cache_key = f"recent_notes_user_{current_user.id}"

    cached_notes = get_cache(cache_key)

    if cached_notes:
        return {
            "message": "Notes from redis cache",
            "payload": cached_notes,
            "status_code": status.HTTP_200_OK,
        }
    
    note_func_logger.info(f"GET /note - Get the note with ID: {id}")
    note = (
        db.query(notes_model.Notes)
        .filter(
            notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
        )
        .first()
    )

    if not note:
        note_func_logger.error(f"GET /note - Note with id: {id} not found")
        raise NoteNotFoundException(note_id=id)

    note_func_logger.info("Displayed")
    return {
        "message": f"The note with id: {note.id} for user with id: {current_user.id} is found!",
        "payload": note,
        "labels": [label.label_name for label in note.labels],
        "status": status.HTTP_200_OK,
    }


# Update a note
@notes_router.put("/update-note/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(
    id: int,
    request: notes_schema.UpdateNotes,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    note_func_logger.info(f"Put /note - Updated the note with ID: {id}")

    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
    )

    if not note.first():
        note_func_logger.error(f"PUT /note - Note with id: {id} not found")
        raise NoteNotFoundException(note_id=id)
    
    updated_data = request.model_dump(exclude_unset=True)
    note.update(updated_data)
    r.delete(f"note_{id}")
    r.delete(f"recent_notes_user_{current_user.id}")
    db.commit()
    note_func_logger.info("Updated!!")
    return {
        "message": f"The note with id: {note.id} for user with id: {current_user.id} was updated!!",
        "payload": note,
        "status": status.HTTP_202_ACCEPTED,
    }


# Delete a note
@notes_router.delete("/delete-note/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    note_func_logger.info(f"DELETE /note - Deleted the note with ID: {id}")
    note = db.query(notes_model.Notes).filter(
        notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
    )
    if not note.first():
        note_func_logger.error(f"DELETE /note - Note with id: {id} not found")
        raise NoteNotFoundException(note_id=id)

    r.delete(f"note_{id}")
    r.delete(f"recent_notes_user_{current_user.id}")    
    note.delete(synchronize_session=False)
    db.commit()
    note_func_logger.info("Deleted!!")
    return {
        "message": "The note with id: {note.id} for user with id: {current_user.id} was deleted!!",
        "payload": note,
        "status": status.HTTP_202_ACCEPTED,
    }


#Extend Note Validity
@notes_router.get("/extend/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def extend_note(note_id: int, db:Session=Depends(get_db)):
    note=db.query(Notes).filter(Notes.id == note_id).first()
    if not note:
        raise NoteNotFoundException
    note.expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    db.commit()
    return {"msg": "Note expiry extended by 30 days"}