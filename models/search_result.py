from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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

    user = relationship("User", back_populates="search_results")
