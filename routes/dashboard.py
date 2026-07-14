from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta

from database.session import SessionLocal
from models.user import User
from models.search_result import SearchResult
from models.search_history import SearchHistory
from models.saved_search import SavedSearch
from models.export_history import ExportHistory
from dependencies.auth import get_current_active_user as get_current_user
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get overall statistics for the dashboard cards."""
    # This is an optimized set of queries
    total_searches = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).count()
    total_businesses = db.query(SearchResult).filter(SearchResult.user_id == current_user.id).count()
    saved_searches = db.query(SavedSearch).filter(SavedSearch.user_id == current_user.id).count()
    exports = db.query(ExportHistory).filter(ExportHistory.user_id == current_user.id).count()
    
    # Calculate some averages and totals
    avg_lead_score_query = db.query(func.avg(SearchResult.lead_score)).filter(SearchResult.user_id == current_user.id).scalar()
    avg_lead_score = round(avg_lead_score_query, 1) if avg_lead_score_query else 0

    verified_emails = db.query(SearchResult).filter(SearchResult.user_id == current_user.id, SearchResult.email != None, SearchResult.email != "").count()
    verified_phones = db.query(SearchResult).filter(SearchResult.user_id == current_user.id, SearchResult.phone != None, SearchResult.phone != "").count()

    today = datetime.utcnow().date()
    todays_searches = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id,
        func.date(SearchHistory.created_at) == today
    ).count()

    return {
        "today_searches": todays_searches,
        "total_searches": total_searches,
        "total_businesses": total_businesses,
        "saved_leads": total_businesses, # Assuming all scraped results are leads for now
        "avg_lead_score": avg_lead_score,
        "verified_emails": verified_emails,
        "verified_phones": verified_phones,
        "exports": exports
    }

@router.get("/recent-searches")
def get_recent_searches(limit: int = 5, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    searches = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).order_by(SearchHistory.created_at.desc()).limit(limit).all()
    return searches

@router.get("/activity")
def get_activity_chart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get activity data for the last 7 days."""
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)
    
    results = db.query(
        func.date(SearchHistory.created_at).label('date'),
        func.count(SearchHistory.id).label('searches')
    ).filter(
        SearchHistory.user_id == current_user.id,
        func.date(SearchHistory.created_at) >= start_date
    ).group_by(func.date(SearchHistory.created_at)).all()
    
    data_dict = {str(r.date): r.searches for r in results}
    
    chart_data = []
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_str = str(current_date)
        chart_data.append({
            "name": current_date.strftime("%a"),
            "searches": data_dict.get(date_str, 0)
        })
        
    return chart_data
