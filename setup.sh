#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting PixelCore API setup..."

# --- 1. Check for Docker ---
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker to proceed with the local PostgreSQL setup."
    echo "Refer to the README.md for more details."
    exit 1
fi

echo "Docker found. Proceeding with Docker Compose setup."

# --- 2. Start Docker Compose PostgreSQL service ---
echo "Starting PostgreSQL database with Docker Compose..."
docker-compose up -d db

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker inspect pixelcore_db --format='{{.State.Health.Status}}' | grep -q "healthy"; do
  printf "."
  sleep 1
done
echo "PostgreSQL is healthy."

# --- 3. Create and Activate Virtual Environment ---
echo "Creating and activating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# --- 4. Install Dependencies ---
echo "Installing Python dependencies..."
pip install -r requirements.txt

# --- 5. Run Django Migrations ---
echo "Running Django migrations..."
python manage.py migrate

# --- 6. Seed the Database ---
echo "Seeding the database with sample data..."
python manage.py seed

# --- 7. Run the Development Server ---
echo "Starting Django development server..."
echo "API will be available at http://127.0.0.1:8000/"
echo "Swagger UI at http://127.0.0.1:8000/api/docs/"
python manage.py runserver
