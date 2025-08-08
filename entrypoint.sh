#!/bin/bash

source .env

# Verify that Postgres is healthy before applying the migrations and running the Django development server
echo "Waiting for postgres at $POSTGRES_HOST:$POSTGRES_PORT..."

# while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#     sleep 0.5
# done
# echo "PostgreSQL started"

# 等待 PostgreSQL 準備就緒
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "等待 PostgreSQL 啟動中..."
  sleep 2
done

echo "PostgreSQL started"

# 套用 migrations
echo "📦 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# 收集靜態檔案（視需求）
echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
