from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import SessionLocal
from app.controllers.auth_controller import login, logout, refresh_tokens
from app.schemas.auth_schema import LoginRequest
from app.middlewares.auth_middleware import get_current_user
from app.models.token import UserToken

router = APIRouter()

# ---------------- Database dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- LOGIN ----------------
@router.post("/login")
def user_login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user with email & password
    """
    return login(request.email, request.password, db)


# ---------------- LOGOUT ----------------
@router.post("/logout")
def user_logout(
    user=Depends(get_current_user),  # ✅ Access token is validated here
    db: Session = Depends(get_db)
):
    """
    Logout user by invalidating their access token
    """
    token_record = db.query(UserToken).filter(UserToken.user_id == user.id).first()
    if token_record:
        db.delete(token_record)
        db.commit()

    return {"message": "Logged out successfully"}


# ---------------- REFRESH TOKEN ----------------
class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """
    Refresh access & refresh tokens using a valid refresh token
    """
    return refresh_tokens(request.refresh_token, db)


# ---------------- GET CURRENT USER ----------------
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    """
    Get the current logged-in user's info
    """
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "roles": [r.name for r in user.roles],
    }
