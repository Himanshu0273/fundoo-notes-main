from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.user_schema  import ShowUser
from typing import Optional

class Notes(BaseModel):
    title: str
    body: str
    model_config = ConfigDict(from_attributes=True)
    
class ShowNote(BaseModel):
    id: int 
    title: str
    body: str
    created_at: date
    user: ShowUser
    
    model_config = ConfigDict(from_attributes=True)
    
class UpdateNotes(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    model_config=ConfigDict(from_attributes=True)