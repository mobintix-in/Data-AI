from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List, Optional

from database.session import SessionLocal
from models.user import User
from models.search_result import SearchResult
from models.lead_timeline import LeadTimeline
from dependencies.auth import get_current_active_user as get_current_user
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_leads(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    lead_status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_desc: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get paginated and filtered business leads."""
    query = db.query(SearchResult).filter(SearchResult.user_id == current_user.id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                SearchResult.name.ilike(search_filter),
                SearchResult.email.ilike(search_filter),
                SearchResult.phone.ilike(search_filter),
                SearchResult.category.ilike(search_filter),
                SearchResult.city.ilike(search_filter),
            )
        )
    
    if lead_status:
        query = query.filter(SearchResult.lead_status == lead_status)

    # Sorting
    if hasattr(SearchResult, sort_by):
        order_col = getattr(SearchResult, sort_by)
        if sort_desc:
            query = query.order_by(desc(order_col))
        else:
            query = query.order_by(order_col)
    
    total = query.count()
    leads = query.offset(skip).limit(limit).all()

    return {
        "items": leads,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.put("/{lead_id}/status")
def update_lead_status(
    lead_id: int,
    status: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update lead status and add to timeline."""
    lead = db.query(SearchResult).filter(SearchResult.id == lead_id, SearchResult.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead.lead_status = status
    
    # Add timeline entry
    timeline_entry = LeadTimeline(
        search_result_id=lead.id,
        status=status,
        notes=notes
    )
    db.add(timeline_entry)
    db.commit()
    db.refresh(lead)
    
    return lead

@router.get("/{lead_id}/timeline")
def get_lead_timeline(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the timeline for a specific lead."""
    lead = db.query(SearchResult).filter(SearchResult.id == lead_id, SearchResult.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return [
        {
            "id": t.id,
            "status": t.status,
            "notes": t.notes,
            "created_at": t.created_at
        }
        for t in lead.timelines
    ]
