# Lead Generation SaaS

A full-stack SaaS application for scraping local business leads from Google Maps and extracting contact emails from their websites. Features a Python FastAPI backend and a Next.js frontend with Tailwind CSS.

## Features
- **Authentication**: JWT-based user authentication (Register, Login, Password Reset).
- **Google Maps Scraper**: Search for businesses by niche, city, and country.
- **Website Email Extractor**: Automatically visits scraped websites to find contact emails.
- **Lead Dashboard**: View search history and lead details in a beautiful dashboard.
- **Excel Export**: Download scraped leads (including phone numbers, emails, addresses, and ratings) directly into an Excel file.

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, Uvicorn.
- **Frontend**: Next.js 16 (React 19), Tailwind CSS v4, Lucide Icons, Axios.
- **Database**: SQLite (managed with Alembic migrations).

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+ & npm

### 1. Backend Setup

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

### 2. Frontend Setup

Open a new terminal, navigate to the `frontend` directory, and install dependencies:

```bash
cd frontend

# Install Node modules
npm install

# Start the development server
npm run dev
```
*The frontend application will be available at `http://localhost:3000`.*

---

## Project Structure

```text
├── alembic/              # Database migration scripts
├── api/ & routes/        # FastAPI route definitions (Auth & Main API)
├── core/ & config/       # Backend configuration and security settings
├── database/ & db/       # SQLAlchemy models and database session setup
├── frontend/             # Next.js frontend application
│   ├── src/app/          # Next.js App Router (pages, layouts)
│   └── src/services/     # API service configuration (Axios)
├── models/ & schemas/    # Pydantic schemas and SQLAlchemy models
├── static/               # Generated static files (Excel exports)
├── app.py                # Main FastAPI application entry point
├── scraper.py            # Google Maps scraping logic
└── scraper_utils.py      # Website email extraction logic
```

## License
MIT License
