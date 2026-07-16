# Lead Generation SaaS (Backend API)

The backend API for a SaaS application that scrapes local business leads from Google Maps and extracts contact emails from their websites. Built with Python and FastAPI.

## Features
- **Authentication**: JWT-based user authentication (Register, Login, Password Reset).
- **Google Maps Scraper API**: Search for businesses by niche, city, and country.
- **Website Email Extractor API**: Automatically visits scraped websites to find contact emails.
- **Lead Management API**: Manage search history and lead details.
- **Data Export**: Generate Excel files with scraped leads (including phone numbers, emails, addresses, and ratings).

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, Uvicorn.
- **Database**: SQLite (managed with Alembic migrations).

---

## Getting Started

### Prerequisites
- Python 3.9+

### Setup

Navigate to the root directory and set up a virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (optional if database.sqlite already exists)
alembic upgrade head

# Start the FastAPI server
python app.py
```
*The backend API will be available at `http://localhost:5000`.*

---

## Project Structure

```text
├── alembic/              # Database migration scripts
├── api/ & routes/        # FastAPI route definitions (Auth & Main API)
├── core/ & config/       # Backend configuration and security settings
├── database/ & db/       # SQLAlchemy models and database session setup
├── models/ & schemas/    # Pydantic schemas and SQLAlchemy models
├── app.py                # Main FastAPI application entry point
├── scraper.py            # Google Maps scraping logic
└── scraper_utils.py      # Website email extraction logic
```

## License
MIT License
