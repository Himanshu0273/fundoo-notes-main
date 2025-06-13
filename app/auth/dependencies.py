from fastapi import Depends, Header, HTTPException, status

from app.auth.oauth import get_current_user


def get_user_with_headers(
    algorithm: str = Header(default="HS256"),
    time_expire: int = Header(default=30),
    current_user=Depends(get_current_user),
):
    return current_user
