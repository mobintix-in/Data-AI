import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.session import SessionLocal
from models.user import User
from models.search_history import SearchHistory
from sqlalchemy import func
from datetime import datetime, timedelta

db = SessionLocal()
try:
    user = db.query(User).first()
    if not user:
        print("No user found")
        sys.exit(0)
    
    current_user = user
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
    print(chart_data)

except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
