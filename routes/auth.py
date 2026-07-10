from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

from config.settings import settings
from database.session import SessionLocal
from dependencies.auth import get_db, get_current_active_user, get_current_user
from models.user import User
from schemas.user import UserCreate, User as UserSchema, GoogleLogin
from schemas.token import Token, TokenPayload, ForgotPassword, PasswordReset
from services.auth_service import AuthService
from utils.security import verify_password, create_access_token, create_refresh_token, get_password_hash
from utils.email import send_mock_email
from jose import jwt, JWTError

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register a new user."""
    user = AuthService.register_user(db, user_in)
    
    # Send verification email
    verify_token = create_access_token(subject=user.email, expires_delta=timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS))
    verify_link = f"http://localhost:3000/verify-email?token={verify_token}"
    send_mock_email(user.email, "Verify your email", f"Please verify your email by clicking: {verify_link}")
    
    return user

@router.post("/login", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.password_hash or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id, expires_delta=refresh_token_expires),
        "token_type": "bearer",
    }

@router.post("/google", response_model=Token)
def login_google(google_login: GoogleLogin, db: Session = Depends(get_db)) -> Any:
    """Login with Google OAuth2 ID Token."""
    try:
        # Note: In production you should pass your CLIENT_ID to verify it
        idinfo = id_token.verify_oauth2_token(google_login.token, requests.Request())
        email = idinfo['email']
        google_id = idinfo['sub']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        profile_image = idinfo.get('picture', '')
        
        user = AuthService.register_or_login_google_user(db, email, google_id, first_name, last_name, profile_image)
        
        user.last_login = datetime.utcnow()
        db.commit()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return {
            "access_token": create_access_token(user.id, expires_delta=access_token_expires),
            "refresh_token": create_refresh_token(user.id, expires_delta=refresh_token_expires),
            "token_type": "bearer",
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")

@router.post("/logout")
def logout() -> Any:
    """
    Logout route. 
    In JWT, logout is usually handled on the client by deleting the token.
    To fully invalidate a JWT server-side, you'd need a token blacklist/redis cache.
    """
    return {"msg": "Successfully logged out. Please remove token on client side."}

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_active_user)) -> Any:
    """Get current user."""
    return current_user

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)) -> Any:
    """Refresh access token."""
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    
    user = db.query(User).filter(User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": refresh_token, # Keep the same refresh token
        "token_type": "bearer",
    }

@router.post("/forgot-password")
def forgot_password(req: ForgotPassword, db: Session = Depends(get_db)) -> Any:
    """Password Recovery."""
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        reset_token = create_access_token(subject=user.email, expires_delta=timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS))
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        send_mock_email(user.email, "Password Reset Request", f"Reset your password here: {reset_link}")
    return {"msg": "If your email is registered, you will receive a password recovery link."}

@router.post("/reset-password")
def reset_password(req: PasswordReset, db: Session = Depends(get_db)) -> Any:
    """Reset password."""
    try:
        payload = jwt.decode(req.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="The user with this email does not exist in the system.")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    try:
        AuthService.validate_password(req.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    user.password_hash = get_password_hash(req.new_password)
    db.commit()
    return {"msg": "Password updated successfully"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)) -> Any:
    """Verify email."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_email_verified = True
    db.commit()
    return {"msg": "Email successfully verified"}
