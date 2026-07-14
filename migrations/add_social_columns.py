from sqlalchemy import create_engine, text
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    # Add new boolean columns if they don't exist
    columns_to_add = [
        "has_facebook", "has_instagram", "has_linkedin", 
        "has_twitter", "has_youtube", "has_whatsapp"
    ]
    
    for col in columns_to_add:
        try:
            conn.execute(text(f"ALTER TABLE search_results ADD COLUMN {col} BOOLEAN DEFAULT FALSE;"))
            print(f"Added column {col}")
        except Exception as e:
            # Column might already exist
            print(f"Skipping {col} (might already exist): {e}")
            
    conn.commit()

print("Social media columns migration complete.")
