from datetime import datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models.user import User
from app.models.token import UserToken
from app.middlewares.auth_middleware import create_token
from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================
# Login: create access + refresh token and store in DB
# ============================================================

def login(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create tokens
    access_token = create_token(
        {"sub": user.email},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_token(
        {"sub": user.email},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Store in DB
    token_entry = UserToken(
        user_id=user.id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(token_entry)
    db.commit()
    db.refresh(token_entry)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "roles": [r.name for r in user.roles],
        },
    }


# ============================================================
# Logout: delete access token from DB
# ============================================================

def logout(access_token: str, db: Session):
    token = db.query(UserToken).filter(UserToken.access_token == access_token).first()
    if token:
        db.delete(token)
        db.commit()


# ============================================================
# Refresh: regenerate access + refresh tokens
# ============================================================

def refresh_tokens(refresh_token: str, db: Session):
    # Check token in DB
    token_record = db.query(UserToken).filter(UserToken.refresh_token == refresh_token).first()
    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # Verify JWT signature
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Get user
    user = db.query(User).filter(User.id == token_record.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Create new tokens
    new_access_token = create_token(
        {"sub": user.email},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_token(
        {"sub": user.email},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Update DB
    token_record.access_token = new_access_token
    token_record.refresh_token = new_refresh_token
    token_record.expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    db.commit()
    db.refresh(token_record)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "roles": [r.name for r in user.roles],
        },
    }
