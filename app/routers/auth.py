from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import token
from app.database import get_db
from app.models import user_model
from app.utils.exceptions import InvalidCredentialsException
from app.utils.hash import Hash
from app.config.logger_config import func_logger

auth_router = APIRouter(
    tags=['Auth']
)

@auth_router.post('/login')
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session=Depends(get_db), algorithm: str = Header(default="HS256"), time_expire=Header(default=30)):
    func_logger.info(f"POST /login - Authenticating user")
    
    user = db.query(user_model.User).filter(user_model.User.username == request.username).first()
    if not user:
        func_logger.error(f"The username entered is invalid: {request.username}")
        raise InvalidCredentialsException()
    
    if not Hash.verify_password(request.password, user.password):
        func_logger.error(f"The password entered is invalid: {request.password}")
        raise InvalidCredentialsException()
    
    tokenobj = token.AccessToken(algorithm=algorithm, time_expire=time_expire, secret_key=user.secret_key)
    access_token = tokenobj.create_access_token(data={"sub": user.username})
    func_logger.info(f"User authenticated successfully!!")
    return {"access_token": access_token, "token_type": "bearer"}