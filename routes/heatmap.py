from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.session import SessionLocal
from models.user import User
from models.search_result import SearchResult
from dependencies.auth import get_current_active_user as get_current_user
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_heatmap_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all leads that have valid coordinates for the heatmap."""
    leads = db.query(SearchResult.id, SearchResult.name, SearchResult.latitude, SearchResult.longitude, SearchResult.category)\
        .filter(
            SearchResult.user_id == current_user.id,
            SearchResult.latitude != None,
            SearchResult.longitude != None,
            SearchResult.latitude != "",
            SearchResult.longitude != ""
        ).all()
    
    data = []
    for lead in leads:
        try:
            data.append({
                "id": lead.id,
                "name": lead.name,
                "lat": float(lead.latitude),
                "lng": float(lead.longitude),
                "category": lead.category
            })
        except ValueError:
            pass # Skip invalid floats
            
    return {"status": "success", "data": data}
