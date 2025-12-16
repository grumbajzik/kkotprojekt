from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from Auth.jwt import decode_jwt
from Auth.security import oauth2_scheme
from Entities import User
from database import SessionLocal, get_db
from jose import jwt, JWTError

SECRET_KEY = "tajny_klic"
ALGORITHM = "HS256"


def get_current_user(auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> User:
    token = auth.credentials
    try:
        payload = decode_jwt(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def is_admin(user: User):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


def approver_only(user: User):
    if not user.is_approver:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only equipment managers can perform this action"
        )
def enable_only(user: User):
    if not user.is_approver or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only equipment managers and admins can perform this action"
        )


def can_modify_user(current_user: User, target_user_id: int):
    if current_user.is_admin:
        return
    if current_user.id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this user"
        )
