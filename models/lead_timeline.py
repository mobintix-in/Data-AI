from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.session import Base

class LeadTimeline(Base):
    __tablename__ = "lead_timelines"

    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey("search_results.id"), nullable=False)
    status = Column(String, nullable=False) # e.g., 'Contacted', 'Meeting'
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    search_result = relationship("SearchResult", back_populates="timelines")
