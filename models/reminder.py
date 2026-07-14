from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey("search_results.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reminder_date = Column(DateTime, nullable=False)
    priority = Column(String, default="Medium") # Low, Medium, High
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    search_result = relationship("SearchResult", back_populates="reminders")
    user = relationship("User", back_populates="reminders")
