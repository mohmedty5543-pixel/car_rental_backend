# Car Rental Marketplace — Django Backend

Production-ready multi-vendor car rental marketplace backend.

## Tech
- Python 3.13+, Django 5+, DRF, SimpleJWT, drf-spectacular
- PostgreSQL, Pillow, django-filter
- Docker / Gunicorn / Nginx

## Quick start (Windows / PowerShell)

```powershell
# 1. Install Python 3.13+ from https://www.python.org/downloads/
# 2. Install PostgreSQL 16+ from https://www.postgresql.org/download/windows/
# 3. Install Git from https://git-scm.com/download/win
# 4. Install VS Code from https://code.visualstudio.com/

# Create venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements/dev.txt

# Create database (in psql)
# CREATE DATABASE car_rental;
# CREATE USER car_rental WITH PASSWORD 'car_rental';
# GRANT ALL PRIVILEGES ON DATABASE car_rental TO car_rental;

# Configure environment
copy .env.example .env
# edit .env

# Migrate & run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API docs: http://localhost:8000/api/docs/

## Docker

```bash
docker compose up --build
```

## Project layout

See `docs/ARCHITECTURE.md`.
