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

## Author

Developed for the EstateMind campaign initiative.
