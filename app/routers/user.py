from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_user_with_headers
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.exceptions import (EmailAlreadyExistsException,
                                  UsernameAlreadyExistsException,
                                  UserNotFoundException)
from app.utils.hash import Hash
from app.config.logger_config import func_logger

user_router = APIRouter(prefix="/user", tags=["Users"])
signup_router = APIRouter()

# func_logger = logger_obj.bind(func=True)

# Add User
@signup_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser,tags=['Sign-In']
)
def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    func_logger.info("POST /signup - Create new User")
    
    existing_email = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if existing_email:
        func_logger.error(f"Email already exists: {request.email}!!")
        raise EmailAlreadyExistsException(email=request.email)
    
    existing_username = db.query(user_model.User).filter(user_model.User.username == request.username).first()
    if existing_username:
        func_logger.error(f"Username already exists: {request.username}")
        raise UsernameAlreadyExistsException(username=request.username)
    
    user_data = request.model_dump()
    user_data["password"] = Hash.get_password_hash(request.password)
    new_user = user_model.User.create(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    func_logger.info(f"User created with ID: {new_user.id}")
    return new_user


# Get user by id
@user_router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser
)
def get_user(id: int, db: Session = Depends(get_db), current_user=Depends(get_user_with_headers)):
    func_logger.info(f"GET /user/{id}- Fetching user")
    
    user = db.query(user_model.User).filter(user_model.User.id == id).first()

    if not user:
        func_logger.error(f"User not found: {id}")
        raise UserNotFoundException(user_id=id)
    
    func_logger.info(f"User returned: {id}")
    return user


# Update user details
@user_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(
    id: int, request: user_schema.UpdateUser, db: Session = Depends(get_db), create_user=Depends(get_user_with_headers)):
    func_logger.info(f"PUT /user/{id} - Updating user details")
    user = db.query(user_model.User).filter(user_model.User.id == id)

    if not user.first():
        func_logger.error(f"User not found for update: {id}")
        raise UserNotFoundException(user_id=id)

    update_data = request.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = Hash.get_password_hash(update_data["password"])

    user.update(update_data)
    db.commit()
    func_logger.info(f"User updated successfully: {id}")
    return "User Details updated!!"


# Delete a user
@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db), create_user=Depends(get_user_with_headers)):
    func_logger.info(f"DELETE /user/{id} - Deleting user")

    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        func_logger.error(f"User not found for update: {id}")
        raise UserNotFoundException(user_id=id)

    user.delete(synchronize_session=False)
    db.commit()
    func_logger.info(f"User deleted successfully: {id}") 
    return "User Deleted!!"
