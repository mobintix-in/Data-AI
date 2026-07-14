from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from database.session import SessionLocal
from models.user import User
from models.search_history import SearchHistory
from dependencies.auth import get_current_active_user as get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def get_search_history(
    limit: int = 50,
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id)\
        .order_by(desc(SearchHistory.created_at)).offset(skip).limit(limit).all()
    
    total = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).count()
    
    items = []
    for h in history:
        items.append({
            "id": h.id,
            "user_id": h.user_id,
            "search_params": h.search_params,
            "results_count": h.results_count,
            "created_at": h.created_at.isoformat() if h.created_at else None
        })
    
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "skip": skip
    }

@router.delete("/{history_id}")
def delete_search_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = db.query(SearchHistory).filter(SearchHistory.id == history_id, SearchHistory.user_id == current_user.id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Search history not found")
        
    db.delete(history)
    db.commit()
    return {"status": "success"}
