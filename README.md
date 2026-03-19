# Aaref_Bledek Campaign Platform

Aaref_Bledek is a full-stack campaign platform for EstateMind's Tunisia real-estate awareness initiative. It includes:

1. A public React campaign website where users can join.
2. A Django REST backend that validates and stores registrations.
3. A Django Admin panel to review joined participants.

This README is a full deployment and operations playbook based on the working production setup.

## Table of Contents

1. Architecture
2. Features
3. Repository Structure
4. Local Development Setup
5. Production Deployment (Render + Vercel)
6. Environment Variables (Ready-to-Use)
7. Verification Checklist
8. Troubleshooting Guide (Real Incidents)
9. Security and Maintenance

## Architecture

### Frontend

- React (Create React App)
- Tailwind CSS
- Framer Motion
- Axios

### Backend

- Django 4.2
- Django REST Framework
- django-cors-headers
- WhiteNoise
- Gunicorn
- python-decouple

### Database

- Render PostgreSQL (production)
- SQLite (optional local fallback)

### Runtime Flow

1. User opens Vercel frontend URL.
2. Join form sends POST request to Render backend API.
3. Backend validates payload and writes to Render Postgres.
4. Admin reviews users in Django Admin.

## Features

- Animated campaign landing page sections.
- Multi-step join modal.
- Client-side and server-side validation.
- Read-only endpoints for campaign data.
- Campaign stats endpoint.
- Admin management for participants, regions, activities.

## Repository Structure

```text
Aaref_Bledek/
  backend/
    campaign/
      admin.py
      models.py
      serializers.py
      urls.py
      views.py
    config/
      settings.py
      urls.py
    .env.template
    .python-version
    build.sh
    Procfile
    runtime.txt
    requirements.txt
    manage.py
  frontend/
    src/
      components/
      services/api.js
    public/
    package.json
```

## Local Development Setup

## 1) Clone

```bash
git clone https://github.com/fares279/Aaref_Bledek-compaign.git
cd Aaref_Bledek-compaign
```

## 2) Backend

Use Python 3.11.

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
copy .env.template .env  # Windows
# cp .env.template .env  # macOS/Linux

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 3) Frontend

```bash
cd frontend
npm install
npm start
```

Frontend: http://localhost:3000
Backend: http://localhost:8000

## 4) Local Admin User

```bash
cd backend
python manage.py createsuperuser
```

Admin URL: http://127.0.0.1:8000/admin/

## Production Deployment (Render + Vercel)

## Step A: Deploy PostgreSQL on Render

1. Create a new Render Postgres instance.
2. Copy these values from database info page:
   - Hostname
   - Port
   - Database
   - Username
   - Password

## Step B: Deploy Backend on Render (Web Service)

Create Web Service from the same GitHub repo.

Use these settings:

- Runtime: Python
- Branch: main
- Root Directory: backend
- Build Command: bash build.sh
- Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
- Health Check Path: /healthz

Important compatibility setting:

- backend/.python-version is pinned to 3.11.9
- This avoids Django 4.2 + Python 3.14 admin/template runtime errors.

## Step C: Deploy Frontend on Vercel

Create project from same GitHub repo.

Use these settings:

- Framework: Create React App
- Root Directory: frontend
- Build Command: npm run build
- Output Directory: build

Set Vercel env var:

- REACT_APP_API_URL=https://aaref-bledek.onrender.com/api/campaign

Deploy and copy final production domain (for example: https://aaref-bledek.vercel.app).

## Step D: Final Backend CORS/CSRF Sync

After frontend domain is live, update backend env:

- CORS_ALLOWED_ORIGINS=https://aaref-bledek.vercel.app
- CSRF_TRUSTED_ORIGINS=https://aaref-bledek.vercel.app

Redeploy backend.

## Environment Variables (Backend, Production)

Set these in Render Web Service environment:

```env
SECRET_KEY=<strong-random-secret>
DEBUG=False
TIME_ZONE=UTC

USE_SQLITE=False
DB_NAME=<render_db_name>
DB_USER=<render_db_user>
DB_PASSWORD=<render_db_password>
DB_HOST=<render_db_host>
DB_PORT=5432
DB_SSLMODE=require
DB_CONN_MAX_AGE=0
DB_CONN_HEALTH_CHECKS=True

ALLOWED_HOSTS=aaref-bledek.onrender.com,.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://aaref-bledek.vercel.app
CSRF_TRUSTED_ORIGINS=https://aaref-bledek.vercel.app
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Optional admin bootstrap when shell access is unavailable:

```env
CREATE_SUPERUSER=True
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=you@example.com
DJANGO_SUPERUSER_PASSWORD=<strong-password>
```

After first successful deploy and login, set CREATE_SUPERUSER to False.

## API Reference

Base URL:

- Local: http://localhost:8000/api/campaign/
- Production: https://aaref-bledek.onrender.com/api/campaign/

Endpoints:

- GET /participants/
- POST /participants/
- GET /regions/
- GET /activities/
- GET /stats/

Example payload:

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "20123456",
  "region": "Tunis",
  "role": "learner",
  "motivation": "I want to learn and contribute to real estate transparency in Tunisia."
}
```

## Verification Checklist

Run these checks after deployment:

1. Backend health:
   - https://aaref-bledek.onrender.com/healthz
2. Backend admin login:
   - https://aaref-bledek.onrender.com/admin/
3. API root:
   - https://aaref-bledek.onrender.com/api/campaign/
4. Frontend site:
   - https://aaref-bledek.vercel.app
5. Submit form from frontend and confirm in admin participants list.

Note: backend root URL `/` returning 404 is expected and not an error.

## Troubleshooting Guide (Real Incidents)

## 1) Build fails on Pillow with Python 3.14

Symptom:

- Failed to build Pillow during Render build.

Fix:

- Remove unused Pillow dependency.

## 2) Build fails on psycopg2-binary

Symptom:

- Error loading psycopg module or no matching distribution.

Fix:

- Use psycopg v3 binary package in requirements.

## 3) Admin page returns 500 with Django template context error

Symptom:

- AttributeError in django/template/context internals.

Fix:

- Run backend on Python 3.11 (pin in backend/.python-version).

## 4) Bad Request (400) on all URLs

Symptom:

- DisallowedHost behavior.

Fix:

- Ensure env key is ALLOWED_HOSTS (plural), not ALLOWED_HOST.

## 5) Vercel build fails while local build works

Symptom:

- CI build fails due warnings treated as errors.

Fix:

- Remove UTF-8 BOM from affected source file.

## 6) CORS or CSRF errors on form submission

Fix:

- CORS_ALLOWED_ORIGINS and CSRF_TRUSTED_ORIGINS must exactly match deployed frontend domain.

## Security and Maintenance

## Required security actions

1. Rotate SECRET_KEY if exposed.
2. Rotate database password/credentials if exposed.
3. Disable CREATE_SUPERUSER after first setup.

## Free tier warning

Render free Postgres instances can expire if not upgraded. Monitor database expiry date in Render dashboard.

## Suggested improvements

1. Add automated API tests.
2. Add frontend integration tests for join form.
3. Add CI (lint + test + build).
4. Add backup/export strategy for participant data.

## Author

Developed for the EstateMind campaign initiative.
