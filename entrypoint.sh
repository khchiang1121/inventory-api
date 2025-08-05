#!/bin/bash
# Verify that Postgres is healthy before applying the migrations and running the Django development server
# if [ "$DATABASE" = "postgres" ] then echo "Waiting for postgres..."
#     while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#       sleep 0.1
#     done
#     echo "PostgreSQL started"
# fi
source .env

echo "Waiting for postgres at $POSTGRES_HOST:$POSTGRES_PORT..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.5
done
echo "PostgreSQL started"

# 套用 migrations（不會重新產生 migration 檔案）
echo "📦 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# 收集靜態檔案（視需求）
echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
