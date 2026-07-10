from sqlalchemy import create_engine, text
from core.config import settings
engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='search_results'"))
    print([r[0] for r in result])
