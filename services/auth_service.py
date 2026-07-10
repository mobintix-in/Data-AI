from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.security import get_password_hash
from fastapi import HTTPException
from config.settings import settings
from utils.security import create_access_token
from datetime import timedelta
import re

class AuthService:
    @staticmethod
    def validate_password(password: str):
        if len(password) < 8 or len(password) > 64:
            raise ValueError("Password must be between 8 and 64 characters")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least 1 number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least 1 special character")
        if " " in password:
            raise ValueError("Password must not contain spaces")

    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> User:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(status_code=400, detail="User with this email already exists.")
        
        try:
            AuthService.validate_password(user_in.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        new_user = User(
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            password_hash=get_password_hash(user_in.password),
            auth_provider="local"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user

    @staticmethod
    def register_or_login_google_user(db: Session, email: str, google_id: str, first_name: str, last_name: str, profile_image: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_id=google_id,
                profile_image=profile_image,
                auth_provider="google",
                is_email_verified=True # Google users are pre-verified
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # If they registered manually before but now using Google, link account
            if user.auth_provider == "local":
                user.google_id = google_id
                user.auth_provider = "google"
                user.is_email_verified = True
                if profile_image and not user.profile_image:
                    user.profile_image = profile_image
                db.commit()
                db.refresh(user)
        return user
