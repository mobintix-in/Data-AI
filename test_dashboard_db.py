import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.session import SessionLocal
from models.user import User
from models.search_result import SearchResult
from models.search_history import SearchHistory
from models.saved_search import SavedSearch
from models.export_history import ExportHistory
from sqlalchemy import func
from datetime import datetime

db = SessionLocal()
try:
    user = db.query(User).first()
    if not user:
        print("No user found")
        sys.exit(0)
    
    current_user = user
    print(f"Testing for user {current_user.id}")

    total_searches = db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).count()
    print(f"total_searches: {total_searches}")
    
    total_businesses = db.query(SearchResult).filter(SearchResult.user_id == current_user.id).count()
    print(f"total_businesses: {total_businesses}")
    
    saved_searches = db.query(SavedSearch).filter(SavedSearch.user_id == current_user.id).count()
    print(f"saved_searches: {saved_searches}")
    
    exports = db.query(ExportHistory).filter(ExportHistory.user_id == current_user.id).count()
    print(f"exports: {exports}")
    
    avg_lead_score_query = db.query(func.avg(SearchResult.lead_score)).filter(SearchResult.user_id == current_user.id).scalar()
    avg_lead_score = round(avg_lead_score_query, 1) if avg_lead_score_query else 0
    print(f"avg_lead_score: {avg_lead_score}")

    verified_emails = db.query(SearchResult).filter(SearchResult.user_id == current_user.id, SearchResult.email != None, SearchResult.email != "").count()
    print(f"verified_emails: {verified_emails}")

    verified_phones = db.query(SearchResult).filter(SearchResult.user_id == current_user.id, SearchResult.phone != None, SearchResult.phone != "").count()
    print(f"verified_phones: {verified_phones}")

    today = datetime.utcnow().date()
    todays_searches = db.query(SearchHistory).filter(
        SearchHistory.user_id == current_user.id,
        func.date(SearchHistory.created_at) == today
    ).count()
    print(f"todays_searches: {todays_searches}")

    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
