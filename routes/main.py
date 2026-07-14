import os
import traceback
from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session

from scraper import scrape_google_maps
from scraper_utils import scrape_email_from_website
from database.session import SessionLocal
from models.search_result import SearchResult
from models.search_history import SearchHistory
from models.user import User
from dependencies.auth import get_db, get_current_active_user
from exporter import export_to_excel_buffer

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.post('/search')
def search(
    country: str = Form(""),
    city: str = Form(""),
    niche: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    country = country.strip()
    city = city.strip()
    niche = niche.strip()
    
    if not country or not city or not niche:
        return JSONResponse(status_code=400, content={"status": "error", "message": "All fields are required."})
        
    try:
        scraped_leads = scrape_google_maps(niche, city, country)
        
        if not scraped_leads:
            return JSONResponse(
                status_code=404, 
                content={
                    "status": "error", 
                    "message": "No data found for the given search criteria."
                }
            )
        
        # Parallelize website email scraping
        def process_lead(lead):
            email = ""
            contact_person = ""
            website = lead.get("website", "")
            
            social_media = False
            contact_form = False
            if website:
                email, social_media, contact_form = scrape_email_from_website(website)
                
            if email:
                prefix = email.split('@')[0].lower()
                generic_prefixes = ['info', 'contact', 'support', 'hello', 'sales', 'admin', 'team', 'office', 'enquiries', 'inquiries', 'mail']
                if prefix not in generic_prefixes:
                    if '.' in prefix:
                        contact_person = " ".join([p.capitalize() for p in prefix.split('.')])
                    else:
                        contact_person = prefix.capitalize()
            
            lead["email"] = email
            lead["contact_person"] = contact_person
            
            # AI Lead Score Calculation
            score = 0
            if website: score += 10
            if email: score += 15
            if lead.get("phone"): score += 10
            
            try:
                if float(lead.get("rating", 0) or 0) > 4.0:
                    score += 15
            except:
                pass
                
            try:
                reviews_str = str(lead.get("reviews", "")).replace(',', '')
                if reviews_str and int(reviews_str) > 100:
                    score += 10
            except:
                pass
                
            if social_media: score += 10
            if website and website.startswith("https"): score += 10
            if lead.get("google_maps_verified"): score += 10
            if contact_form: score += 10
            if lead.get("business_active"): score += 10
            
            score = min(score, 100) # Cap at 100
            
            lead["lead_score"] = score
            if score > 75:
                lead["score_color"] = "High"
            elif score >= 50:
                lead["score_color"] = "Medium"
            else:
                lead["score_color"] = "Low"
                
            return lead

        with ThreadPoolExecutor(max_workers=8) as executor:
            scraped_leads = list(executor.map(process_lead, scraped_leads))
            
        now = datetime.utcnow()
        
        try:
            # Save the search history log
            history_record = SearchHistory(
                user_id=current_user.id,
                search_params={"niche": niche, "city": city, "country": country},
                results_count=len(scraped_leads),
                created_at=now
            )
            db.add(history_record)
            
            for lead in scraped_leads:
                db_lead = SearchResult(
                    user_id=current_user.id,
                    date=now,
                    country=country,
                    city=city,
                    niche=niche,
                    niche_size=lead.get("niche_size", ""),
                    name=lead.get("name", ""),
                    rating=lead.get("rating", ""),
                    reviews=lead.get("reviews", ""),
                    price_range=lead.get("price_range", ""),
                    address=lead.get("address", ""),
                    phone=lead.get("phone", ""),
                    website=lead.get("website", ""),
                    email=lead.get("email", ""),
                    contact_person=lead.get("contact_person", ""),
                    lead_score=lead.get("lead_score", 0),
                    score_color=lead.get("score_color", "Low")
                )
                db.add(db_lead)
                
            db.commit()
        except Exception as db_err:
            db.rollback()
            print(f"Database insertion error: {db_err}")
            traceback.print_exc()
            return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to save data to database."})
        
        # Generate Excel file and save to static directory
        try:
            buffer = export_to_excel_buffer(db, current_user.id, search_date=now)
            download_url = ""
            if buffer:
                file_name = f"search_results_{current_user.id}.xlsx"
                os.makedirs("static", exist_ok=True)
                file_path = os.path.join("static", file_name)
                with open(file_path, "wb") as f:
                    f.write(buffer.getvalue())
                download_url = f"/static/{file_name}"
            else:
                print("Warning: export_to_excel_buffer returned None")
        except Exception as excel_err:
            print(f"Excel generation error: {excel_err}")
            traceback.print_exc()
            download_url = ""
        
        return JSONResponse(content={
            "status": "success",
            "message": "Search completed successfully. Your search data has been saved.",
            "download_url": download_url,
            "leads": scraped_leads
        })
        
    except Exception as e:
        print(f"Error in scraping handler: {e}")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Server Error: {str(e)}"})

@router.get('/download')
def download(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    buffer = export_to_excel_buffer(db, current_user.id)
    if buffer:
        headers = {
            'Content-Disposition': f'attachment; filename="search_results.xlsx"'
        }
        return StreamingResponse(buffer, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        return JSONResponse(status_code=404, content={"message": "Could not generate Excel file. Please try again."})

@router.get('/history')
def get_search_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        results = db.query(SearchResult).filter(SearchResult.user_id == current_user.id).order_by(SearchResult.date.desc()).all()
        history = []
        for r in results:
            history.append({
                "id": r.id,
                "date": r.date.isoformat() if r.date else None,
                "niche": r.niche,
                "city": r.city,
                "country": r.country,
                "name": r.name,
                "email": r.email,
                "phone": r.phone,
                "website": r.website,
                "lead_score": r.lead_score,
                "score_color": r.score_color
            })
        return JSONResponse(content={"status": "success", "history": history})
    except Exception as e:
        print(f"Error fetching history: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to fetch history"})
