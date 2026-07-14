from sqlalchemy import create_engine, text
from database.session import Base
from config.settings import settings
import models.user
import models.search_result

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS search_results CASCADE;"))
    conn.commit()

Base.metadata.create_all(bind=engine)
print("Table search_results dropped and recreated using correct Base.")
