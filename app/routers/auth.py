from fastapi import APIRouter, status, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import user_model
from app.auth import token
from app.utils.hash import Hash

router = APIRouter(
    tags=['Auth']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session=Depends(get_db), algorithm: str = Header(default="HS256"), time_expire=Header(default=30)):
    user = db.query(user_model.User).filter(user_model.User.username == request.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!!")
    
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Password!!!")
    
    
    #Generate JWT
    # ALGORITHM = request.algorithm
    # ACCESS_TOKEN_EXPIRE_MINUTES = request.time_expire
    # tokenobj = token.AccessToken(ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, user.secret_key)
    # access_token = tokenobj.create_access_token(data={"sub": user.username})
    tokenobj = token.AccessToken(algorithm=algorithm, time_expire=time_expire, secret_key=user.secret_key)
    access_token = tokenobj.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}