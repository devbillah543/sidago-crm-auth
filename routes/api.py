# app/routes/api.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.token import UserToken
from app.controllers.auth_controller import login, logout, refresh_tokens
from app.schemas.auth_schema import LoginRequest
from app.middlewares.auth_middleware import get_current_user, require_role

router = APIRouter()

# ---------------- Database dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- LOGIN ----------------
@router.post("/login", summary="Login user")
def user_login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user with email & password
    Returns access token, refresh token, and user info
    """
    return login(request.email, request.password, db)


# ---------------- LOGOUT ----------------
@router.post("/logout", summary="Logout user")
def user_logout(
    user: User = Depends(get_current_user),  # Access token validated
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


@router.post("/refresh", summary="Refresh access & refresh tokens")
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    """
    Generate new access and refresh tokens using a valid refresh token
    Returns new tokens and user info
    """
    return refresh_tokens(request.refresh_token, db)


# ---------------- GET CURRENT USER ----------------
@router.get("/me", summary="Get current user info")
def get_me(user: User = Depends(get_current_user)):
    """
    Get details of the currently logged-in user
    """
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "roles": [r.name for r in user.roles],
    }


# ---------------- GET AGENT LIST ----------------
@router.get("/agents", summary="Get all agents (admin only)")
def get_agents(
    admin_user: User = Depends(require_role("admin")),  # Only admin can access
    db: Session = Depends(get_db)
):
    """
    Returns a list of all users who have the 'agent' role.
    Accessible only by users with 'admin' role.
    """
    agents = (
        db.query(User)
        .join(User.roles)
        .filter(Role.name == "agent")
        .all()
    )

    return [
        {
            "id": agent.id,
            "email": agent.email,
            "username": agent.username,
            "roles": [role.name for role in agent.roles]
        }
        for agent in agents
    ]
