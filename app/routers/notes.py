from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import oauth
from app.database import get_db
from app.models import notes_model
from app.schemas import notes_schema, user_schema
from app.utils.exceptions import NoteNotFoundException
from app.config.logger_config import note_func_logger

notes_router = APIRouter(prefix="/note", tags=["Notes"])


# Create a note
@notes_router.post("/", status_code=status.HTTP_201_CREATED)
def create_note(
    request: notes_schema.Notes,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth.get_current_user),
):
    note_func_logger.info("POST /note - Create new note")
    new_note = notes_model.Notes(
        title=request.title, body=request.body, user_id=current_user.id
    )
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

    note.delete(synchronize_session=False)
    db.commit()
    note_func_logger.info("Deleted!!")
    return {
        "message": "The note with id: {note.id} for user with id: {current_user.id} was deleted!!",
        "payload": note,
        "status": status.HTTP_202_ACCEPTED,
    }
