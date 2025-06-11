from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from jose import JWTError, jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
 
from app.auth import token as token_module
from app.auth.dependencies import get_user_with_headers
from app.config.logger_config import func_logger
from app.config.settings import smtpsettings
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.emails_utils import send_verification_email
from app.utils.exceptions import (EmailAlreadyExistsException,
                                  UsernameAlreadyExistsException,
                                  UserNotFoundException)
from app.utils.hash import Hash

user_router = APIRouter(prefix="/user", tags=["Users"])
signup_router = APIRouter()


#Create User
@signup_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser, tags=['Sign-In']
)
async def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    func_logger.info("POST /signup - Create new User")
    
    try:
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
        db.flush()
        db.commit()
        db.refresh(new_user)
        
        token_obj = token_module.AccessToken(secret_key=new_user.secret_key)
        verify_token = token_obj.create_access_token(
            {"sub": new_user.username},
            expires_delta=timedelta(minutes=10)
        )
        
        BACKEND_URL=smtpsettings.BACKEND_URL
        verify_link = f"{BACKEND_URL}/user/verify-email?token={verify_token}"
        await send_verification_email(new_user.email, verify_link)

        func_logger.info(f"User created with ID: {new_user.id}")
        return new_user

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during user signup.")
        raise HTTPException(status_code=500, detail="Internal Server Error during signup")

#Verify Email
@user_router.get("/verify-email", response_class=HTMLResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        unverified_payload = jwt.decode(token, key='', options={"verify_signature": False})
        username = unverified_payload.get("sub")

        if not username:
            return HTMLResponse(content="<h2>Invalid token</h2>", status_code=400)

        user = db.query(user_model.User).filter(user_model.User.username == username).first()
        if not user:
            return HTMLResponse(content="<h2>User not found</h2>", status_code=404)

        token_obj = token_module.AccessToken(secret_key=user.secret_key)
        token_obj.verify_access_token(token, credentials_exception=HTTPException(status_code=401, detail="Invalid token"))

        if user.is_verfied:
            return HTMLResponse(content="<h2>Email already verified</h2>", status_code=200)

        user.is_verfied = True
        db.commit()

        return HTMLResponse(content="<h2>Email verified successfully!</h2>", status_code=200)

    except JWTError:
        return HTMLResponse(content="<h2>Invalid or expired token</h2>", status_code=401)

    except Exception as e:
        return HTMLResponse(content=f"<h2>Server error: {str(e)}</h2>", status_code=500)



#Update the user details
@user_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(
    id: int,
    request: user_schema.UpdateUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_user_with_headers)
):
    func_logger.info(f"PUT /user/{id} - Updating user details")

    try:
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

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during user update.")
        raise HTTPException(status_code=500, detail="Internal Server Error during user update")

#Delete the user
@user_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_user_with_headers)
):
    func_logger.info(f"DELETE /user/{id} - Deleting user")

    try:
        user = db.query(user_model.User).filter(user_model.User.id == id)
        if not user.first():
            func_logger.error(f"User not found for deletion: {id}")
            raise UserNotFoundException(user_id=id)

        user.delete(synchronize_session=False)
        db.commit()

        func_logger.info(f"User deleted successfully: {id}")
        return "User Deleted!!"

    except SQLAlchemyError as e:
        db.rollback()
        func_logger.error("❌ Database error during user deletion.")
        raise HTTPException(status_code=500, detail="Internal Server Error during user deletion")
