from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from database.session import SessionLocal
from models.user import User
from models.saved_search import SavedSearch
from dependencies.auth import get_current_active_user as get_current_user
from schemas.saas import SavedSearchCreate, SavedSearchResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[SavedSearchResponse])
def get_saved_searches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    searches = db.query(SavedSearch).filter(SavedSearch.user_id == current_user.id)\
        .order_by(desc(SavedSearch.created_at)).all()
    return searches

@router.post("", response_model=SavedSearchResponse)
def create_saved_search(
    saved_search: SavedSearchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    search = SavedSearch(
        user_id=current_user.id,
        name=saved_search.name,
        filters=saved_search.filters
    )
    db.add(search)
    db.commit()
    db.refresh(search)
    return search

@router.delete("/{search_id}")
def delete_saved_search(
    search_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    search = db.query(SavedSearch).filter(SavedSearch.id == search_id, SavedSearch.user_id == current_user.id).first()
    if not search:
        raise HTTPException(status_code=404, detail="Saved search not found")
        
    db.delete(search)
    db.commit()
    return {"status": "success"}
