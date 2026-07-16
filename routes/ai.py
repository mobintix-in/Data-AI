import os
from google import genai
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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

@router.post("/generate-summary/{lead_id}")
def generate_summary(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured on server.")

    lead = db.query(SearchResult).filter(SearchResult.id == lead_id, SearchResult.user_id == current_user.id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
        Act as a B2B sales expert. Write a short, professional 2-3 sentence summary about this business lead.
        Highlight why they might be a good prospect based on this info:
        Name: {lead.name}
        Category: {lead.category}
        Rating: {lead.rating} from {lead.reviews} reviews
        City: {lead.city}, {lead.country}
        Has Website: {'Yes' if lead.website else 'No'}
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        summary = response.text
        
        lead.ai_summary = summary
        db.commit()
        db.refresh(lead)
        
        return {"status": "success", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")
