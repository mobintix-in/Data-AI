from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

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
    lead_score = Column(Integer, default=0)
    score_color = Column(String, default="Low")

    has_facebook = Column(Boolean, default=False)
    has_instagram = Column(Boolean, default=False)
    has_linkedin = Column(Boolean, default=False)
    has_twitter = Column(Boolean, default=False)
    has_youtube = Column(Boolean, default=False)
    has_whatsapp = Column(Boolean, default=False)

    lead_status = Column(String, default="New") # New, Contacted, Follow Up, Meeting, Negotiation, Converted, Rejected
    ai_summary = Column(String, nullable=True)
    latitude = Column(String, nullable=True) # changed to String or Float depending on what scraper provides, but String is safer
    longitude = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="search_results")
    timelines = relationship("LeadTimeline", back_populates="search_result", cascade="all, delete")
    notes = relationship("Note", back_populates="search_result", cascade="all, delete")
    reminders = relationship("Reminder", back_populates="search_result", cascade="all, delete")
