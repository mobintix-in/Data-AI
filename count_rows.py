from sqlalchemy import create_engine, text
from config.settings import settings
engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    users_count = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
    search_results_count = conn.execute(text("SELECT COUNT(*) FROM search_results")).scalar()
    print(f"Users: {users_count}")
    print(f"Search Results: {search_results_count}")
