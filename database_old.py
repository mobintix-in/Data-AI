import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:127081@localhost:5432/project")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initializes the database connection and creates the search_results table if it doesn't exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_results (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                country TEXT,
                city TEXT,
                niche TEXT,
                name TEXT,
                address TEXT,
                website TEXT,
                email TEXT,
                phone TEXT,
                rating TEXT,
                reviews TEXT,
                category TEXT,
                niche_size TEXT,
                price_range TEXT,
                contact_person TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Call init_db immediately so the table exists
init_db()
