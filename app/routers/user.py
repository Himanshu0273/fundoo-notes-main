from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.hash import Hash
from app.auth.dependencies import get_user_with_headers
router = APIRouter(prefix="/user", tags=["Users"])


# Get user according to id
@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser
)
def get_user(id: int, db: Session = Depends(get_db), current_user=Depends(get_user_with_headers)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available."
        )
    return user


# Add user
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser
)
def create_user(request: user_schema.User, db: Session = Depends(get_db), create_user=Depends(get_user_with_headers)):
    user_data = request.model_dump()
    user_data["password"] = Hash.get_password_hash(request.password)
    new_user = user_model.User.create(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Update user details
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(
    id: int, request: user_schema.UpdateUser, db: Session = Depends(get_db), create_user=Depends(get_user_with_headers)):
    user = db.query(user_model.User).filter(user_model.User.id == id)

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available."
        )

    update_data = request.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = Hash.get_password_hash(update_data["password"])

    user.update(update_data)
    db.commit()
    return "User Details updated!!"


# Delete a user
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db), create_user=Depends(get_user_with_headers)):
    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not available."
        )

    user.delete(synchronize_session=False)
    db.commit()
    return "User Deleted!!"
