from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import notes_model
from app.schemas import notes_schema
from typing import List
from app.auth import oauth
from app.utils.exceptions import NoteNotFoundException

notes_router = APIRouter(prefix='/note', tags=['Notes'])

#Create a note
@notes_router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(request: notes_schema.Notes, db: Session=Depends(get_db), current_user: notes_schema.Notes=Depends(oauth.get_current_user)):
    new_note = notes_model.Notes(title=request.title, body=request.body, user_id = current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

#Get all notes of a user
@notes_router.get('/', response_model=List[notes_schema.ShowNote], status_code=status.HTTP_200_OK)
def get_all_notes(db:Session=Depends(get_db), current_user: notes_schema.Notes=Depends(oauth.get_current_user)):
    notes = db.query(notes_model.Notes).all()
    return notes

#Get specific note of a user
@notes_router.get('/{id}', status_code=status.HTTP_200_OK)
def get_specific_note(id: int, db:Session = Depends(get_db), current_user: notes_schema.Notes=Depends(oauth.get_current_user)):
    note = db.query(notes_model.Notes).filter(notes_model.Notes.id == id).first()
    
    if not note:
        raise NoteNotFoundException(note_id=id)
        
    return note


#Update a note
@notes_router.put('/update-note/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_note(id: int,request: notes_schema.UpdateNotes, db: Session=Depends(get_db), current_user: notes_schema.Notes=Depends(oauth.get_current_user)):
    note = db.query(notes_model.Notes).filter(notes_model.Notes.id==id)
    
    if not note.first():
        raise NoteNotFoundException(note_id=id)
    
    updated_data = request.model_dump(exclude_unset=True)
    note.update(updated_data)
    db.commit()
    return 'Note Updated!!!'


#Delete a note
@notes_router.delete('/delete-note/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_note(id: int, db: Session=Depends(get_db), current_user: notes_schema.Notes=Depends(oauth.get_current_user)):
    note = db.query(notes_model.Notes).filter(notes_model.Notes.id == id)
    if not note.first():
        raise NoteNotFoundException(note_id=id)
        
    note.delete(synchronize_session=False)
    db.commit()
    return 'Note Deleted!!!'