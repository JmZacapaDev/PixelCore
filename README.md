# PixelCore API

## Project Overview
PixelCore API is a backend for a content-sharing platform where users can register, log in, upload or manage content (games, videos, artwork, music), and rate items (1–5 stars).

## Tech Stack
- **Framework:** Django + Django REST Framework
- **Auth:** djangorestframework-simplejwt
- **Database:** PostgreSQL
- **Environment Variables:** `.env` file with `python-dotenv`
- **Documentation:** drf-spectacular (Swagger / OpenAPI 3.0)
- **Filtering:** django-filter
- **Tests:** unittest
- **CORS:** django-cors-headers
- **Database URL Parsing:** dj-database-url

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd ngp/PixelCore
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
First, create a `requirements.txt` file:
```bash
pip freeze > requirements.txt
```
Then install:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the `PixelCore/` directory (same level as `manage.py`) based on `.env.example`.

**`.env.example` content:**
```
# Django secret key. KEEP THIS SECRET IN PRODUCTION!
SECRET_KEY='your_secret_key_here'

# Set to True for development, False for production
DEBUG=True

# Database settings
# Example for PostgreSQL:
# DATABASE_URL='postgres://user:password@host:port/database_name'
DATABASE_URL='postgres://user:password@host:port/database_name' # IMPORTANT: Configure your PostgreSQL connection string

# Allowed hosts for Django. Comma-separated values.
# Example: ALLOWED_HOSTS='localhost,127.0.0.1,.example.com'
ALLOWED_HOSTS='localhost,127.0.0.1'

# CORS settings
# Set to True to allow all origins for development.
# In production, specify allowed origins: CORS_ALLOWED_ORIGINS='https://example.com,https://sub.example.com'
CORS_ALLOW_ALL_ORIGINS=True
```
**IMPORTANT:** Ensure you configure `DATABASE_URL` with your PostgreSQL connection string.

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Seed the Database (Optional)
To populate the database with sample data:
```bash
python manage.py seed
```

### 7. Create a Superuser (Optional)
To access the Django Admin panel:
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Documentation (Swagger UI)
Once the server is running, access the interactive API documentation at:
`http://127.0.0.1:8000/api/docs/`

## Running Tests
```bash
python manage.py test
```

## Project Structure
```
PixelCore/
├── PixelCore/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── content/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── management/
│   │   └── commands/
│   │       └── seed.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── exceptions.py
│   └── tests.py
├── ratings/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .env.example
└── venv/
```
