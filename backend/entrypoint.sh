#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL started"

# Create migrations for our apps first
echo "Creating migrations..."
python manage.py makemigrations Usuarios || true
python manage.py makemigrations Libros || true

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create users if they don't exist
echo "Creating users..."
python manage.py shell <<'PYEOF'
import os
from django.contrib.auth import get_user_model
User = get_user_model()

# Create Superuser
superuser_username = os.getenv('SUPERUSER_USERNAME', 'superadmin')
superuser_email = os.getenv('SUPERUSER_EMAIL', 'superadmin@gestlib.com')
superuser_password = os.getenv('SUPERUSER_PASSWORD', 'SuperAdmin2024!')
superuser_dni = os.getenv('SUPERUSER_DNI', '12345678')
superuser_fullname = os.getenv('SUPERUSER_FULLNAME', 'Super Administrador del Sistema')

if not User.objects.filter(username=superuser_username).exists():
    User.objects.create_superuser(
        username=superuser_username,
        email=superuser_email,
        password=superuser_password,
        dni=superuser_dni,
        full_name=superuser_fullname,
        address='Oficina Principal',
        type='administrador'
    )
    print(f'Superuser created: {superuser_username}/{superuser_password}')
else:
    print('Superuser already exists')

# Create Admin User
admin_username = os.getenv('ADMIN_USERNAME', 'admin')
admin_email = os.getenv('ADMIN_EMAIL', 'admin@gestlib.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'Admin2024!')
admin_dni = os.getenv('ADMIN_DNI', '87654321')
admin_fullname = os.getenv('ADMIN_FULLNAME', 'Administrador de Biblioteca')

if not User.objects.filter(username=admin_username).exists():
    admin_user = User.objects.create_user(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        dni=admin_dni,
        full_name=admin_fullname,
        address='Biblioteca Central',
        type='administrador',
        is_staff=True
    )
    print(f'Admin user created: {admin_username}/{admin_password}')
else:
    print('Admin user already exists')
PYEOF

# Load books data if CSV file exists and no books exist yet
if [ -f "data.csv" ]; then
    echo "Checking if books need to be loaded..."
    BOOK_COUNT=$(python manage.py shell -c "from Libros.models import Libro; print(Libro.objects.count())")
    if [ "$BOOK_COUNT" = "0" ]; then
        echo "No books found. Loading from data.csv..."
        python manage.py cargar_libros --file=data.csv --limit=200
    else
        echo "Books already loaded ($BOOK_COUNT books found)"
    fi
else
    echo "No data.csv file found, skipping book loading"
fi

# Start server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000