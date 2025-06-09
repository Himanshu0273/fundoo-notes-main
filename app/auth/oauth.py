from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.database import get_db
from app.models import user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token_data: str = Depends(oauth2_scheme), 
    db: Session=Depends(get_db),
    algorithm: str = Header(default="HS256"),
    time_expire: int = Header(default=30)
):
    
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the user",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    
    try:
        unverified_payload = jwt.decode(token_data,key='', options={"verify_signature": False})
        username = unverified_payload.get("sub")
        if not username:
            raise credentials_exception
        
        user = db.query(user_model.User).filter(user_model.User.username==username).first()
        if not user:
            raise credentials_exception
        
        tokenobj = AccessToken(algorithm=algorithm, time_expire=time_expire, secret_key=user.secret_key)
        return tokenobj.verify_access_token(token_data, credentials_exception)
        
    except JWTError:
        raise credentials_exception