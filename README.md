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

### Quick Setup (Recommended)
For a quick and easy setup, use the provided `setup.sh` script. This script will:
- Ensure Docker is running.
- Start the local PostgreSQL database using Docker Compose.
- Create a .env file with the necessary DATABASE_URL.
- Create and activate the Python virtual environment.
- Install all necessary Python dependencies.
- Run database migrations.
- Seed the database with sample data (including a superuser).
- Start the Django development server.

To run the quick setup:
1.  **Ensure Docker is running** on your system.
2.  **Navigate to the `PixelCore/` directory**.
3.  **Run the setup script:**
    ```bash
    ./setup.sh
    ```
    The API will be available at `http://127.0.0.1:8000/`.
    Swagger UI at `http://127.0.0.1:8000/api/docs/`.

    A superuser for testing purposes will be created with the following credentials:
    - **Email:** `admin@tests.com`
    - **Password:** `admin123`

### Manual Setup

If you prefer a manual setup or need more control, follow these steps:

### 1. Clone the Repository
```bash
git clone <repository_url>
# You will be inside the 'PixelCore' directory after cloning.
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
If you are performing a manual setup, create a `.env` file in the `PixelCore/` directory (same level as `manage.py`) based on `.env.example`. The `setup.sh` script handles this automatically.

**`.env.example` content:**
```
# Django secret key. KEEP THIS SECRET IN PRODUCTION!
SECRET_KEY='your_secret_key_here'

# Set to True for development, False for production
DEBUG=True

# Database settings
# For local development with Docker Compose PostgreSQL:
# DATABASE_URL='postgres://pixelcore_user:pixelcore_password@localhost:5432/pixelcore_db'
DATABASE_URL='postgres://pixelcore_user:pixelcore_password@localhost:5432/pixelcore_db'

# These variables are used by docker-compose.yml for the PostgreSQL service
POSTGRES_DB=pixelcore_db
POSTGRES_USER=pixelcore_user
POSTGRES_PASSWORD=pixelcore_password

# Allowed hosts for Django. Comma-separated values.
# Example: ALLOWED_HOSTS='localhost,127.0.0.1,.example.com'
ALLOWED_HOSTS='localhost,127.0.0.1'

# CORS settings
# Set to True to allow all origins for development.
# In production, specify allowed origins: CORS_ALLOWED_ORIGINS='https://example.com,https://sub.example.com'
CORS_ALLOW_ALL_ORIGINS=True
```
**IMPORTANT:** If you are using the Docker Compose setup for PostgreSQL (recommended for local development), ensure your `.env` file contains the `DATABASE_URL` as shown in `.env.example`. The `setup.sh` script handles this automatically.

### 4.1. Local PostgreSQL Setup with Docker Compose (Recommended for Development)
To easily set up a local PostgreSQL database, you can use Docker Compose.

1.  **Ensure Docker is running** on your system.
2.  **Navigate to the `PixelCore/` directory** (where `docker-compose.yml` is located).
3.  **Start the PostgreSQL service:**
    ```bash
    docker-compose up -d db
    ```
    This will start a PostgreSQL container in the background.
4.  **Verify the database is running:**
    ```bash
    docker-compose ps
    ```
    You should see `pixelcore_db` with a healthy status.
5.  **The `DATABASE_URL` in your `.env` file should be configured as:**
    `DATABASE_URL='postgres://pixelcore_user:pixelcore_password@localhost:5432/pixelcore_db'`
    (These credentials match the defaults in `docker-compose.yml` and `.env.example`).

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Seed the Database (Optional)
To populate the database with sample data, including a superuser for admin access:
```bash
python manage.py seed
```
A superuser for testing purposes will be created with the following credentials:
- **Email:** `admin@tests.com`
- **Password:** `admin123`
You can use these credentials to log in to the Django Admin panel (`http://127.0.0.1:8000/admin/`) or to obtain JWT tokens for testing authenticated API endpoints.

### 7. Create a Superuser (Optional)
To access the Django Admin panel:
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```


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
└── .venv/
```
