from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.database import get_db
from datetime import datetime
from app.models import user_model
from app.utils.redis_client import r
from app.utils.exceptions import TooManyRequestsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def rate_limit_user(user_id: int, limit: int = 10, window: int = 60):
    current_window = int(datetime.now().timestamp() // window)
    redis_key = f"rate_limit:user:{user_id}:{current_window}"

    current = r.incr(redis_key)
    if current == 1:
        r.expire(redis_key, window)

    if current > limit:
        raise TooManyRequestsException

async def get_current_user(
    token_data: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    algorithm: str = Header(default="HS256"),
    time_expire: int = Header(default=30),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        unverified_payload = jwt.decode(
            token_data, key="", options={"verify_signature": False}
        )
        username = unverified_payload.get("sub")
        if not username:
            raise credentials_exception

        user = (
            db.query(user_model.User)
            .filter(user_model.User.username == username)
            .first()
        )
        if not user:
            raise credentials_exception

        tokenobj = AccessToken(
            user.secret_key, algorithm=algorithm, time_expire=time_expire
        )
        tokenobj.verify_access_token(token_data, credentials_exception)

        await rate_limit_user(user.id)
        
        return user

    except JWTError:
        raise credentials_exception
