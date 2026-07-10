from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    search_results = relationship("SearchResult", back_populates="user")

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    country = Column(String)
    city = Column(String)
    niche = Column(String)
    name = Column(String)
    address = Column(String)
    website = Column(String)
    email = Column(String)
    phone = Column(String)
    rating = Column(String)
    reviews = Column(String)
    category = Column(String)
    niche_size = Column(String)
    price_range = Column(String)
    contact_person = Column(String)

    user = relationship("User", back_populates="search_results")
