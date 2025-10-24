#!/bin/bash
# Script to start Django dashboard

echo "Starting IoTShield Dashboard..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo "You can create a superuser with: python manage.py createsuperuser"

# Collect static files
python manage.py collectstatic --noinput

# Start development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
