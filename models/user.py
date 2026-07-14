from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database.session import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True) # nullable for google login users
    auth_provider = Column(String, default="local") # local or google
    google_id = Column(String, unique=True, index=True, nullable=True)
    profile_image = Column(String, nullable=True)
    role = Column(String, default="User") # Admin, User, Premium User
    subscription_plan = Column(String, default="free")
    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    gemini_api_key = Column(String, nullable=True)

    # Relationships
    search_results = relationship("SearchResult", back_populates="user", cascade="all, delete")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete")
    saved_searches = relationship("SavedSearch", back_populates="user", cascade="all, delete")
    notes = relationship("Note", back_populates="user", cascade="all, delete")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete")
    export_history = relationship("ExportHistory", back_populates="user", cascade="all, delete")
    system_logs = relationship("SystemLog", back_populates="user", cascade="all, delete")
