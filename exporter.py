import io
import pandas as pd
from sqlalchemy.orm import Session
from db.models import SearchResult

import traceback

def export_to_excel_buffer(db: Session, user_id: int, search_date=None):
    """Compiles database results for a specific user into Excel buffer using pandas."""
    try:
        query = db.query(
            SearchResult.date,
            SearchResult.country,
            SearchResult.city,
            SearchResult.niche,
            SearchResult.niche_size,
            SearchResult.name,
            SearchResult.rating,
            SearchResult.reviews,
            SearchResult.price_range,
            SearchResult.address,
            SearchResult.phone,
            SearchResult.website,
            SearchResult.email,
            SearchResult.contact_person
        ).filter(SearchResult.user_id == user_id)
        
        if search_date:
            query = query.filter(SearchResult.date == search_date)
            
        query = query.order_by(SearchResult.date.desc())
        
        df = pd.read_sql_query(query.statement, db.bind)
        
        # Handle cases where new columns might be missing
        for col in ['rating', 'reviews', 'phone', 'niche_size', 'price_range', 'contact_person']:
            if col not in df.columns:
                df[col] = ''
                
        # Clean placeholders from existing DB data
        placeholders_to_clean = ["Unknown Name", "No address", "not website", "No phone", "No rating", "0", "Unknown", "No email found", "No category"]
        df.replace(placeholders_to_clean, "", inplace=True)
        
        # Organize the column order and rename
        df = df[['date', 'country', 'city', 'niche', 'niche_size', 'name', 'rating', 'reviews', 'price_range', 'address', 'phone', 'website', 'email', 'contact_person']]
        df.columns = ['Date', 'Country', 'City', 'Search Niche', 'Niche Size', 'Business Name', 'Rating', 'Reviews', 'Price Range', 'Address', 'Phone Number', 'Website', 'Email', 'Contact Person']
        
        # Format the Date column for visual cleanliness
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Remove duplicate records based on business name and either address or phone
        df.drop_duplicates(subset=['Business Name', 'Address'], keep='first', inplace=True)
        df.drop_duplicates(subset=['Business Name', 'Phone Number'], keep='first', inplace=True)
        
        # Clean address newlines for better Excel formatting
        df['Address'] = df['Address'].apply(lambda x: str(x).replace('\n', ', ') if pd.notnull(x) else x)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return output
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        traceback.print_exc()
        return None
