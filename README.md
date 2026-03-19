# Aaref_Bledek Campaign Platform

Aaref_Bledek is a full-stack campaign platform built to support the EstateMind initiative for real-estate awareness in Tunisia. It combines a modern React landing experience with a Django REST backend that stores participant registrations, campaign regions, and campaign activities.

## Overview

The platform is designed around one core workflow:

1. Visitors explore the campaign vision and activities.
2. Visitors join the movement through a 3-step registration modal.
3. Registrations are validated and saved in the backend database.
4. Admin users can review all joined participants through Django Admin.

## Key Features

- Campaign landing page with animated sections and strong visual storytelling.
- Multi-step join form with front-end validation.
- Backend validation for:
  - Unique email addresses.
  - Tunisian phone number format.
  - Minimum motivation length.
- Campaign statistics endpoint (participants, regions, role distribution).
- Django Admin interface for managing joined users and campaign data.

## Tech Stack

### Frontend

- React (Create React App)
- Tailwind CSS
- Framer Motion
- Axios

### Backend

- Django 4.2
- Django REST Framework
- django-cors-headers
- python-decouple
- SQLite (local mode) or PostgreSQL (configurable)

## Project Structure

```text
Aaref_Bledek/
  backend/
    campaign/            # Models, serializers, views, API routes
    config/              # Django settings and global URL config
    manage.py
    requirements.txt
  frontend/
    src/components/      # UI sections and registration modal
    src/services/api.js  # Axios client for backend API
    package.json
```

## Data Model

### Participant

Stores each join request:

- full_name
- email (unique)
- phone
- region
- role (learner | contributor | volunteer | ambassador)
- motivation
- created_at
- is_active

### Region

Tracks campaign region entities:

- governorate
- delegation_count
- participant_count

### Activity

Defines campaign activities:

- title
- description
- activity_type
- icon
- participant_count

## API Endpoints

Base URL: `http://localhost:8000/api/campaign/`

- `GET /participants/` - List active participants
- `POST /participants/` - Register a new participant
- `GET /regions/` - List regions
- `GET /activities/` - List activities
- `GET /stats/` - Campaign summary stats

### Example Registration Request

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "20123456",
  "region": "Tunis",
  "role": "learner",
  "motivation": "I want to learn and help improve real estate transparency in Tunisia."
}
```

## Local Setup

## 1) Clone

```bash
git clone https://github.com/fares279/Aaref_Bledek-compaign.git
cd Aaref_Bledek-compaign
```

## 2) Backend Setup

Recommended Python version: 3.11 (matches the project virtual environment compatibility).

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create backend environment file:

- Copy `.env.template` to `.env`
- Update values as needed

Run migrations and start backend:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 3) Frontend Setup

In a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend default URL: `http://localhost:3000`

## 4) Create Admin User (Optional but Recommended)

```bash
cd backend
python manage.py createsuperuser
```

Admin URL: `http://127.0.0.1:8000/admin/`

## Form Validation Behavior

### Frontend checks

- Required full name
- Valid email format
- Tunisian phone format (`+216XXXXXXXX` or `XXXXXXXX`)
- Required region and role
- Motivation length >= 20 characters

### Backend checks

- Email uniqueness
- Phone regex validation
- Motivation minimum length
- Structured success/error response payload

## Current Notes

- The platform is campaign-focused and currently optimized around registration and participation.
- Stats and catalog endpoints are implemented and ready for richer frontend integration.
- Basic placeholder tests exist but should be expanded for production quality.

## Suggested Next Improvements

- Add automated API tests for participant registration and stats.
- Add frontend integration tests for the 3-step join modal.
- Add CI pipeline (lint + tests + build).
- Add production-ready deployment configs (Docker / Nginx / Gunicorn).

## Shareable Public URL (Production Guide)

If you want people on other devices to open your campaign page and submit the form into your database, you need both parts hosted online:

1. Backend API + database hosted on a cloud service.
2. Frontend hosted on a public static hosting service.

### What I already prepared in this repository

- Added deployment-oriented backend settings in `backend/config/settings.py`:
  - `ALLOWED_HOSTS` from env.
  - `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` from env.
  - secure proxy/cookie settings toggled by env.
  - WhiteNoise static serving for Django admin assets.
- Added backend deployment files:
  - `backend/Procfile`
  - `backend/build.sh`
  - `backend/runtime.txt`
- Added production dependencies to `backend/requirements.txt`:
  - `gunicorn`
  - `whitenoise`
- Extended `backend/.env.template` with deployment variables.

### Manual Steps You Must Do

You need to create cloud services/accounts and set environment variables. I cannot do these account-level operations for you from this environment.

## Option A (Recommended): Render + Render Postgres + Vercel

### Step 1: Deploy backend on Render

1. Create a new **Web Service** from your GitHub repo.
2. Set **Root Directory** to `backend`.
3. Build command:

```bash
bash build.sh
```

4. Start command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

5. Create a **Render Postgres** database.
6. Set backend environment variables in Render:

```env
SECRET_KEY=<strong-random-secret>
DEBUG=False
USE_SQLITE=False

DB_NAME=<from-render-postgres>
DB_USER=<from-render-postgres>
DB_PASSWORD=<from-render-postgres>
DB_HOST=<from-render-postgres>
DB_PORT=<from-render-postgres>

ALLOWED_HOSTS=<your-backend-service>.onrender.com
CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>
CSRF_TRUSTED_ORIGINS=https://<your-frontend-domain>

SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

7. After first deploy, run once in Render shell:

```bash
python manage.py createsuperuser
```

### Step 2: Deploy frontend on Vercel

1. Import the same GitHub repo in Vercel.
2. Set **Root Directory** to `frontend`.
3. Framework preset: Create React App.
4. Add frontend environment variable:

```env
REACT_APP_API_URL=https://<your-backend-service>.onrender.com/api/campaign
```

5. Deploy and get your public frontend URL.

### Step 3: Final CORS/CSRF sync

Update Render backend env values to your final Vercel domain:

```env
CORS_ALLOWED_ORIGINS=https://<your-vercel-domain>
CSRF_TRUSTED_ORIGINS=https://<your-vercel-domain>
```

Redeploy backend.

### Step 4: Validate end-to-end

1. Open your Vercel URL on phone/laptop.
2. Fill the Join form and submit.
3. Check records at:

`https://<your-backend-service>.onrender.com/admin/campaign/participant/`

If records appear there, your public flow is fully working.

## Option B (Quick temporary link, not recommended for production)

You can tunnel your local machine with tools like Cloudflare Tunnel or ngrok. This gives a shareable URL quickly, but:

- Your computer must stay on.
- Your internet must stay stable.
- Security and reliability are weaker.

For real usage, use Option A.

## Common Issues and Fixes

- **Form opens but submit fails (CORS error):**
  - Backend `CORS_ALLOWED_ORIGINS` does not match frontend URL exactly.
- **403 CSRF error:**
  - Add frontend domain to `CSRF_TRUSTED_ORIGINS`.
- **500 on submit:**
  - Check DB env vars and migrations.
- **Admin CSS broken:**
  - Ensure `collectstatic` ran during build (already handled by `build.sh`).

## Your final shareable URL

Send people the **frontend URL** (Vercel). They should not use backend API URLs directly.

Example:

`https://aaref-bledek-campaign.vercel.app`

Form submissions will then be stored in your hosted Postgres DB and visible in Django admin.

## Author

Developed for the EstateMind campaign initiative.
