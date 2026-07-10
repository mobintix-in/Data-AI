from sqlalchemy import create_engine, text
from db.database import init_db
from core.config import settings
from db.models import Base # Ensure models are imported so metadata is populated

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS search_results CASCADE;"))
    conn.commit()

init_db()
print("Table search_results dropped and recreated.")
